# Tests for formatting utility function

import pytest
from simframe.utils.format import byteformat


def test_negative():
    with pytest.raises(ValueError):
        byteformat(-1.)


def test_small_values():
    assert byteformat(0.1) == "    < 1   B"


def test_colors():
    assert byteformat(12_000_000).startswith("\033[93m")
    assert byteformat(120_000_000).startswith("\033[91m")
