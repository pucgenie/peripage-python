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
def printImage(self, img: PIL.Image.Image, delay=0.01, resample=PIL.Image.Resampling.NEAREST) -> list[str]:
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

    if img.mode != "L":
        img = img.convert('L')
    img = PIL.ImageOps.invert(img)
    if img.size[0] != self.getRowWidth():
        img = img.resize((self.getRowWidth(), int(self.getRowWidth() / img.size[0] * img.size[1])), resample)
        warnings.append('RESIZED')
    img = img.convert('1')

    imgbytes = img.tobytes()
    self.printImageBytes(imgbytes, delay=delay)
    return warnings

@add_method(PeripagePrinter)
def printImageIterator(self, imgiterator: typing.Iterable[PIL.Image.Image], delay: float=0.01):
    """
    Iterate over iterator and print out each PIL Image that it returns.

    Arguments:
    * `rowiterator` - iterator that returns list[bytes].
    * `delay` - delay between printing each row of the image.
    """

    for img in imgiterator:
        self.printImage(img, delay=delay)

@add_method(PeripagePrinter)
def printQR(self, text: str, delay: float=0.01, resample=PIL.Image.Resampling.NEAREST) -> None:
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
    self.printImage(qrcode.make(text, border=0), delay=delay, resample=resample)
