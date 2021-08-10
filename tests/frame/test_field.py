# Tests for Field class


import numpy as np
import pytest
from simframe import Frame
from simframe import Integrator
from simframe.frame import Field


def test_field_repr_str():
    f = Frame()
    fi = Field(f, [0., 0.])
    assert isinstance(repr(fi), str)
    assert isinstance(str(fi), str)
    fi = Field(f, 0., constant=True)
    assert isinstance(repr(fi), str)
    assert isinstance(str(fi), str)


def test_field_format():
    f = Frame()
    fi = Field(f, 1.26)
    assert "{:3.1f}".format(fi) == "1.3"
    fi = Field(f, [1, 2])
    assert "{}".format(fi) == "Field"


def test_field_attributes():
    f = Frame()
    fi = Field(f, 1.)
    with pytest.raises(TypeError):
        fi.constant = "_"
    with pytest.raises(TypeError):
        fi.save = "_"
    with pytest.raises(RuntimeError):
        fi.buffer = None


def test_field_set():
    f = Frame()
    f.addfield("Y", 0.)
    f.Y._setvalue(1.)
    assert f.Y == 1.
    f.Y.constant = True
    with pytest.raises(RuntimeError):
        f.Y._setvalue(0.)


def test_field_update():
    f = Frame()
    f.addfield("Y", 1.)

    def upd(f):
        return 0.
    f.Y.updater = upd
    f.Y.update()
    assert f.Y == 0.


def test_field_jacobian():
    f = Frame()
    f.addfield("Y", 1.)
    f.addintegrationvariable("x", 0.)

    def jac(f, x):
        if x == None:
            return 0.
        else:
            return x
    f.Y.jacobinator = jac
    with pytest.raises(RuntimeError):
        f.Y.jacobian()
    f.integrator = Integrator(f.x)
    f.integrator._var = None
    with pytest.raises(RuntimeError):
        f.Y.jacobian()
    f.integrator = Integrator(f.x)
    assert f.Y.jacobian() == 0.
    assert f.Y.jacobian(x=1.) == 1.


def test_field_derivative():
    f = Frame()
    f.addfield("Y", 1.)
    f.addintegrationvariable("x", 0.)

    def diff(f, x, Y):
        return -Y
    f.Y.differentiator = diff
    with pytest.raises(RuntimeError):
        f.Y.derivative()
    f.integrator = Integrator(f.x)
    f.integrator._var = None
    with pytest.raises(RuntimeError):
        f.Y.derivative()
    f.integrator = Integrator(f.x)
    assert np.all(f.Y.derivative() == -f.Y)
    f.addfield("Y", [1., 0])
    assert np.all(f.Y.derivative() == 0.)

    def jac(f, x):
        return [[2., 0], [0., 2.]]
    f.Y.jacobinator = jac
    assert np.all(f.Y.derivative() == [2., 0.])
