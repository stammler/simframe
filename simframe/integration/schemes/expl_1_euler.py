from simframe.integration import AbstractScheme

def _f_expl_1_euler(Y, dx):
    """Simple explicit 1st order Euler integration scheme
    
    Parameters
    ----------
    Y : Field
        Variable to be integrated
    dx : IntVar
        Stepsize of integration variable
        
    Returns
    -------
    dY : Field
        Delta of variable to be integrated"""
    return dx*Y.derivative(Y)

expl_1_euler = AbstractScheme(_f_expl_1_euler, description="Explicit 1st-order Euler")