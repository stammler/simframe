from simframe.frame.heartbeat import Heartbeat


class AbstractGroup(object):
    """This is an abstract class that serves as template for other classes.

    ``AbstractGroup`` has a descriptive string, an owner and an updater.
    The owner is the parent ``Frame`` object and is hidden. The updater is of type ``Heartbeat``.

    ``AbstractGroup`` has an ``update`` method that is calling ``systole``, ``updater``, and ``diastole``
    of the ``Heartbeat`` object, which manages the update of ``AbstractGroup``.

    ``AbstractGroup`` should not be instanciated directly."""

    __name__ = ""

    _description = ""
    _owner = None
    _updater = Heartbeat(None)

    @property
    def description(self):
        '''Description of the instance.'''
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    @property
    def updater(self):
        '''``Heatbeat`` object with instructions for updating the instance.'''
        return self._updater

    @updater.setter
    def updater(self, value):
        if isinstance(value, Heartbeat):
            self._updater = value
        else:
            self._updater = Heartbeat(value)

    def __str__(self):
        ret = "{}".format(str(self.__name__))
        description = " (" + self.description + \
            ")" if self.description != "" else self.description
        ret = "{}{}".format(self.__name__, description)
        return ret

    def __repr__(self):
        return self.__str__()

    def update(self, *args, **kwargs):
        """Function to update the object.
        Ths functions calls the heartbeat instance of the object.

        Parameters
        ----------
        args : additional positional arguments
        kwargs : additional keyword arguments

        Notes
        -----
        Positional arguments and keyword arguments are only passed to the ``updater``,
        NOT to ``systole`` and ``diastole``."""
        self.updater.beat(self._owner, *args, **kwargs)
