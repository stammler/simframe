from simframe.integration.scheme import Scheme

# Butcher coefficients
a10 = 0.4
a20, a21 = 0.29697761,  0.15875964
a30, a31, a32 = 0.21810040, -3.05096516, 3.83286476
b0, b1, b2, b3 = 0.17476028, -0.55148066, 1.20553560, 0.17118478
c1, c2 = 0.4,  0.45573725


def _f_expl_4_ralston(x0, Y0, dx, *args, dYdx=None, **kwargs):
    """Explicit 4th-order Ralston's method

    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
    dYdx : Field, optional, default : None
        Current derivative. Will be calculated, if not set.
    args : additional positional arguments
    kwargs : additional keyworda arguments

    Returns
    -------
    dY : Field
        Delta of variable to be integrated

    Butcher tableau
    ---------------
     0          | 0           0          0          0
     0.4        | 0.4         0          0          0
     0.45573725 | 0.29697761  0.15875964 0          0
     1          | 0.21810040 -3.05096516 3.83286476 0
    ------------|----------------------------------------------
                | 0.17476028 -0.55148066 1.20553560 0.17118478
    """

    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0 * dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + (a20*k0 + a21*k1)*dx)
    k3 = Y0.derivative(x0 + dx, Y0 + (a30*k0 + a31*k1 + a32*k2)*dx)

    return dx*(b0*k0 + b1*k1 + b2*k2 + b3*k3)


expl_4_ralston = Scheme(
    _f_expl_4_ralston, description="Explicit 4th-order Ralston's method")
