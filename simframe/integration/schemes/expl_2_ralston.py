from simframe.integration.scheme import Scheme

# Butcher coefficients
a10 = 2/3
b0, b1 = 1/4, 3/4
c1 = 2/3


def _f_expl_2_ralston(x0, Y0, dx, *args, **kwargs):
    """Explicit 2nd-order Ralston's method

    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
    args : additional positional arguments
    kwargs : additional keyworda arguments

    Returns
    -------
    Y1 : Field
        New value of Y

    Butcher tableau
    ---------------
      0  |  0   0
     2/3 | 2/3  0
    -----|---------
         | 1/4 3/4
    """
    k0 = Y0.derivative(x0, Y0)
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0*dx)

    return Y0 + dx*(b0*k0 + b1*k1)


expl_2_ralston = Scheme(
    _f_expl_2_ralston, description="Explicit 2nd-order Ralston's method")
