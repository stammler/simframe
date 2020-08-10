from simframe import Frame
from simframe import Integrator
from simframe import writers
from simframe.frame import IntVar

import pytest


def test_frame_initialization():
    f = Frame()
    assert isinstance(f, Frame)


def test_frame_writer():
    f = Frame()
    assert f.writer is None
    with pytest.raises(TypeError):
        f.writer = "writer"
    f.writer = writers.hdf5writer
    assert f.writer is writers.hdf5writer
    f = Frame(writer=writers.hdf5writer)
    assert f.writer is writers.hdf5writer


def test_frame_integrator():
    f = Frame()
    assert f.integrator is None
    with pytest.raises(TypeError):
        f.integrator = "test"
    f.integrator = Integrator(IntVar(f, 0.))
    assert isinstance(f.integrator, Integrator)
    f = Frame(integrator=Integrator(IntVar(f, 0.)))
    assert isinstance(f.integrator, Integrator)
