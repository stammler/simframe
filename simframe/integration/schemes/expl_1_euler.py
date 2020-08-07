from simframe.integration import AbstractScheme

def _f_expl_1_euler(x0, Y0, dx):
    """Simple explicit 1st order Euler integration scheme
    
    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
        
    Returns
    -------
    dY : Field
        Delta of variable to be integrated"""
    return dx*Y0.derivative(x0, Y0)

expl_1_euler = AbstractScheme(_f_expl_1_euler, description="Explicit 1st-order Euler")