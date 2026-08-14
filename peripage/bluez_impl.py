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

import typing

from peripage import PeripagePrinter, PrinterType

try:
    import bluetooth
except ModuleNotFoundError as mnfe:
    from sys import stderr
    print("Your environment is missing pybluez. Suggestion (mind your venv etc.): python3 -m pip install 'pybluez[ble]'", file=stderr,)
    raise mnfe

class PeripageBluezPrinter(PeripagePrinter):

    def __init__(self, mac: str, printer_type: PrinterType, timeout: float=1.0,):
        super(mac, printer_type, timeout,)

    def isConnected(self) -> bool:
        """
        Check if printer is connected (socket alive)
        """

        try:
            self.sock.getpeername()
            return True
        except:
            return False

    def connect(self) -> bool:
        """
        Open a new connection to the printer without checking for existing
        connection. In case of malfunction and/or twice connecting to the same
        printer, socket descriptor becomes unoperateable.

        In order to make printer operate normally, it is required to call
        `reset()` after connecting.
        """
        if self.isConnected():
            return False

        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.mac, 1))
        self.sock.settimeout(self.timeout)
        return True

    def reconnect(self) -> None:
        """
        Reconnect to the printer with existing connection check.

        In order to make printer operate normally, it is required to call
        `reset()` after connecting.
        """

        self.disconnect()

        self.connect()

    def disconnect(self) -> None:
        """
        Disconnect from the printer.
        """

        if not self.isConnected():
            return False
        # self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        del self.sock
        return True

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
