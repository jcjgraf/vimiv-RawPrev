# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

import subprocess
from typing import Any, BinaryIO

from PyQt5.QtGui import QPixmap

from vimiv import api
from vimiv.utils import log, files

_logger = log.module_logger(__name__)


def test_cr2(header: bytes, _f: BinaryIO) -> bool:
    return header[:2] in (b"II", b"MM") and header[8:10] == b"CR"


def load_cr2(path):
    """Extract the thumbnail from the image and initialize QPixmap"""
    output = subprocess.run(
        ["dcraw", "-e", "-c", path], capture_output=True, check=True
    )
    pixmap = QPixmap()
    pixmap.loadFromData(output.stdout)

    return pixmap


def init(info: str, *_args: Any, **_kwargs: Any) -> None:
    """Setup RawPrev plugin by adding the raw handler"""
    api.add_external_format("cr2", test_cr2, load_cr2)

    _logger.debug("Initialized RawPrev")
