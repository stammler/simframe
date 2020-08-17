from simframe.integration.scheme import Scheme

# Butcher coefficients
a10, a21 = 1/3, 2/3
c1, c2 = 1/3, 2/3
b0, b2 = 1/4, 3/4


def _f_expl_3_heun(x0, Y0, dx, *args, **kwargs):
    """Explicit 3rd-order Heun's method

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
      0  |  0   0   0
     1/3 | 1/3  0   0
     2/3 |  0  2/3  0
    -----|-------------
         | 1/4  0  3/4
    """
    k0 = Y0.derivative(x0, Y0)
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0*dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + a21*k1*dx)

    return Y0 + dx*(b0*k0 + b2*k2)


expl_3_heun = Scheme(
    _f_expl_3_heun, description="Explicit 3rd-order Heun's method")
