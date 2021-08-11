# This is a test case for integration with adaptive step sizes


import numpy as np
import pytest
from simframe import Frame
from simframe import Instruction
from simframe import Integrator
from simframe import schemes


def test_adaptive():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return f.x.suggested
    f.x.updater = dx
    f.x.snapshots = [10.]
    f.x.suggest(100.)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [Instruction(
        schemes.expl_5_cash_karp_adptv, f.Y)]

    f.run()
    assert f.Y == 5.34990702474703e-3


def test_adaptive_fail():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return f.x.suggested
    f.x.updater = dx
    f.x.snapshots = [10.]
    f.x.suggest(100.)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [Instruction(
        schemes.expl_5_cash_karp_adptv, f.Y)]
    f.integrator.maxit = 1

    with pytest.raises(StopIteration):
        f.run()


def test_adaptive_update():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return f.x.suggested
    f.x.updater = dx
    f.x.snapshots = [10.]
    f.x.suggest(100.)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [Instruction(schemes.expl_5_cash_karp_adptv, f.Y),
                                 Instruction(schemes.update, f.Y)]

    f.run()
    assert f.Y == 5.34990702474703e-3
