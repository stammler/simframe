# Tests for the namespace writer


import numpy as np
import pytest
from simframe import Frame
from simframe import Instruction
from simframe import Integrator
from simframe import schemes
from simframe import writers


def test_namespacewriter_attributes():
    writer = writers.namespacewriter
    assert isinstance(repr(writer), str)
    assert isinstance(str(writer), str)


def test_namespacewriter_getfilename():
    writer = writers.namespacewriter
    assert writer._getfilename() == None


def test_namespacewriter_simple():
    f = Frame()
    f.addfield("Y", 1.)
    f.addgroup("A")
    f.A.addfield("B", 0.)

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
    f.writer = writers.namespacewriter
    f.run()
    Y = f.writer.read.sequence("Y")
    assert np.all(Y == [1., 0.])
    x = f.writer.read.sequence("x")
    assert np.all(x == [0., 1.])
    data = f.writer.read.all()
    assert np.all(data.Y == [1., 0.])
    assert np.all(data.x == [0., 1.])
    f.writer.reset()


def test_namespacewriter_read_empty():
    f = Frame()
    f.addfield("Y", 1.)
    f.writer = writers.namespacewriter
    with pytest.raises(RuntimeError):
        Y = f.writer.read.sequence("Y")
    with pytest.raises(RuntimeError):
        data = f.writer.read.all()


def test_namespacewriter_read_out_of_bounds():
    f = Frame()
    f.addfield("Y", 1.)
    f.writer = writers.namespacewriter
    f.writer.verbosity = 0
    f.writer.dumping = False
    f.writer.write(f)
    with pytest.raises(RuntimeError):
        f.writer.read.output(1)
    data0000 = f.writer.read.output(0)
    assert data0000.Y == 1.
    f.writer.reset()


def test_namespacewriter_read_sequence():
    f = Frame()
    f.addfield("Y", [1., 0])
    f.addfield("x", 0, save=False)
    f.writer = writers.namespacewriter
    f.writer.write(f)
    with pytest.raises(TypeError):
        f.writer.read.sequence(1)
    with pytest.raises(RuntimeError):
        f.writer.read.sequence("x")
    Y = f.writer.read.sequence("Y")
    assert np.all(Y == [1., 0.])
    f.writer.reset()
