from simframe.integration.scheme import Scheme

import numpy as np

# Butcher coefficients
a10 = 1/2
a21 = 3/4
a30, a31, a32 = 2/9, 1/3, 4/9
b0, b1, b2 = 2/9, 1/3, 4/9
bs0, bs1, bs2, bs3 = 7/24, 1/4, 1/3, 1/8
e0, e1, e2, e3 = b0-bs0, b1-bs1, b2-bs2, -bs3
c1, c2 = 1/2, 3/4


def _f_expl_3_bogacki_shampine_adptv(x0, Y0, dx, *args, dYdx=None, econ=0.005832, eps=0.1, pgrow=-1/3, pshrink=-0.5, safety=0.9, **kwargs):
    """Explicit adaptive 3rd-order Bogacki-Shampine method

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
    econ : float, optional, default : 0.005832
        Error controll parameter for setting stepsize
    eps : float, optional, default : 0.9
        Desired maximum relative error
    prgrow : float, optional, default : -1/3
        Power for increasing step size
    pshrink : float, optional, default : -1/2
        Power for decreasing stepsize
    safety : float, optional, default : 0.9
        Safety factor when changing step size
    args : additional positional arguments
    kwargs : additional keyworda arguments

    Returns
    -------
    dY : Field
        Delta of variable to be integrated
        False if step size too large

    Butcher tableau
    ---------------
      0  |  0    0   0   0
     1/2 | 1/2   0   0   0
     3/4 |  0   3/4  0   0
      1  | 2/9  1/3 4/9  0
    -----|------------------
         | 2/9  1/3 4/9  0
         | 7/24 1/4 1/3 1/8
    """
    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0 * dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + a21*k1 * dx)
    k3 = Y0.derivative(x0 + dx, Y0 + (a30*k0 + a31*k1 + a32*k2)*dx)

    Yscale = np.abs(Y0) + np.abs(dx*k0)
    Yscale[Yscale == 0.] = 1.e100       # Deactivate for zero crossings

    e = dx*(e0*k0 + e1*k1 + e2*k2 + e3*k3)
    emax = np.max(np.abs(e/Yscale)) / eps

    # Integration successful
    if emax <= 1.:
        # Suggest new stepsize
        dxnew = safety*dx*emax**pgrow if econ < emax else 5.*dx
        x0.suggest(dxnew)
        return dx*(b0*k0 + b1*k1 + b2*k2)
    else:
        # Suggest new stepsize
        dxnew = np.maximum(safety*dx*emax**pshrink, 0.1*dx)
        x0.suggest(dxnew)
        return False


expl_3_bogacki_shampine_adptv = Scheme(
    _f_expl_3_bogacki_shampine_adptv, description="Explicit adaptive 3rd-order Bogacki-Shampine method")
