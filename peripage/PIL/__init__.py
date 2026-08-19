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

"""
Enhances PeripagePrinter class 
"""

import PIL.Image
import PIL.ImageOps

def add_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        # pucgenie: Don't pollute our namespace.
        #return func # returning func means func can still be used normally
    return decorator

import typing
from .. import PeripagePrinter

@add_method(PeripagePrinter)
async def printImage(self: PeripagePrinter, img: PIL.Image.Image, delay: float=0.008, resample: PIL.Image.Resampling=PIL.Image.Resampling.NEAREST,) -> list[str]:
    """
    Print PIL Image on this printer with automatic internal to-blackwhite
    conversion.

    WARNING: In order to prevent the overhead of the printer (and possibly
    loose some data but to limitations of the in-printer buffer) it is
    suggested to split image into many vertical pieces and wait a
    reasonable amount of time to let the printer to cooldown.

    Arguments:
    * `img` - your pretty PIL Image.
    * `delay` - delay between printing each row of the image.
    * `resample` - resampling mode of the image, used to automatically
    rescale image to fit the printer width of `Printer.getRowWidth()`.

    Returns a list of str with all automagical, optional actions taken.
    """

    # logger-less feedback
    warnings = []

    if img.mode not in ["L", "1",]:
        img = img.convert('L')
    img = PIL.ImageOps.invert(img)
    if img.size[0] != self.getRowWidth():
        img = img.resize((self.getRowWidth(), int(self.getRowWidth() / img.size[0] * img.size[1])), resample)
        warnings.append('RESIZED')
    if img.mode != "1":
        # pucgenie: TODO: Double vertical grayscale resolution by also generating a row-by-row list of concentration (=saturation, contrast, heat) values. Rows containing edge-pixels only get lower concentration, all others get full concentration.
        img = img.convert('1')

    imgbytes = img.tobytes()
    await self.printImageBytes(imgbytes, delay=delay,)
    return warnings

@add_method(PeripagePrinter)
async def printImageIterator(self: PeripagePrinter, imgiterator: typing.Iterable[PIL.Image.Image], delay: float=0.008,):
    """
    Iterate over iterator and print out each PIL Image that it returns.

    Arguments:
    * `rowiterator` - iterator that returns list[bytes].
    * `delay` - delay between printing each row of the image.
    """

    for img in imgiterator:
        await self.printImage(img, delay=delay)

@add_method(PeripagePrinter)
async def printQR(self: PeripagePrinter, text: str, delay: float=0.008, resample=PIL.Image.Resampling.NEAREST,) -> None:
    """
    Generate a QR code from specified string and print it.

    Arguments:
    * `text` - your pretty text.
    * `delay` - delay between printing each row of the image.
    * `resample` - resampling mode of the image, used to automatically
    rescale image to fit the printer width of `Printer.getRowWidth()`.
    """
    # pucgenie: convenience functionality - don't break the whole driver if qrcode dependency is unavailable
    import qrcode
    await self.printImage(qrcode.make(text, border=0), delay=delay, resample=resample)
