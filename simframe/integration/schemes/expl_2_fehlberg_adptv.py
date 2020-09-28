from simframe.integration.scheme import Scheme

import numpy as np

# Butcher coefficients
a10 = 1/2
a20, a21 = 1/256, 255/256
b0, b1, b2 = 1/512, 255/256, 1/512
bs0, bs1 = 1/256, 255/256
e0, e1, e2 = b0-bs0, b1-bs1, b2
c1 = 1/2


def _f_expl_2_fehlberg_adptv(x0, Y0, dx, *args, dYdx=None, econ=0.0324, eps=0.1, pgrow=-0.5, pshrink=-1., safety=0.9, **kwargs):
    """Explicit adaptive 2nd-order Fehlberg's method

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
    econ : float, optional, default : 0.0324
        Error controll parameter for setting stepsize
    eps : float, optional, default : 0.9
        Desired maximum relative error
    prgrow : float, optional, default : -0.5
        Power for increasing step size
    pshrink : float, optional, default : -1.
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
      0  | 0     0       0
     1/2 | 1/2   0       0
      1  | 1/256 255/256 0
    -----|---------------------
         | 1/512 255/256 1/512
         | 1/256 255/256 0
    """
    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0 * dx)
    k2 = Y0.derivative(x0 + dx, Y0 + (a20*k0 + a21*k1)*dx)

    Yscale = np.abs(Y0) + np.abs(dx*k0)
    Yscale[Yscale == 0.] = 1.e100       # Deactivate for zero crossings

    e = dx*(e0*k0 + e1*k1 + e2*k2)
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


expl_2_fehlberg_adptv = Scheme(
    _f_expl_2_fehlberg_adptv, description="Explicit adaptive 2nd-order Fehlberg's method")
