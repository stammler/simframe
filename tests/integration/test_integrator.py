# Test of Integrator class


import pytest
from simframe import Frame
from simframe import Integrator
from simframe import schemes
from simframe.frame import Field
from simframe.frame import Heartbeat
from simframe.frame import IntVar


def test_integrator_repr_str():
    f = Frame()
    iv = IntVar(f, 0)
    i = Integrator(iv)
    assert isinstance(repr(i), str)
    assert isinstance(str(i), str)


def test_integrator_attributes():
    f = Frame()
    iv = IntVar(f, 0)
    i = Integrator(iv)
    with pytest.raises(TypeError):
        i.description = 1
    with pytest.raises(TypeError):
        i.maxit = "_"
    with pytest.raises(ValueError):
        i.maxit = 0
    with pytest.raises(TypeError):
        i.var = 1
    hb = Heartbeat()
    i.preparator = hb
    assert i.preparator == hb
    i.finalizer = hb
    assert i.finalizer == hb
    i.failop = hb
    assert i.failop == hb
    with pytest.raises(TypeError):
        i.instructions = 1
    with pytest.raises(TypeError):
        i.instructions = [1]
