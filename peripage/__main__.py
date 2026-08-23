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
import sys

async def main():
    import argparse
    from peripage import PrinterType, PeripagePrinter
    import peripage

    parser = argparse.ArgumentParser(description='Print on a Peripage printer via bluetooth')
    parser.add_argument(
        'mac',
        help="Bluetooth MAC address of the printer. If it's not a well-formed MAC address, device discovery will be run.",
        type=str
    )
    # pucgenie: I hope we could dynamically determine that somehow
    parser.add_argument(
        '-p', '--printer',
        help='Printer model selection',
        choices=PrinterType.names(),
        type=str,
        required=True
    )
    parser.add_argument(
        '-c', '--concentration',
        help='Concentration value for printing (temperature), affects contrast',
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

    subparsers = parser.add_subparsers(dest="mode", required=True, help="Operation",)
    parser_text = subparsers.add_parser("text", help="Print text")
    parser_text.add_argument(
        'text',
        help='ASCII text to print. Text must be ASCII-safe and will be filtered for invalid characters',
        type=str
    )

    parser_stream = subparsers.add_parser("stream", help="Print text received from STDIN, line by line. Text must be ASCII-safe and will be filtered for invalid characters")

    parser_img = subparsers.add_parser("image", help="Image printing")
    parser_img.add_argument(
        'image',
        help='Path to the image for printing',
        type=str
    )
    parser_img.add_argument(
        '--mirror',
        help='Mirror image for printing',
        action='store_true'
    )

    parser_qr = subparsers.add_parser("qr", help="Print text")
    parser_qr.add_argument(
        'qr',
        help='String to convert into a QR code for printing',
        type=str
    )

    parser_introduce = subparsers.add_parser("introduce", help="Ask the printer to introduce itself")

    args = parser.parse_args()
    del parser

    try:
        import peripage.PIL
    except ModuleNotFoundError as mnfe:
        from sys import stderr
        print("Your environment is missing PIL. Suggestion (mind your venv etc.): python3 -m pip install 'Pillow'", file=stderr,)
        #raise mnfe
    
    import re
    if re.fullmatch("..:..:..:..:..:..", args.mac,) is not None:
        factory: list[PeripagePrinter] = [None,]
        import importlib
        for factory_module, factory_impl, notfound_message in [
            ('.bleak_impl', 'PeripageBleakPrinter', "Your environment is missing bleak. Suggestion (mind your venv etc.): python3 -m pip install 'bleak'",),
            ('.bluez_impl', 'PeripageBluezPrinter', "Your environment is missing pybluez. Suggestion (mind your venv etc.): python3 -m pip install 'PyBluez-bitalino'",),
            ]:
            try:
                exec(f"""from {factory_module} import {factory_impl}
factory[0] = {factory_impl}""", globals=globals(), locals=locals(),)
                #from .bleak_impl import PeripageBleakPrinter
                #exec(f"""""", globals=globals(), locals=locals(),)
                #factory = importlib.import_module(factory_impl, package=factory_module,)
                assert factory[0] is not None
                break
            except ModuleNotFoundError as mnfe:
                from sys import stderr
                print(notfound_message, file=stderr,)
        else:
            print("No loadable communication layer found!", file=sys.stderr,)
            sys.exit(2)
            
        printer = factory[0](args.mac, PrinterType[args.printer])
        #print("factory:", factory,)
        #printer = PeripageXPrinter(args.mac, PrinterType[args.printer])
    else:
        from peripage.bleak_impl import PeripageBleakPrinter
        from bleak.backends.device import BLEDevice
        printer0: BLEDevice = await PeripageBleakPrinter.discover_devices(PeripageBleakPrinter)
        if printer0 is None:
            sys.exit(0)
        printer = PeripageBleakPrinter(printer0.address, PrinterType[args.printer],)

    await printer.connect()
    await printer.reset()

    # Act based on args
    match args.mode:
        case 'introduce':
            # print('Hello, my name is Harold..')
            device_full = await printer.getDeviceFull()
            print(device_full.decode('ascii'))
            await printer.disconnect()
            sys.exit(0)

        case 'stream':
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

        case 'text':
            await printer.setConcentration(args.concentration)

            text = args.text.rstrip()

            if len(text) > 0:
                await printer.printASCII(text)
                await printer.flushASCII()

            if args.break_size > 0:
                await printer.printBreak(args.break_size)

            await printer.disconnect()

            sys.exit(0)

        case 'image':
            await printer.setConcentration(args.concentration)

            try:
                import PIL.Image
                img = PIL.Image.open(args.image)
            except:
                print(f'Failed to open image { args.image }', file=sys.stderr,)
                sys.exit(1)

            await printer.printImage(img, mirror=args.mirror,)

            if args.break_size > 0:
                await printer.printBreak(args.break_size)

            await printer.disconnect()

            sys.exit(0)

        case 'qr':

            await printer.setConcentration(args.concentration)

            await printer.printQR(args.qr)

            if args.break_size > 0:
                await printer.printBreak(args.break_size)

            await printer.disconnect()

            sys.exit(0)

        case _:
            print('How did you get there?')

if __name__ == '__main__':
    import asyncio
    #if sys.platform == "win32":
    #    # pucgenie: I hope this fixes "service not found" on Windows. Maybe we need to use bleakclient.pair() when connecting on Windows instead...
    #    asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop,)
    #else:
    asyncio.run(main())
