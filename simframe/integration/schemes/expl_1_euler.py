from simframe.integration import AbstractScheme

def _f_expl_1_euler(dx, Y):
    """Simple explicit 1st order Euler integration scheme
    
    Parameters
    ----------
    dx : IntVar
        Stepsize of integration variable
    Y : Field
        Variable to be integrated
        
    Returns
    -------
    dY : Field
        Delta of variable to be integrated"""
    return dx*Y.derivative(Y)

expl_1_euler = AbstractScheme(_f_expl_1_euler, description="Explicit 1st-order Euler")