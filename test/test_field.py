from simframe import Frame
from simframe.frame import Field

import numpy as np
import pytest


def test_field_creationcopy():
    A = np.ones(5)
    f = Frame()
    f.addfield("f", A)
    assert np.all(f.f == A)
    A *= 2
    assert np.all(f.f == np.ones(5))
    f.addfield("f", A, copy=False)
    assert np.all(f.f == A)
    A *= 2
    assert np.all(f.f == A)


def test_field_assignment():
    A = np.ones(5)
    B = np.ones(5) * 2.
    f = Frame()
    f.addfield("f", A)
    assert np.all(f.f == A)
    f.f = B
    assert isinstance(f.f, Field)
    assert np.all(f.f == B)
    B *= 2.
    assert not np.all(f.f == B)
    with pytest.raises(ValueError):
        f.f = 1
    f.addfield("f", 0)
    with pytest.raises(ValueError):
        f.f = "test"


def test_field_update():
    f = Frame()
    f.addfield("f", np.ones(5))
    f.update()
    assert np.all(f.f == np.ones(5))

    def upd(f):
        return 2. * f.f
    f.f.updater = upd
    f.f.update()
    assert np.all(f.f == 2. * np.ones(5))


def test_field_differentiator():
    f = Frame()
    f.addfield("f", np.ones(5))

    def upd(f, x, Y):
        return 2. * x * Y
    f.f.differentiator = upd
    assert np.all(f.f.derivative(x=2.) == 4. * np.ones(5))
