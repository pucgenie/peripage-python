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

# Manjaro Linux test:
"""
Found: C0:15:83:15:1F:78 "PeriPage_1F78_BLE"
Connected: True
BleakClient, C0:15:83:15:1F:78
['__aenter__', '__aexit__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__', '_backend', '_backend_id', '_pair_before_connect', 'address', 'backend_id', 'connect', 'disconnect', 'is_connected', 'mtu_size', 'name', 'pair', 'read_gatt_char', 'read_gatt_descriptor', 'services', 'start_notify', 'stop_notify', 'unpair', 'write_gatt_char', 'write_gatt_descriptor']
49535343-fe7d-4ae5-8fa9-9fafd205e455 (Handle: 1): Unknown
0000fee7-0000-1000-8000-00805f9b34fb (Handle: 12): Tencent Holdings Limited
0000ff80-0000-1000-8000-00805f9b34fb (Handle: 20): Vendor specific
0000180a-0000-1000-8000-00805f9b34fb (Handle: 26): Device Information
0000ff00-0000-1000-8000-00805f9b34fb (Handle: 35): Vendor specific

[Service] 49535343-fe7d-4ae5-8fa9-9fafd205e455 (Handle: 1): UART (Unknown)
  [Characteristic] 49535343-6daa-4d02-abf6-19569aca69fe (Handle: 2): Unknown (write)
  [Characteristic] 49535343-8841-43f4-a8d4-ecbe34729bb3 (Handle: 4): Unknown (write-without-response,write), Max write w/o rsp size: 182
  [Characteristic] 49535343-1e4d-4bd9-ba61-23c647249616 (Handle: 6): Unknown (notify)
    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 8): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
  [Characteristic] 49535343-aca3-481c-91ec-d85e28a60318 (Handle: 9): Unknown (notify,write)
    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 11): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
[Service] 0000fee7-0000-1000-8000-00805f9b34fb (Handle: 12): Tencent Holdings Limited
  [Characteristic] 0000fec7-0000-1000-8000-00805f9b34fb (Handle: 13): Apple: Inc. (write)
  [Characteristic] 0000fec8-0000-1000-8000-00805f9b34fb (Handle: 15): Apple: Inc. (indicate)
    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 17): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
  [Characteristic] 0000fec9-0000-1000-8000-00805f9b34fb (Handle: 18): Apple: Inc. (read), Value: bytearray(b'')
[Service] 0000ff80-0000-1000-8000-00805f9b34fb (Handle: 20): BMS? (Vendor specific)
  [Characteristic] 0000ff82-0000-1000-8000-00805f9b34fb (Handle: 21): Vendor specific (write-without-response,write), Max write w/o rsp size: 182
  [Characteristic] 0000ff81-0000-1000-8000-00805f9b34fb (Handle: 23): Vendor specific (notify)
    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 25): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
[Service] 0000180a-0000-1000-8000-00805f9b34fb (Handle: 26): Device Information
  [Characteristic] 00002a29-0000-1000-8000-00805f9b34fb (Handle: 27): Manufacturer Name String (read), Value: bytearray(b'ISSC')
  [Characteristic] 00002a24-0000-1000-8000-00805f9b34fb (Handle: 29): Model Number String (read), Value: bytearray(b'BT5050')
  [Characteristic] 00002a27-0000-1000-8000-00805f9b34fb (Handle: 31): Hardware Revision String (read), Value: bytearray(b'5050_SPP')
  [Characteristic] 00002a26-0000-1000-8000-00805f9b34fb (Handle: 33): Firmware Revision String (read), Value: bytearray(b'2030030')
[Service] 0000ff00-0000-1000-8000-00805f9b34fb (Handle: 35): Vendor specific
  [Characteristic] 0000ff02-0000-1000-8000-00805f9b34fb (Handle: 36): Vendor specific (write-without-response,write), Max write w/o rsp size: 182
  [Characteristic] 0000ff01-0000-1000-8000-00805f9b34fb (Handle: 38): Vendor specific (notify)
    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 40): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
  [Characteristic] 0000ff03-0000-1000-8000-00805f9b34fb (Handle: 41): Vendor specific (notify)
    [Descriptor] 00002905-0000-1000-8000-00805f9b34fb (Handle: 43): Characteristic Aggregate Format, Value: bytearray(b'\x00\x00\x00\x00\x00\x00\

    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 44): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
"""
# Windows test: There are no service UUIDs.

import asyncio
from types import TracebackType

try:
    from bleak import BleakScanner, BleakClient
except ModuleNotFoundError as mnfe:
    from sys import stderr
    print("Your environment is missing bleak (bluetooth low-energy (BLE) library). Suggestion (mind your venv etc.): python3 -m pip install 'bleak'", file=stderr,)
    raise mnfe
import re
import typing

from peripage import PrinterType
from bleak.backends.device import BLEDevice
from abc import abstractmethod

