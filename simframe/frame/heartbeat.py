from simframe.frame.updater import Updater


class Heartbeat(object):
    """This class controls an update including ``systole`` and ``diastole``.

    A full cardiac cycle constists of a systole operation, the actual update and a systole operation.
    All three are of type ``Updater``.

    The ``beat`` function calls ``systole``, ``updater``, ``diastole`` in that order and returns the return value
    of the ``updater``. Any positional or keyword arguments are only passed to the ``updater``, NOT to
    ``systole`` and ``diastole``.

    """

    __name__ = "Heartbeat"

    _systole = None
    _updater = None
    _diastole = None

    def __init__(self, updater=None, systole=None, diastole=None):
        """``Heartbeat`` class

        Parameters
        ----------
        updater : Updater, callable, None, optional, default : None
            This it the main updater of the heartbeat object
        systole : Updater, callable, None, optional, default : None
            The updater of the systole
        diastole : Updater, callable, None, optional, default : None
            The updater of the diastole"""

        self.updater = updater
        self.systole = systole
        self.diastole = diastole

    def __str__(self):
        return "{}".format(str(self.__name__))

    def __repr__(self):
        return self.__str__()

    @property
    def systole(self):
        '''``Updater`` that is called in the beginning of cardiac cycle.'''
        return self._systole

    @systole.setter
    def systole(self, value):
        if isinstance(value, Updater):
            self._systole = value
        elif hasattr(value, "__call__") or value is None:
            self._systole = Updater(value)
        else:
            raise TypeError(
                "Systole has to be of type Updater, None, or has to be callable.")

    @property
    def updater(self):
        '''``Updater`` that is performing the update instruction.'''
        return self._updater

    @updater.setter
    def updater(self, value):
        if isinstance(value, Updater):
            self._updater = value
        elif hasattr(value, "__call__") or value is None:
            self._updater = Updater(value)
        else:
            raise TypeError(
                "Updater has to be of type Updater, None, or has to be callable.")

    @property
    def diastole(self):
        '''``Updater`` that is called at the end of the cardiac cycle.'''
        return self._diastole

    @diastole.setter
    def diastole(self, value):
        if isinstance(value, Updater):
            self._diastole = value
        elif hasattr(value, "__call__") or value is None:
            self._diastole = Updater(value)
        else:
            raise TypeError(
                "Diastole has to be of type Updater, None, or has to be callable.")

    def beat(self, owner, *args, Y=None, **kwargs):
        """This method executes ``systole``, ``updater``, and ``distole`` in that order and returns the return value of
        the ``updater``.

        Parameters
        ----------
        owner : Frame
            Parent frame object to which updater belongs
        Y : Field, optional, default : None
            Field that should be updated

        Notes
        -----
            *args and **kwargs are only passed to updater, NOT to systole and diastole

        Returns
        -------
        ret : Return value of updater."""

        # Perform systole operation
        self.systole.update(owner)

        # Perform update operation and save return value.
        ret = self.updater.update(owner, *args, **kwargs)
        # If Y is given and a return value was received, then beat is updating a field.
        # The new field value needs to be set here, so the diastole has access to the new value.
        if Y is not None and ret is not None:
            Y[...] = ret

        # Perform diastole operation.
        self.diastole.update(owner)
        return ret
