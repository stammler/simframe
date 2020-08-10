from simframe.integration import AbstractScheme

import numpy as np

# Butcher coefficients
a10 = 1.0
b0  = 0.5
b1  = 0.5
bs0 = 1.0
c1  = 1.0
e0  = b0 - bs0
e1  = b1

def _f_expl_2_heun_euler_adptv(x0, Y0, dx, econ=0.0324, eps=0.1, pgrow=-0.5, pshrink=-1., safety=0.9):
    """Explicit adaptive 2nd-order Heun-Euler method
    
    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
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
        
    Returns
    -------
    dY : Field or False
        Delta of variable to be integrated if integration successfule
        False if step size too large
        
    Butcher tableau
    ---------------
      0  |
      1  |  1
    -----|---------
         | 0.5 0.5
         |  1   0
    """
    k0 = Y0.derivative(x0        , Y0            )
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0*dx)

    Yscale  = np.abs(Y0) + np.abs(dx*k0)

    e = dx*(e0*k0 + e1*k1)
    emax = np.max(np.abs(e/Yscale)) / 0.1

    # Integration successful
    if emax <= 1.:
        # Suggest new stepsize
        dxnew = safety*dx*emax**pgrow if econ > emax else 5.*dx
        x0.suggest(dxnew)
        return dx*(b0*k0 + b1*k1)
    else:
        # Suggest new stepsize
        dxnew = np.maximum(safety*dx*emax**pshrink, 0.1*dx)
        x0.suggest(dxnew)
        return dx*(b0*k0 + b1*k1)

expl_2_heun_euler_adptv = AbstractScheme(_f_expl_2_heun_euler_adptv, description="Explicit adaptive 2nd-order Heun-Euler method")