from simframe.integration.scheme import Scheme

# Butcher coefficients
a10 = 1/3
a20 = -1/3
b0, b1, b2, b3 = 1/8, 3/8, 3/8, 1/8
c1, c2 = 1/3, 2/3


def _f_expl_4_38rule(x0, Y0, dx, *args, dYdx=None, **kwargs):
    """Explicit 4th-order 3/8 rule method

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
     1/3 | 1/3  0   0   0
     2/3 |-1/3  1   0   0
      1  |  1  -1   1   0
    -----|-----------------
         | 1/8 3/8 3/8 1/8
    """

    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0 * dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + (a20*k0 + k1)*dx)
    k3 = Y0.derivative(x0 + dx, Y0 + (k0 - k1 + k2)*dx)

    return dx*(b0*k0 + b1*k1 + b2*k2 + b3*k3)


expl_4_38rule = Scheme(
    _f_expl_4_38rule, description="Explicit 4th-order 3/8 rule method")
