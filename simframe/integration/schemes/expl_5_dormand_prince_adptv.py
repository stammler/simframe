from simframe.integration.scheme import Scheme

import numpy as np

# Butcher coefficients
a10 = 1/5
a20, a21 = 3/40, 9/40
a30, a31, a32 = 44/45, -56/15, 32/9
a40, a41, a42, a43 = 19372/6561, -25360/2187, 64448/6561, -212/729
a50, a51, a52, a53, a54 = 9017/3168, -355/33, 46732/5247, 49/176, 5103/18656
a60, a62, a63, a64, a65 = 35/384, 500/1113, 125/192, -2187/6784, 11/84
b0, b2, b3, b4, b5 = 35/384, 500/1113, 125/192, -2187/6784, 11/84
bs0, bs2, bs3, bs4, bs5, bs6 = 5179/57600, 7571 / \
    16695, 393/640, -92097/339200, 187/2100, 1/40
e0, e2, e3, e4, e5, e6 = b0-bs0, b2-bs2, b3-bs3, -bs4, b5-bs5, -bs6
c1, c2, c3, c4, = 1/5, 3/10, 4/5, 8/9


def _f_expl_5_dormand_prince_adptv(x0, Y0, dx, *args, dYdx=None, econ=0.0001889568, eps=0.1, pgrow=-0.2, pshrink=-0.25, safety=0.9, **kwargs):
    """Explicit adaptive 5th-order Dormand-Prince method

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
    eps : float, optional, default : 0.1
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
      0   |      0           0          0          0          0          0      0
     1/5  |     1/5          0          0          0          0          0      0
     3/10 |     3/40        9/40        0          0          0          0      0
     4/5  |    44/45      -56/15      32/9         0          0          0      0
     8/9  | 19372/6561 −25360/2187 64448/6561  −212/729       0          0      0
      1   |  9017/3168   −355/33   46732/5247    49/176  −5103/18656     0      0
      1   |    35/384        0       500/1113   125/192  −2187/6784    11/84    0
    ------|-------------------------------------------------------------------------
          |   35/384         0       500/1113   125/192  −2187/6784    11/84    0
          | 5179/57600       0      7571/16695  393/640 −92097/339200 187/2100 1/40
    """
    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0 * dx)
    k2 = Y0.derivative(x0 + c2*dx, Y0 + (a20*k0 + a21*k1)*dx)
    k3 = Y0.derivative(x0 + c3*dx, Y0 + (a30*k0 + a31*k1 + a32*k2)*dx)
    k4 = Y0.derivative(x0 + dx, Y0 + (a40*k0 + a41*k1 + a42*k2 + a43*k3)*dx)
    k5 = Y0.derivative(x0 + dx, Y0 + (a50*k0 + a51 *
                       k1 + a52*k2 + a53*k3 + a54*k4)*dx)
    k6 = Y0.derivative(x0 + dx, Y0 + (a60*k0 + a62 *
                       k2 + a63*k3 + a64*k4 + a65*k5)*dx)

    Yscale = np.abs(Y0) + np.abs(dx*k0)
    Yscale[Yscale == 0.] = 1.e100       # Deactivate for zero crossings

    e = dx*(e0*k0 + e2*k2 + e3*k3 + e4*k4 + e5*k5 + e6*k6)
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


expl_5_dormand_prince_adptv = Scheme(
    _f_expl_5_dormand_prince_adptv, description="Explicit adaptive 5th-order Dormand-Prince method")
