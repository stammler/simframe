from simframe.integration import AbstractScheme

def _update(x0, Y0, dx, *args, **kwargs):
    """Instruction for updating Y
    
    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
    args : additional positional arguments
    kwargs : additional keyword arguments
        
    Returns
    -------
    dY : True"""
    Y0 += Y0._buffer
    Y0._buffer = 0.
    return True

update = AbstractScheme(_update, description="Instruction to update Y")