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

import asyncio

try:
    from bleak import BleakScanner, BleakClient
except ModuleNotFoundError as mnfe:
    from sys import stderr
    print("Your environment is missing pybluez. Suggestion (mind your venv etc.): python3 -m pip install 'pybluez[ble]'", file=stderr,)
    raise mnfe
import re
import typing

class BluetoothDevice(typing.NamedTuple):
    address: str  # Die Bluetooth-MAC-Adresse (z. B. "00:11:22:33:FF:EE")
    name: str

CHARACTERISTIC_UUID = '49535343-8841-43f4-a8d4-ecbe34729bb3' # template said: "00002a37-0000-1000-8000-00805f9b34fb"

async def main(address=None,):
    printer = None
    if address is None:
        devices = await BleakScanner.discover()
        peripage_matcher = re.compile("PeriPage_...._BLE")
        for d in devices:
            if d.name is not None and peripage_matcher.fullmatch(d.name):
                print(f"""Found: {d.address} "{d.name}" """)
                printer = d
    else:
        printer = BluetoothDevice(address, None,)
    if printer is not None:
        async with BleakClient(printer.address, services=['49535343-fe7d-4ae5-8fa9-9fafd205e455', CHARACTERISTIC_UUID,],) as client:
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

asyncio.run(main(address='C0:15:83:15:1F:78'))


def notification_handler(sender: int, data: bytearray):
    print(f"Received from {sender}: {data}")

async def subscribe(address):
    async with BleakClient(address) as client:
        # Subscribe to updates
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        # Keep the script running to receive data
        await asyncio.sleep(60.0) 
        await client.stop_notify(CHARACTERISTIC_UUID)


from peripage import AbstractPrinter
class PeripageBleakPrinter(AbstractPrinter):

    def isConnected(self) -> bool:
        """
        Check if printer is connected (socket alive)
        """

        try:
            self.sock.getpeername()
            return True
        except:
            return False

    def connect(self) -> None:
        """
        Open a new connection to the printer without checking for existing
        connection. In case of malfunction and/or twice connecting to the same
        printer, socket descriptor becomes unoperateable.

        In order to make printer operate normally, it is required to call
        `reset()` after connecting.
        """

        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.mac, 1))
        self.sock.settimeout(self.timeout)

    def reconnect(self) -> None:
        """
        Reconnect to the printer with existing connection check.

        In order to make printer operate normally, it is required to call
        `reset()` after connecting.
        """

        if self.isConnected():
            # self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            del self.sock

        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.mac, 1))
        self.sock.settimeout(self.timeout)

    def disconnect(self) -> None:
        """
        Disconnect from the printer.
        """

        if self.isConnected():
            # self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            del self.sock

    def setTimeout(self, timeout) -> None:
        """
        Set the bluetooth socket connection recv / send timeout.
        """

        self.timeout = timeout
        if self.isConnected():
            self.sock.settimeout(timeout)

    def tellPrinter(self, byteseq: bytes) -> None:
        """
        Send `bytes` to the printer without response.

        Arguments:
        * `byteseq` - `bytes` data
        """

        self.sock.send(byteseq)

    def askPrinter(self, byteseq: bytes, recv_size: int=1024) -> bytes:
        """
        Send `bytes` to the printer with response.

        Arguments:
        * `recv_size` - max size of received chunk
        * `byteseq` - `bytes` data
        """

        self.sock.send(byteseq)
        return self.sock.recv(recv_size)

    def listenPrinter(self, recv_size: int=1024) -> bytes:
        """
        Receive data from printer.

        Arguments:
        * `recv_size` - max size of received chunk
        """

        return self.sock.recv(recv_size)

    def tellPrinterSeq(self, byteseq: typing.Iterable[bytes]) -> None:
        """
        Send list of `bytes` to the printer without response.

        Arguments:
        * `byteseq` - `list` of `bytes`
        """

        for s in byteseq:
            self.sock.send(s)

    def askPrinterSeq(self, byteseq: typing.Iterable[bytes], recv_size: int=1024) -> bytes:
        """
        Send list of `bytes` to the printer with response.

        Arguments:
        * `recv_size` - max size of received chunk
        * `byteseq` - `list` of `bytes`
        """

        for s in byteseq:
            self.sock.send(s)
        return self.sock.recv(recv_size)