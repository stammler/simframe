import inspect
from simframe.utils.color import colorize


class Updater():
    """Class that manages how a ``Group`` or ``Field`` is updated."""

    __name__ = "Updater"

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
        s = "{}".format(str(self.__name__)) + "\n"
        s += (len(s)-1)*"-" + "\n"
        s += "\n"
        # Signature
        try:
            sig = "{}{}".format(self._func.__name__,
                                inspect.signature(self._func))
            s += "{} {}".format(colorize("Signature:",
                                color="red"), str(sig)) + "\n"
        except:
            pass
        # Source/Docstring
        try:
            source = inspect.getsource(self._func)
            cat = colorize("Source:", color="red")
        except:
            source = self._func.__doc__
            cat = colorize("Docstring:", color="red")
        if source is not None:
            s += cat + "\n"
            s += source + "\n"
        # File
        try:
            fn = inspect.getfile(self._func)
            s += "{} {}".format(colorize("File:", color="red"), fn) + "\n"
        except:
            pass
        # Type
        cls = self._func.__class__.__name__
        s += "{} {}".format(colorize("Type:", color="red"), cls)
        return s

    def __repr__(self):
        return self.__str__()
