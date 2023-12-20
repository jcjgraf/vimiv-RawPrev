# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

from functools import lru_cache
from typing import Any, BinaryIO

from vimiv import api
from vimiv.qt.gui import QPixmap, QImageReader
from vimiv.qt.core import QProcess
from vimiv.utils import log

_logger = log.module_logger(__name__)


def test_raf(header: bytes, _f: BinaryIO) -> bool:
    return header[:15] == b"FUJIFILMCCD-RAW"


def test_cr2(header: bytes, _f: BinaryIO) -> bool:
    return header[:2] in (b"II", b"MM") and header[8:10] == b"CR"


def test_orf(header: bytes, _f: BinaryIO) -> bool:
    return header[:4] == b"IIRO"


@lru_cache(maxsize=40)
def load_cr2(path) -> QPixmap:
    """Extract the thumbnail from the image and initialize QPixmap"""

    process = QProcess()
    process.start("dcraw", ["-e", "-c", path])

    if not process.waitForFinished():
        _logger.error(f"Process exited with code {process.exitCode()}")
        raise OSError("Error waiting for process")

    if (
        process.exitStatus() != QProcess.ExitStatus.NormalExit
        or process.exitCode() != 0
    ):
        _logger.error(f"Process exited with code {process.exitCode()}")
        stderr = process.readAllStandardError()
        raise OSError(f"Error calling dcraw: '{stderr.data().decode()}'")

    handler = QImageReader(process, "jpeg".encode())
    handler.setAutoTransform(True)

    process.closeWriteChannel()
    process.terminate()

    # Extract QImage from QImageReader and convert to QPixmap
    pixmap = QPixmap()
    pixmap.convertFromImage(handler.read())

    return pixmap


def test_cr3(header: bytes, _f: BinaryIO) -> bool:
    return (
        header[4:8] == b"ftyp"
        and header[8:11] == b"crx"
        and header[16:24] == b"crx isom"
        and header[28:32] == b"moov"
    )


@lru_cache(maxsize=40)
def load_cr3(path) -> QPixmap:
    """Extract the thumbnail from the image and initialize QPixmap"""

    process = QProcess()
    process.start(
        "exiftool",
        [
            "-b",
            "-JpgFromRaw",
            "-w!",
            "/tmp/vimiv-RawPrev%d%F.jpg",
            "-q",
            "-execute",
            "-tagsfromfile",
            "@",
            "-srcfile",
            f"/tmp/vimiv-RawPrev{path}.jpg",
            "-overwrite_original",
            "-common_args",
            path,
        ],
    )

    if not process.waitForFinished():
        _logger.error(f"Process exited with code {process.exitCode()}")
        raise OSError("Error waiting for process")

    if (
        process.exitStatus() != QProcess.ExitStatus.NormalExit
        or process.exitCode() != 0
    ):
        _logger.error(f"Process exited with code {process.exitCode()}")
        stderr = process.readAllStandardError()
        raise OSError(f"Error calling exiftool: '{stderr.data().decode()}'")

    # TODO reuse process
    process = QProcess()
    process.start("cat", [f"/tmp/vimiv-RawPrev/{path}.jpg"])

    if not process.waitForFinished():
        _logger.error(f"Process exited with code {process.exitCode()}")
        raise OSError("Error waiting for process")

    if (
        process.exitStatus() != QProcess.ExitStatus.NormalExit
        or process.exitCode() != 0
    ):
        _logger.error(f"Process exited with code {process.exitCode()}")
        stderr = process.readAllStandardError()
        raise OSError(f"Error calling cat: '{stderr.data().decode()}'")

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
    api.add_external_format("raf", test_raf, load_cr2)
    api.add_external_format("cr2", test_cr2, load_cr2)
    api.add_external_format("cr3", test_cr3, load_cr3)
    api.add_external_format("orf", test_orf, load_cr2)

    _logger.debug("Initialized RawPrev")
