# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

from typing import Any, BinaryIO

from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtCore import QProcess

from vimiv import api
from vimiv.utils import log

_logger = log.module_logger(__name__)


def test_cr2(header: bytes, _f: BinaryIO) -> bool:
    return header[:2] in (b"II", b"MM") and header[8:10] == b"CR"


def load_cr2(path) -> QPixmap:
    """Extract the thumbnail from the image and initialize QPixmap"""

    process = QProcess()
    process.start(f"dcraw -e -c {path}")
    process.waitForFinished()

    if process.exitStatus() != QProcess.NormalExit or process.exitCode() != 0:
        stderr = process.readAllStandardError()
        raise ValueError(f"Error calling dcraw: '{stderr.data().decode()}'")

    handler = QImageReader(process, "jpeg".encode())
    handler.setAutoTransform(True)

    process.closeWriteChannel()
    process.terminate()

    # Extract QImage from QImageReader and convert to QPixmap
    pixmap = QPixmap()
    pixmap.convertFromImage(handler.read())

    return pixmap


def test_cr3(header: bytes, _f: BinaryIO) -> bool:
    return header[4:8] == b"ftyp" and header[8:11] == b"crx" and header[16:24] == b"crx isom" and header[28:32] == b"moov"


def load_cr3(path) -> QPixmap:
    """Extract the thumbnail from the image and initialize QPixmap"""

    process = QProcess()
    process.start(f"exiftool -b -JpgFromRaw -w! /tmp/vimiv-RawPrev%d%F.jpg -q -execute -tagsfromfile @ -srcfile /tmp/vimiv-RawPrev{path}.jpg -overwrite_original -common_args {path}")
    process.waitForFinished()

    if process.exitStatus() != QProcess.NormalExit or process.exitCode() != 0:
        stderr = process.readAllStandardError()
        raise ValueError(f"Error calling exiftool: '{stderr.data().decode()}'")

    # TODO reuse process
    process = QProcess()
    process.start(f"cat /tmp/vimiv-RawPrev/{path}.jpg")
    process.waitForFinished()

    if process.exitStatus() != QProcess.NormalExit or process.exitCode() != 0:
        stderr = process.readAllStandardError()
        raise ValueError(f"Error calling cat: '{stderr.data().decode()}'")

    handler = QImageReader(process, "jpeg".encode())
    handler.setAutoTransform(True)

    process.closeWriteChannel()
    process.terminate()

    # Extract QImage from QImageReader and convert to QPixmap
    pixmap = QPixmap()
    pixmap.convertFromImage(handler.read())

    return pixmap


def init(info: str, *_args: Any, **_kwargs: Any) -> None:
    """Setup RawPrev plugin by adding the raw handler"""
    api.add_external_format("cr2", test_cr2, load_cr2)
    api.add_external_format("cr3", test_cr3, load_cr3)

    _logger.debug("Initialized RawPrev")
