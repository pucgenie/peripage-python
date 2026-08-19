# peripage-python - python library for peripage thermal printers
# Copyright (C) 2020-2023  bitrate16 (pegasko)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


async def main():
    import argparse
    from peripage import PrinterType, PeripagePrinter
    import peripage

    parser = argparse.ArgumentParser(description='Print on a Peripage printer via bluetooth')
    parser.add_argument(
        '-m', '--mac',
        help="Bluetooth MAC address of the printer. If it's not a well-formed MAC address, device discovery will be run.",
        required=True,
        type=str
    )
    parser.add_argument(
        '-c', '--concentration',
        help='Concentration value for printing (temperature)',
        choices=[0, 1, 2],
        metavar='[0-2]',
        type=int,
        default=0
    )
    parser.add_argument(
        '-b', '--break',
        dest='break_size',
        help='Size of the break inserted after printed image or text',
        choices=range(256),
        metavar='[0-255]',
        type=int,
        default=0
    )
    parser.add_argument(
        '-p', '--printer',
        help='Printer model selection',
        choices=PrinterType.names(),
        type=str,
        required=True
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-t', '--text',
        help='ASCII text to print. Text must be ASCII-safe and will be filtered for invalid characters',
        type=str
    )
    group.add_argument(
        '-s', '--stream',
        help='Print text received from STDIN, line by line. Text must be ASCII-safe and will be filtered for invalid characters',
        action='store_true'
    )
    group.add_argument(
        '-i', '--image',
        help='Path to the image for printing',
        type=str
    )
    group.add_argument(
        '-q', '--qr',
        help='String to convert into a QR code for printing',
        type=str
    )
    group.add_argument(
        '-e', '--introduce',
        help='Ask the printer to introduce itself',
        action='store_true'
    )

    args = parser.parse_args()
    del parser

    import sys
    try:
        import peripage.PIL
    except ModuleNotFoundError as mnfe:
        from sys import stderr
        print("Your environment is missing PIL. Suggestion (mind your venv etc.): python3 -m pip install 'Pillow'", file=stderr,)
        #raise mnfe
    
    import re
    if re.fullmatch("..:..:..:..:..:..", args.mac,) is not None:
        factory: PeripagePrinter = None
        import importlib
        for factory_module, factory_impl, notfound_message in [
            ('.bleak_impl', 'PeripageBleakPrinter', "Your environment is missing bleak. Suggestion (mind your venv etc.): python3 -m pip install 'bleak'",),
            ('.bluez_impl', 'PeripageBluezPrinter', "Your environment is missing pybluez. Suggestion (mind your venv etc.): python3 -m pip install 'PyBluez-bitalino'",),
            ]:
            try:
                from .bleak_impl import PeripageBleakPrinter
                factory = PeripageBleakPrinter
                #factory = importlib.import_module(factory_impl, package=factory_module,)
                #exec(f"""from {factory_module} import {factory_impl} as PeripageXPrinter""")
                #factory = PeripageXPrinter
                break
            except ModuleNotFoundError as mnfe:
                from sys import stderr
                print(notfound_message, file=stderr,)
        else:
            print("No loadable communication layer found!", file=sys.stderr,)
            sys.exit(2)
            
        printer = factory(args.mac, PrinterType[args.printer])
        #print("factory:", factory,)
        #printer = PeripageXPrinter(args.mac, PrinterType[args.printer])
    else:
        from peripage.bleak_impl import PeripageBleakPrinter
        from bleak.backends.device import BLEDevice
        printer0: BLEDevice = await PeripageBleakPrinter.discover_devices(PeripageBleakPrinter)
        if printer0 is None:
            sys.exit(0)
        # FIXME: Don't assume Peripage A6 as printer type.
        printer = PeripageBleakPrinter(printer0.address, PrinterType.A6,)

    await printer.connect()
    await printer.reset()

    # Act based on args
    if getattr(args, 'introduce', False,):

        # print('Hello, my name is Harold..')
        device_full = await printer.getDeviceFull()
        print(device_full.decode('ascii'))
        await printer.disconnect()
        sys.exit(0)

    elif getattr(args, 'stream', False,):

        await printer.setConcentration(args.concentration)

        while True:
            try:
                line = input().rstrip()

                await printer.printlnASCII(line)

            except EOFError:
                # Input closed ^d^d
                break

        if args.break_size > 0:
            await printer.printBreak(args.break_size)

        await printer.disconnect()

        sys.exit(0)

    elif getattr(args, 'text', None,) is not None:

        await printer.setConcentration(args.concentration)

        text = args.text.rstrip()

        if len(text) > 0:
            await printer.printASCII(text)
            await printer.flushASCII()

        if args.break_size > 0:
            await printer.printBreak(args.break_size)

        await printer.disconnect()

        sys.exit(0)

    elif getattr(args, 'image', None,) is not None:

        await printer.setConcentration(args.concentration)

        try:
            import PIL.Image
            img = PIL.Image.open(args.image)
        except:
            print(f'Failed to open image { args.image }', file=sys.stderr,)
            sys.exit(1)

        await printer.printImage(img)

        if args.break_size > 0:
            await printer.printBreak(args.break_size)

        await printer.disconnect()

        sys.exit(0)

    elif getattr(args, 'qr', None,) is not None:

        await printer.setConcentration(args.concentration)

        await printer.printQR(args.qr)

        if args.break_size > 0:
            await printer.printBreak(args.break_size)

        await printer.disconnect()

        sys.exit(0)

    else:

        print('How did you get there?')
    #asyncio.run(PeripageBleakPrinter.discover_devices(address='C0:15:83:15:1F:78'))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
