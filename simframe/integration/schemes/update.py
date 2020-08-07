from simframe.integration import AbstractScheme

def _update(Y, dx=None):
    """Instruction for updating Y
    
    Parameters
    ----------
    Y : Field
        Variable to be updated
    dx : IntVar, optional, default : None
        not used for this instruction
        
    Returns
    -------
    dY : True"""
    Y += Y._buffer
    Y._buffer = 0.
    return True

update = AbstractScheme(_update, description="Instruction to update Y")