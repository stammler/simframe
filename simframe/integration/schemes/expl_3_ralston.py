from simframe.integration.scheme import Scheme

# Butcher coefficients
a10 = 1/2
a21 = 3/4
b0, b1, b2 = 2/9, 1/3, 4/9
c1, c2 = 1/2, 3/4


def _f_expl_3_ralston(x0, Y0, dx, *args, dYdx=None, **kwargs):
    """Explicit 3rd-order Ralston's method

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
      0  |  0   0   0
     1/2 | 1/2  0   0
     3/4 |  0  3/4  0
    -----|-------------
         | 2/9 1/3 4/9
    """
    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0*dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + a21*k1*dx)

    return dx*(b0*k0 + b1*k1 + b2*k2)


expl_3_ralston = Scheme(
    _f_expl_3_ralston, description="Explicit 3rd-order Ralston's method")
