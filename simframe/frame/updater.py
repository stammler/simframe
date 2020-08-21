class Updater():
    """Class that manages how a ``Group`` or ``Field`` is updated."""

    __name__ = "Updater"

    _func = None

    def __init__(self, func=None):
        """Contains update instructions.

        Parameter
        ---------
        func : callable, optional, default : None
            Function that is called when update function is called. None is a null operation."""
        self._func = func

    def update(self, owner, *args, **kwargs):
        """Function that is called when ``Group`` or ``Field`` to which ``Updater`` belongs is being updated.

        Parameters
        ----------
        owner : Frame
            Parent ``Frame`` object
        args : additional positional arguments
        kwargs : additonal keyword arguments"""
        if self._func is not None:
            return self._func(owner, *args, **kwargs)

    def __str__(self):
        return "{}".format(str(self.__name__))

    def __repr__(self):
        return self.__str__()
