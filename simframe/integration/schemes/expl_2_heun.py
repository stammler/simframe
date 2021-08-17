from simframe.integration.scheme import Scheme

# Butcher coefficients
a10 = 1.0
b0 = 0.5
b1 = 0.5
c1 = 1.0


def _f_expl_2_heun(x0, Y0, dx, *args, dYdx=None, **kwargs):
    """Explicit 2nd-order Heun's method

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
      0  |  0   0
      1  |  1   0
    -----|---------
         | 1/2 1/2
    """
    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0*dx)

    return dx*(b0*k0 + b1*k1)


class expl_2_heun(Scheme):
    """Class for explicit 2nd-order Heun's method"""

    def __init__(self, *args, **kwargs):
        super().__init__(_f_expl_2_heun,
                         description="Explicit 2nd-order Heun's method", *args, **kwargs)
