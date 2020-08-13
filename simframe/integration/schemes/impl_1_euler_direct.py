from simframe.integration.abstractscheme import AbstractScheme

import numpy as np


def _f_impl_1_euler_direct(x0, Y0, dx, *args, **kwargs):
    """Implicit 1st-order Euler integration scheme with direct matrix inversion

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
    dY : Field
        Delta of variable to be integrated

    Butcher tableau
    ---------------
     1 | 1
    ---|---
       | 1 
    """
    jac = Y0.derivative(x0, Y0)
    N = jac.shape[0]
    eye = np.eye(N)
    A = eye - dx*jac
    return np.dot(np.linalg.inv(A), Y0)


impl_1_euler_direct = AbstractScheme(
    _f_impl_1_euler_direct, description="Implicit 1st-order direct Euler method")
