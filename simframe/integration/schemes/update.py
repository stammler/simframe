from simframe.integration.scheme import Scheme


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
    if Y0.buffer is not None:
        Y0._setvalue(Y0 + Y0._buffer)
        Y0._buffer = None
    return True


update = Scheme(_update, description="Instruction to update Y")
