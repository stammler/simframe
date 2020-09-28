from simframe.integration.scheme import Scheme

import numpy as np

# Butcher coefficients
a10 = 1/2
a20, a21 = 3/40, 9/40
a30, a31, a32 = 3/10, -9/10, 6/5
a40, a41, a42, a43 = -11/54, 5/2, -70/27, 35/27
a50, a51, a52, a53, a54 = 1631/55296, 175 / \
    512, 575/13824, 44275/110592, 253/4096
b0, b2, b3, b5 = 37/378, 250/621, 125/594, 512/1771
bs0, bs2, bs3, bs4, bs5 = 2825/27648, 18575/48384, 13525/55296, 277/14336, 1/4
e0, e2, e3, e4, e5 = b0-bs0, b2-bs2, b3-bs3, -bs4, b5-bs5
c1, c2, c3, c5 = 1/5, 3/10, 3/10, 7/8


def _f_expl_5_cash_karp_adptv(x0, Y0, dx, *args, dYdx=None, econ=0.0001889568, eps=0.1, pgrow=-0.2, pshrink=-0.25, safety=0.9, **kwargs):
    """Explicit adaptive 5th-order Cash-Karp method

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
      0   |     0         0         0           0          0         0
     1/5  |    1/5        0         0           0          0         0
     3/10 |    3/40      9/40       0           0          0         0
     3/5  |    3/10     -9/10      6/5          0          0         0
      1   |  -11/54      5/2     -70/27       35/27        0         0
     7/8  | 1631/55296 175/512   575/13824 44275/110592 253/4096     0
    ------|----------------------------------------------------------------
          |   37/378      0      250/621     125/594       0      512/1771
          | 2825/27648    0    18575/48384 13525/55296  277/14336   1/4
    """
    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0 * dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + (a20*k0 + a21*k1)*dx)
    k3 = Y0.derivative(x0 + c3*dx, Y0 + (a30*k0 + a31*k1 + a32*k2)*dx)
    k4 = Y0.derivative(x0 + dx, Y0 + (a40*k0 + a41*k1 + a42*k2 + a43*k3)*dx)
    k5 = Y0.derivative(x0 + c5*dx, Y0 + (a50*k0 + a51 *
                                         k1 + a52*k2 + a53*k3 + a54*k4)*dx)

    Yscale = np.abs(Y0) + np.abs(dx*k0)
    Yscale[Yscale == 0.] = 1.e100       # Deactivate for zero crossings

    e = dx*(e0*k0 + e2*k2 + e3*k3 + e4*k4 + e5*k5)
    emax = np.max(np.abs(e/Yscale)) / eps

    # Integration successful
    if emax <= 1.:
        # Suggest new stepsize
        dxnew = safety*dx*emax**pgrow if econ < emax else 5.*dx
        x0.suggest(dxnew)
        return dx*(b0*k0 + b2*k2 + b3*k3 + b5*k5)
    else:
        # Suggest new stepsize
        dxnew = np.maximum(safety*dx*emax**pshrink, 0.1*dx)
        x0.suggest(dxnew)
        return False


expl_5_cash_karp_adptv = Scheme(
    _f_expl_5_cash_karp_adptv, description="Explicit adaptive 5th-order Cash-Karp method")
