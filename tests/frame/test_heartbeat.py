# Tests for Heartbeat class


from _pytest.recwarn import T
import pytest
from simframe import Frame
from simframe.frame import Heartbeat
from simframe.frame import Updater


def test_heartbeat_repr_str():
    hb = Heartbeat()
    assert isinstance(repr(hb), str)
    assert isinstance(str(hb), str)


def test_heartbeat_attributes():
    hb = Heartbeat()
    with pytest.raises(TypeError):
        hb.diastole = 1
    with pytest.raises(TypeError):
        hb.systole = 1
    with pytest.raises(TypeError):
        hb.updater = 1
    upd = Updater()
    hb.diastole = upd
    assert hb.diastole == upd
    hb.systole = upd
    assert hb.systole == upd
    hb.updater = upd
    assert hb.updater == upd


def test_heartbeat_order():
    f = Frame()
    f.addfield("x", 1.)
    f.addfield("y", 2.)
    f.addfield("z", 3.)

    def sys(f):
        f.x = f.y * f.z

    def upd(f):
        f.y = f.z * f.x

    def dia(f):
        f.z = f.x * f.y

    f.updater = Heartbeat(updater=upd, systole=sys, diastole=dia)
    f.update()
    assert f.x == 6.
    assert f.y == 18.
    assert f.z == 108.
