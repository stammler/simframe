from simframe import Frame
from simframe.frame import Field
from simframe.frame import Group
from simframe.frame import IntVar
from simframe.frame import Heartbeat

import pytest


def test_group_description():
    # Note Frame is sub-class of Group
    f = Frame()
    assert f.description == ""
    with pytest.raises(ValueError):
        f.description = None
    f.description = "description"
    assert f.description == "description"
    f = Frame(description="testframe")
    assert f.description == "testframe"


def test_group_updater_func():
    f = Frame()
    assert isinstance(f.updater, Heartbeat)
    f.A = 0
    f.update()
    assert f.A == 0

    def upd(f):
        f.A += 1
    f.updater = upd
    f.update()
    assert f.A == 1


def test_group_updater_list():
    f = Frame()
    f.A = 1
    f.addgroup("g1")
    f.addgroup("g2")
    f.addgroup("g3")

    def g1(f):
        f.A += 1

    def g2(f):
        f.A += 2

    def g3(f):
        f.A *= 3
    f.g1.updater = g1
    f.g2.updater = g2
    f.g3.updater = g3
    ls = ["g1", "g2", "g3"]
    f.updater = ls
    f.update()
    assert f.A == 12
    f.A = 1
    ls = ["g2", "g3", "g1"]
    f.updater = ls
    f.update()
    assert f.A == 10
    f.A = 1
    ls = ["g3", "g2", "g1"]
    f.updater = ls
    f.update()
    assert f.A == 6


def test_group_addgroup():
    f = Frame()
    f.addgroup("g")
    assert isinstance(f.g, Group)


def test_group_addfield():
    f = Frame()
    f.addfield("f", 0.)
    assert isinstance(f.f, Field)
    assert f.f == 0.


def test_group_addintvar():
    f = Frame()
    f.addintegrationvariable("i", 0.)
    assert isinstance(f.i, IntVar)
    assert f.i == 0
