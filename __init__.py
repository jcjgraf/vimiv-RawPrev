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

    _logger.debug("Initialized RawPrev")
