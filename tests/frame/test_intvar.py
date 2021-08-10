# Tests for IntVar class


import pytest
from simframe import Frame
from simframe.frame import IntVar


def test_intvar_attributes():
    f = Frame()
    intv = IntVar(f, 1.)
    assert intv == 1.


def test_intvar_update():
    f = Frame()
    intv = IntVar(f, 1.)

    def dx(f):
        return 1.
    intv.updater = dx
    assert intv.update() == None
    assert intv == 1.


def test_intvar_suggest():
    f = Frame()
    intv = IntVar(f, 0.)
    with pytest.raises(RuntimeError):
        intv.suggested
    with pytest.raises(ValueError):
        intv.suggest(-1.)
    intv.suggest(1.)
    assert intv.suggested == 1.
    intv.suggest(2.)
    assert intv.suggested == 1.
    intv.suggest(2., reset=True)
    assert intv.suggested == 2.


def test_intvar_stepsize():
    f = Frame()
    intv = IntVar(f, 0.)
    intv._updater = None
    with pytest.raises(RuntimeError):
        intv.stepsize


def test_intvar_snapshots():
    f = Frame()
    intv = IntVar(f, 2.1)
    with pytest.raises(ValueError):
        intv.snapshots = [2., 1.]
    with pytest.raises(ValueError):
        intv.snapshots = [1., 1.]

    def dx(x):
        return 1.
    intv.updater = dx
    intv.snapshots = []
    with pytest.raises(ValueError):
        intv.nextsnapshot
    with pytest.raises(ValueError):
        intv.prevsnapshot
    intv.snapshots = [1., 2., 3.]
    assert intv.nextsnapshot == 3.
    assert intv.prevsnapshot == 2.
