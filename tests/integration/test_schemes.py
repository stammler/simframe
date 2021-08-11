# Tests for the different integration schemes


import numpy as np
import pytest
from simframe import Frame
from simframe import Instruction
from simframe import Integrator
from simframe import schemes


def test_expl_1_euler():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_1_euler, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 2.656139888758694e-05)


def test_expl_2_fehlberg_adaptive():
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
    f.x.suggest(0.1)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_2_fehlberg_adptv,
                    f.Y, controller={"eps": 1.e-3})
    ]

    f.run()
    assert np.allclose(f.Y, 7.911222877853164e-3)


def test_expl_2_heun_euler_adaptive():
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
    f.x.suggest(0.1)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_2_heun_euler_adptv,
                    f.Y, controller={"eps": 1.e-3})
    ]

    f.run()
    assert np.allclose(f.Y, 4.553150014598088e-05)


def test_expl_2_heun():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_2_heun, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.6222977814657625e-05)


def test_expl_2_midpoint():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_2_midpoint, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.6222977814657625e-05)


def test_expl_2_ralston():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_2_ralston, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.6222977814657625e-05)


def test_expl_3_bogacki_shampine_adptv():
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
    f.x.suggest(0.1)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_3_bogacki_shampine_adptv,
                    f.Y, controller={"eps": 1.e-5})
    ]

    f.run()
    assert np.allclose(f.Y, 4.539180330465722e-05)


def test_expl_3_gottlieb_shu_adptv():
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
    f.x.suggest(0.1)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_3_gottlieb_shu_adptv,
                    f.Y, controller={"eps": 1.e-4})
    ]

    f.run()
    assert np.allclose(f.Y, 4.5390485375346277e-05)


def test_expl_3_heun():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_3_heun, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.537943947598517e-05)


def test_expl_3_kutta():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_3_kutta, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.537943947598517e-05)


def test_expl_3_ralston():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_3_ralston, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.53794394759852e-05)


def test_expl_3_ssprk():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_3_ssprk, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.537943947598521e-05)


def test_expl_4_38rule():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_4_38rule, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.5400341016294825e-05)


def test_expl_4_ralston():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_4_ralston, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.540034080370188e-05)


def test_expl_4_runge_kutta():
    f = Frame()
    f.addfield("Y", 1.)

    def dYdx(f, x, Y):
        return -Y
    f.Y.differentiator = dYdx
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_4_runge_kutta, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.540034101629485e-05)


def test_expl_5_cash_karp_adptv():
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
    f.x.suggest(0.1)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_5_cash_karp_adptv,
                    f.Y, controller={"eps": 1.e-3})
    ]

    f.run()
    assert np.allclose(f.Y, 4.57114092616805e-05)


def test_expl_5_dormand_prince_adptv():
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
    f.x.suggest(0.1)

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.expl_5_dormand_prince_adptv,
                    f.Y, controller={"eps": 1.e-2})
    ]

    f.run()
    assert np.allclose(f.Y, 1.8016162079480785e-06)


def test_impl_1_euler_direct():
    f = Frame()
    f.addfield("Y", 1.)

    def jac(f, x):
        return np.array([-1.])
    f.Y.jacobinator = jac
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.impl_1_euler_direct, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 7.25657159014803e-05)


def test_impl_1_euler_gmres():
    f = Frame()
    f.addfield("Y", 1.)

    def jac(f, x):
        return np.array([-1.])
    f.Y.jacobinator = jac
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.impl_1_euler_gmres, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 7.256571590148018e-05)


def test_impl_1_euler_gmres_fail():
    f = Frame()
    f.addfield("Y", 1.)

    def jac(f, x):
        return np.array([-1.])
    f.Y.jacobinator = jac
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.impl_1_euler_gmres, f.Y,
                    controller={"gmres_opt": {"atol": 0., "tol": 1.e-18, "maxiter": 1}})
    ]

    with pytest.raises(StopIteration):
        f.run()


def test_impl_2_midpoint_direct():
    f = Frame()
    f.addfield("Y", 1.)

    def jac(f, x):
        return np.array([-1.])
    f.Y.jacobinator = jac
    f.addintegrationvariable("x", 0.)

    def dx(f):
        return 0.1
    f.x.updater = dx
    f.x.snapshots = [10.]

    f.integrator = Integrator(f.x)
    f.integrator.instructions = [
        Instruction(schemes.impl_2_midpoint_direct, f.Y)
    ]

    f.run()
    assert np.allclose(f.Y, 4.5022605238147066e-05)
