from simframe.integration.scheme import Scheme

# Butcher coefficients
a10 = 1/2
a21 = 1/2
b0, b1, b2, b3 = 1/6, 1/3, 1/3, 1/6
c1, c2 = 1/2, 1/2


def _f_expl_4_runge_kutta(x0, Y0, dx, *args, dYdx=None, **kwargs):
    """Explicit 4th-order classical Runge-Kutta method

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
      0  |  0   0   0   0
     1/2 | 1/2  0   0   0
     1/2 |  0  1/2  0   0
      1  |  0   0   1   0
    -----|-----------------
         | 1/6 1/3 1/3 1/6
    """

    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0*dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + a21*k1*dx)
    k3 = Y0.derivative(x0 + dx, Y0 + k2*dx)

    return dx*(b0*k0 + b1*k1 + b2*k2 + b3*k3)


expl_4_runge_kutta = Scheme(
    _f_expl_4_runge_kutta, description="Explicit 4th-order classical Runge-Kutta method")
