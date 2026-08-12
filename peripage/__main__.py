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


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Print on a Peripage printer via bluetooth')
    parser.add_argument(
        '-m', '--mac',
        help='Bluetooth MAC address of the printer',
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
        choices=peripage.PrinterType.names(),
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
    import peripage
    from peripage import PeripagePrinter, PrinterType
    try:
        import peripage.PIL
    except ModuleNotFoundError as mnfe:
        from sys import stderr
        print("Your environment is missing PIL. Suggestion (mind your venv etc.): python3 -m pip install 'Pillow'", file=stderr,)
        #raise mnfe
    
    factory: PeripagePrinter = None
    for factory_module, factory_impl, notfound_message in [
        ('.bleak_impl', 'PeripageBleakPrinter', "Your environment is missing bleak. Suggestion (mind your venv etc.): python3 -m pip install 'bleak'",),
        ('.bluez_impl', 'PeripageBluezPrinter', "Your environment is missing pybluez. Suggestion (mind your venv etc.): python3 -m pip install 'PyBluez-bitalino'",),
        ]:
        try:
            exec(f"from {factory_module} import {factory_impl}")
            factory = eval(factory_impl)
        except ModuleNotFoundError as mnfe:
            from sys import stderr
            print(notfound_message, file=stderr,)
    else:
        print("No loadable communication layer found!", file=stderr,)
        sys.exit(2)
        
    printer = factory(args.mac, PrinterType[args.printer])
    printer.connect()
    printer.reset()

    # Act based on args
    if getattr(args, 'introduce', False,):

        # print('Hello, my name is Harold..')
        print(printer.getDeviceFull().decode('ascii'))
        printer.disconnect()
        sys.exit(0)

    elif getattr(args, 'stream', False,):

        printer.setConcentration(args.concentration)

        while True:
            try:
                line = input().rstrip()

                printer.printlnASCII(line)

            except EOFError:
                # Input closed ^d^d
                break

        if args.break_size > 0:
            printer.printBreak(args.break_size)

        printer.disconnect()

        sys.exit(0)

    elif getattr(args, 'text', None,) is not None:

        printer.setConcentration(args.concentration)

        text = args.text.rstrip()

        if len(text) > 0:
            printer.printASCII(text)
            printer.flushASCII()

        if args.break_size > 0:
            printer.printBreak(args.break_size)

        printer.disconnect()

        sys.exit(0)

    elif getattr(args, 'image', None,) is not None:

        printer.setConcentration(args.concentration)

        try:
            import PIL.Image
            img = PIL.Image.open(args.image)
        except:
            print(f'Failed to open image { args.image }', file=sys.stderr,)
            sys.exit(1)

        printer.printImage(img)

        if args.break_size > 0:
            printer.printBreak(args.break_size)

        printer.disconnect()

        sys.exit(0)

    elif getattr(args, 'qr', None,) is not None:

        printer.setConcentration(args.concentration)

        printer.printQR(args.qr)

        if args.break_size > 0:
            printer.printBreak(args.break_size)

        printer.disconnect()

        sys.exit(0)

    else:

        print('How did you get there?')

if __name__ == '__main__':
    main()
