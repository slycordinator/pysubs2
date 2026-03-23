import multiprocessing
import itertools
import pytest

from pysubs2.exceptions import UnknownFormatIdentifierError, UnknownFileExtensionError, FormatAutodetectionError
from pysubs2.formats import get_format_class, get_format_identifier, get_file_extension, autodetect_format
from pysubs2.ssafile import SSAFile

def test_identifier_to_class() -> None:
    with pytest.raises(UnknownFormatIdentifierError) as exc_info:
        get_format_class("unknown-format-identifier")
    assert exc_info.value.format_ == "unknown-format-identifier"


def test_ext_to_identifier() -> None:
    with pytest.raises(UnknownFileExtensionError) as exc_info:
        get_format_identifier(".xyz")
    assert exc_info.value.ext == ".xyz"


def test_identifier_to_ext() -> None:
    with pytest.raises(UnknownFormatIdentifierError) as exc_info:
        get_file_extension("unknown-format-identifier")
    assert exc_info.value.format_ == "unknown-format-identifier"


def test_format_detection_fail() -> None:
    with pytest.raises(FormatAutodetectionError) as exc_info:
        autodetect_format("")
    assert not exc_info.value.formats


def _test_97_func(i: int, error: int) -> int:
    if i == 0:
        if error == 0:
            raise RuntimeError("Regular exception is properly handled by multiprocessing")
        elif error == 1:
            SSAFile.from_string("")
        else:
            assert False
    else:
        return i


@pytest.mark.timeout(5)
def test_97_format_detection_multiprocessing_error() -> None:
    # see issue #97
    with multiprocessing.Pool(4) as pool:
        with pytest.raises(RuntimeError):
            pool.starmap(_test_97_func, zip(range(4), itertools.repeat(0)))
        with pytest.raises(FormatAutodetectionError):
            pool.starmap(_test_97_func, zip(range(4), itertools.repeat(1)))
