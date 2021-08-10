# Tests for Color class


import pytest
from simframe.utils import Color


def test_color_call_none():
    c = Color()
    string = "test"
    assert c(string) == "\033[0m" + string + "\033[0m"


def test_color_color_not_existing():
    c = Color()
    string = "test"
    with pytest.raises(ValueError):
        c(string, color="_")


def test_color_set_color():
    c = Color()
    color = "blue"
    with pytest.raises(ValueError):
        c.color = "_"
    c.color = color
    assert c.color == color
