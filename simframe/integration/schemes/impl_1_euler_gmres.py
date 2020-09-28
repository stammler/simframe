from simframe.integration.scheme import Scheme

import numpy as np
from scipy.sparse import linalg


def _f_impl_1_euler_gmres(x0, Y0, dx, jac=None, gmres_opt={}, *args, **kwargs):
    """Implicit 1st-order Euler integration scheme with GMRES solver

    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
    jac : Field, optional, defaul : None
        Current Jacobian. Will be calculated, if not set
    gmres_opt : dict, optional, default : {}
        dictionary with options for scipy GMRES solver
    args : additional positional arguments
    kwargs : additional keyworda arguments

    Returns
    -------
    dY : Field
        Delta of variable to be integrated

    Butcher tableau
    ---------------
     1 | 1
    ---|---
       | 1 
    """
    if jac is None:
        jac = Y0.jacobian(x0 + dx)
    N = jac.shape[0]
    eye = np.eye(N)
    A = eye - dx*jac
    res, state = linalg.gmres(A, Y0, **gmres_opt)
    if state != 0:
        return False
    else:
        return res - Y0


impl_1_euler_gmres = Scheme(
    _f_impl_1_euler_gmres, description="Implicit 1st-order Euler method with GMRES solver")
