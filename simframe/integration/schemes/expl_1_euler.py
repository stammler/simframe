from simframe.integration.scheme import Scheme


def _f_expl_1_euler(x0, Y0, dx, *args, dYdx=None, **kwargs):
    """Explicit 1st-order Euler integration scheme

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
    args : additional positional arguments
    kwargs : additional keyworda arguments

    Returns
    -------
    dY : Field
        Delta of variable to be integrated

    Butcher tableau
    ---------------
     0 | 0
    ---|---
       | 1 
    """
    k0 = Y0.derivative(x0, Y0) if dYdx is None else dYdx
    return dx*k0


expl_1_euler = Scheme(
    _f_expl_1_euler, description="Explicit 1st-order Euler method")
