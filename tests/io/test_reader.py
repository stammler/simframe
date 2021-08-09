# Tests for the reader attribute

import numpy as np
from pathlib import Path
import pytest
import shutil
from simframe import Frame
from simframe import Instruction
from simframe import Integrator
from simframe import schemes
from simframe import writers
from simframe.io import Reader
from simframe.io import Writer


def test_reader_attributes():
    def f():
        pass
    string = "test"
    writer = Writer(f)
    reader = Reader(writer)
    with pytest.raises(ValueError):
        reader.description = 1
    reader.description = string
    assert reader.description == string
    assert isinstance(repr(reader), str)
    assert isinstance(str(reader), str)
    with pytest.raises(NotImplementedError):
        reader.output(string)
    with pytest.raises(NotImplementedError):
        reader.sequence(string)


def test_not_implemented_functions():
    def f():
        pass
    string = "test"
    writer = Writer(f)
    reader = Reader(writer)
    assert isinstance(repr(reader), str)
    assert isinstance(str(reader), str)
    with pytest.raises(NotImplementedError):
        reader.output(string)
    with pytest.raises(NotImplementedError):
        reader.sequence(string)


def test_simple_read_files():
    f = Frame()
    f.addgroup("A")
    f.A.addfield("B", [0., 0.])
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 1.
    f.x.updater = dx
    f.x.snapshots = [1.]
    f.integrator = Integrator(f.x)
    f.integrator.instructions = [Instruction(schemes.expl_1_euler, f.Y)]
    f.writer = writers.hdf5writer
    print("datadir:", f.writer.datadir)
    f.run()
    x = f.writer.read.sequence("x")
    assert np.all(x == [0., 1.])
    Y = f.writer.read.sequence("Y")
    assert np.all(Y == [1., 0.])
    B = f.writer.read.sequence("A.B")
    assert np.all(B == [0., 0.])
    data = f.writer.read.all()
    shutil.rmtree(f.writer.datadir)
    with pytest.raises(RuntimeError):
        f.writer.datadir = "temp"
        f.writer.read.all()
    f.writer.datadir = "data"
