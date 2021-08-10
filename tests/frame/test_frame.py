# Test for Frame class


import numpy as np
import pytest
from simframe import Frame
from simframe import Integrator
from simframe.io import Progressbar


def test_frame_attributes():
    f = Frame()
    with pytest.raises(TypeError):
        f.integrator = 1
    with pytest.raises(TypeError):
        f.progressbar = 1
    f.progressbar = Progressbar()
    with pytest.raises(TypeError):
        f.verbosity = "_"
    with pytest.raises(TypeError):
        f.writer = "_"


def test_frame_run():
    f = Frame()
    f.verbosity = 0
    f.addintegrationvariable("x", 0.)
    with pytest.raises(RuntimeError):
        f.run()
    f.integrator = Integrator(f.x)
    f.integrator._var = None
    with pytest.raises(RuntimeError):
        f.run()
    f.integrator = Integrator(f.x)
    with pytest.raises(RuntimeError):
        f.run()
    f.x = 3.
    f.x.snapshots = [1., 2.]
    with pytest.raises(RuntimeError):
        f.run()

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x = 1.5
    f.run()
    assert np.all(f.x == 2.)
