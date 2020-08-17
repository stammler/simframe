from simframe.integration.scheme import Scheme

import numpy as np


def _f_impl_2_midpoint_direct(x0, Y0, dx, *args, **kwargs):
    """Implicit 2nd-order midpoint method with direct matrix inversion

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
     1/2 | 1/2
    -----|-----
         |  1 
    """
    J = Y0.jacobian(x0+0.5*dx)          # Jacobian
    N = J.shape[0]                      # Problem size
    eye = np.eye(N)                     # Identity matrix

    A = eye - 0.5*dx*J
    Ainv = np.linalg.inv(A)
    k1 = np.dot(Ainv, np.dot(J, Y0))

    return Y0 + dx*k1


impl_2_midpoint_direct = Scheme(
    _f_impl_2_midpoint_direct, description="Implicit 2nd-order direct midpoint method")
