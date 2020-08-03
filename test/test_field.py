import numpy as np
from simframe import Frame
from simframe.frame import Field
from simframe.frame import Updater

import pytest

def test_field():

    sim = Frame()

    # Adding field to frame
    sim.addfield("a", 0)
    assert isinstance(sim.a, Field)
    assert sim.a == 0

    # Assigning value
    assert (sim.a + 1) == 1
    with pytest.raises(ValueError):
        sim.a = "string"
    with pytest.raises(ValueError):
        sim.a = np.empty(5)
    # Note: The ValueError here comes from NumPy. It tries to assign a value before type checking.
    # Therefore we have to reset sim.a to make sure it has the correct value afterwards.
    sim.a = 0

    # Adding updater by using a function
    def increment(sim):
        return sim.a + 1
    sim.a.updater = increment
    assert isinstance(sim.a.updater, Updater)
    sim.a.update()
    assert sim.a == 1

    # Adding updater by using an updater.
    u = Updater(increment)
    sim.a.updater = u
    assert isinstance(sim.a.updater, Updater)
    sim.a.update()
    assert sim.a == 2

    # Adding a list to updater, which has to fail for fields
    sim.a.updater = []
    assert isinstance(sim.a.updater, list)
    with pytest.raises(ValueError):
        sim.a.update()

    # Adding keyword arguments to updater
    def increment_kwargs(sim, val=0):
        return sim.a + 1 + val
    sim.a.updater = increment_kwargs
    sim.a.update()
    assert sim.a == 3
    sim.a.update(val=1)
    assert sim.a == 5

    # Make sure that constant fields do not get updated
    sim.a.constant = True
    assert sim.a.constant
    with pytest.raises(RuntimeError):
        sim.a = 0
    with pytest.raises(RuntimeError):
        sim.a.update()