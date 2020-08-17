from simframe.integration.scheme import Scheme


def _f_expl_1_euler(x0, Y0, dx, *args, **kwargs):
    """Explicit 1st-order Euler integration scheme

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
    Y1 : Field
        New value of Y

    Butcher tableau
    ---------------
     0 | 0
    ---|---
       | 1 
    """
    return Y0 + dx*Y0.derivative(x0, Y0)


expl_1_euler = Scheme(
    _f_expl_1_euler, description="Explicit 1st-order Euler method")