UART_SERVICE_UUID           = '49535343-fe7d-4ae5-8fa9-9fafd205e455'
# template said: "00002a37-0000-1000-8000-00805f9b34fb"
TX_CHARACTERISTIC_UUID      = '49535343-8841-43f4-a8d4-ecbe34729bb3'
RX_CHARACTERISTIC_UUID      = '49535343-1e4d-4bd9-ba61-23c647249616'
TX_SYNC_CHARACTERISTIC_UUID = '49535343-6daa-4d02-abf6-19569aca69fe'

from peripage import PeripagePrinter
class PeripageBleakPrinter(PeripagePrinter):

    def __init__(self, mac: str, printer_type: PrinterType, timeout: float=1.0,):
        super().__init__(mac, printer_type, timeout,)
        self.client: BleakClient = None
        # preallocate to ensure real-time behaviour of rx_notification_handler #prematureoptimization
        self.rx_data = [None]
        self.rx_data.clear()

    def rx_notification_handler(self, sender: int, data: bytearray,):
        self.rx_data.append(data)
        print(f"Received from {sender}: {data}")

    @abstractmethod
    async def discover_devices(cls, address=None,) -> BLEDevice:
        printer: BLEDevice = None
        if address is None:
            """Discover (probably) compatible devices"""
            peripage_matcher = re.compile("PeriPage_...._BLE")
            for d in await BleakScanner.discover():
                if d.name is not None and peripage_matcher.fullmatch(d.name):
                    print(f"""Found: {d.address} "{d.name}" """)
                    if input(f"""Use {d.name} [y] or find other devices [any]?""") == 'y':
                        printer = d
                        break
                else:
                    print(f"""Unknown device: {d.address} "{d.name}" """)
        else:
            printer = BLEDevice(address, None, None,)
        if printer is not None:
            """List available services"""
            async with BleakClient(printer.address,) as client:
                print(f"Connected: {client.is_connected}")
                print(client)
                print(dir(client))
                for service in client.services:
                    print(service)
                    print(dir(service))
                    for character in service.characteristics:
                        print(character)
                        print(dir(character))
                # Writing data
                #await client.write_gatt_char(CHARACTERISTIC_UUID, b"Hello World")

                # Reading data
                #data = await client.read_gatt_char(CHARACTERISTIC_UUID)
                #print(data)
        else:
            print("Printer not found.")
        return printer

    def isConnected(self) -> bool:
        """
        Check if printer is connected (socket alive)
        """

        try:
            return self.client is not None and self.client.is_connected()
        except:
            return False

    async def _notifier_subscribe(self):
        await self.client.start_notify(RX_CHARACTERISTIC_UUID, self.rx_notification_handler,)

    async def _notifier_unsubscribe(self):
        await self.client.stop_notify(RX_CHARACTERISTIC_UUID)

    async def connect(self) -> bool:
        """
        Open a new connection to the printer without checking for existing
        connection. In case of malfunction and/or twice connecting to the same
        printer, socket descriptor becomes unoperateable.

        Automatically sends a reset command. (Firmware internals: In order to
        make printer operate normally, it is required to call `reset()` after
        connecting.)
        """
        if self.client is not None:
            print("Client already connected", file=stderr,)
            return False
        # pucgenie: Can't use services=[UART_SERVICE_UUID,], because the UUID is not fixed.
        self.client = BleakClient(self.mac,)
        await self.client.connect()
        await self._notifier_subscribe()
        await self.reset()
        if self.printer_type is None:
            self.serial_number = await self.getDeviceSerialNumber()
            self.guess_printer_type()
        return True

    async def disconnect(self) -> None:
        """
        Disconnect from the printer.
        """

        if self.isConnected():
            await self._notifier_unsubscribe()
            await self.client.disconnect()
            self.client = None

    def setTimeout(self, timeout,) -> None:
        """
        Set the bluetooth socket connection recv / send timeout.
        """

        self.timeout = timeout

    async def tellPrinter(self, byteseq: bytes,) -> None:
        """
        Send `bytes` to the printer without response.

        Arguments:
        * `byteseq` - `bytes` data
        """

        await self.client.write_gatt_char(TX_CHARACTERISTIC_UUID, byteseq, False,)

    async def askPrinter(self, byteseq: bytes, recv_size: int=1024,) -> list[bytes]:
        """
        Send `bytes` to the printer with response.

        Arguments:
        * `recv_size` - max size of received chunk
        * `byteseq` - `bytes` data
        """
        #await self._notifier_unsubscribe()
        if len(self.rx_data) > 0:
            print(f"Dropped RX data segments: {len(self.rx_data)}")
        self.rx_data.clear()

        await self.client.write_gatt_char(TX_SYNC_CHARACTERISTIC_UUID, byteseq, True,)
        await asyncio.sleep(self.timeout)

        #await self._notifier_subscribe()
        ret = self.rx_data

        self.rx_data = [None]
        self.rx_data.clear()

        return ret

    def listenPrinter(self) -> list[bytes]:
        """
        Receive data from printer.

        Arguments:
        * `recv_size` - max size of received chunk
        """

        return self.rx_data
