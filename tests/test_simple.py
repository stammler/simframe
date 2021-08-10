# This is the most simple case of a differential equation.
# Running this test already covers more than 50% of the code base.


import shutil
from simframe import Frame
from simframe import Instruction
from simframe import Integrator
from simframe import schemes
from simframe import writers


def test_simple():
    f = Frame()
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
    f.run()
    assert f.Y == 0.
    assert f.x.prevstepsize == 1.
