# Tests for Group class


import pytest
import sys
from simframe import Frame
from simframe import Integrator
from simframe import writers
from simframe.frame import Heartbeat


def test_group_repr_str():
    f = Frame()
    assert isinstance(repr(f), str)
    assert isinstance(str(f), str)
    f.addintegrationvariable("x", 0)
    f.addfield("Y", 1.)
    f.addfield("abcdefghijklm", 0.)
    f.addgroup("A")
    f.addgroup("BCDEFGHIJKLMN")
    f.C = None
    f.abcdef1234567 = None
    f.A.addfield("k", 0.)
    assert isinstance(repr(f), str)
    assert isinstance(str(f), str)
    assert isinstance(repr(f.A), str)
    assert isinstance(str(f.A), str)
    f.integrator = Integrator(f.x)
    f.writer = writers.namespacewriter()
    assert isinstance(repr(f), str)
    assert isinstance(str(f), str)


def test_group_change_constant_field():
    f = Frame()
    f.addfield("Y", 0, constant=True)
    with pytest.raises(RuntimeError):
        f.Y = 1


def test_group_updateorder():
    f = Frame()
    f.addfield("x", 1.)
    f.addfield("y", 2.)
    with pytest.raises(RuntimeError):
        f.updateorder = ["x", "y"]
    assert f.updateorder == None
    with pytest.raises(ValueError):
        f.updater = ["x", None]
    with pytest.raises(RuntimeError):
        f.updater = ["x", "z"]
    f.updater = ["y", "x"]
    assert f.updateorder == ["y", "x"]
    assert repr(f.updater.updater._func) == "list_updater"

    def upd_x(f):
        return f.x * f.y

    def upd_y(f):
        return f.x + f.y

    f.x.updater = upd_x
    f.y.updater = upd_y
    f.update()
    assert f.x == 3.
    assert f.y == 3.

    def upd(f):
        f.y.update()
        f.x.update()

    f.updater = Heartbeat(upd)
    f.update()
    assert f.x == 18.
    assert f.y == 6.


def test_group_toc():
    f = Frame()
    f.addgroup("A")
    f.addfield("x", 1.)
    f.toc
    f.toc = None


def test_group_memory_usage():
    f = Frame()
    f.addgroup("A")
    f.addfield("x", 1.)
    version = sys.version_info
    if version.major == 3 and version.minor == 11:
        mem = 181.
    elif version.major == 3 and version.minor >= 12:
        mem = 157.
    else:
        mem = 197.
    assert f.memory_usage() == mem
    assert f.memory_usage(skip_hidden=True) == 8.
    f.memory_usage(print_output=True)
