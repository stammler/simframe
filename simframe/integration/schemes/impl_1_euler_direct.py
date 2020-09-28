from simframe.integration.scheme import Scheme

import numpy as np


def _f_impl_1_euler_direct(x0, Y0, dx, jac=None, *args, **kwargs):
    """Implicit 1st-order Euler integration scheme with direct matrix inversion

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
    A = eye - dx[0] * jac
    return (np.linalg.inv(A) - eye) @ Y0


impl_1_euler_direct = Scheme(
    _f_impl_1_euler_direct, description="Implicit 1st-order direct Euler method")
