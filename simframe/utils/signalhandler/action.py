class Action(object):
    """Template class of an action that is performed once a signal is detected."""

    def __init__(self):
        """
        Callable action class that is performing an action on a ``simframe.Frame``.
        """
        super().__init__()

    def _do(self, frame, *args, **kwargs):
        """
        Function that is performed when action is called.
        Has to be implemented by child class.

        Parameters
        ----------
        frame : Frame
            Simulation frame on which the action should be performed.
        args : additional positional arguments
        kwargs : additional keyword arguments
        """
        raise NotImplementedError

    def __call__(self, frame, *args, **kwargs):
        """
        Performing the action.

        Parameters
        ----------
        frame : Frame
            Simulation frame on which the action should be performed.
        args : additional positional arguments
        kwargs : additional keyword arguments
        """
        return self._do(frame, *args, **kwargs)