from simframe.integration.scheme import Scheme

# Butcher coefficients
a10 = 1/2
a21 = 2.
b0, b1, b2 = 1/6, 2/3, 1/6
c1 = 1/2


def _f_expl_3_kutta(x0, Y0, dx, *args, **kwargs):
    """Explicit 3rd-order Kutta's method

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
     1/2 | 1/2  0   0
      1  | -1   2   0
    -----|-------------
         | 1/6 2/3 1/6
    """
    k0 = Y0.derivative(x0, Y0)
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0 * dx)
    k2 = Y0.derivative(x0 + dx, Y0 + (-k0 + a21*k1)*dx)

    return Y0 + dx*(b0*k0 + b1*k1 + b2*k2)


expl_3_kutta = Scheme(
    _f_expl_3_kutta, description="Explicit 3rd-order Kutta's method")
