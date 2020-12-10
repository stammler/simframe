import numpy as np

from simframe.frame.field import Field
from simframe.frame.heartbeat import Heartbeat
from simframe.utils.color import colorize


class IntVar(Field):
    """Cclass for integration variables that behaves as ``Field`` but has additional functionality with respect to
    stepsize management for integration.

    Notes
    -----
    The ``updater`` for integration variables is calculating the stepsize. The function associated to the
    ``updater`` needs the parent ``Frame`` object as first positional argument and needs to return the
    desired stepsize.

    ``IntVar.update()`` does not update the integration variable. Try not to update the integration variable by hand.
    Let the ``Integrator`` do it for you."""

    _snapshots = []
    _suggested = None
    _prevstepsize = 0.

    def __new__(cls, owner, value=0, snapshots=[], updater=None, description="", save=True, copy=False):
        """Parameters
        ----------
        owner : Frame
            Parent frame object to which the field belongs
        value : number, optional, default : 0
            Initial value of the field
        snapshots : list, array, optional, default : []
            List or array of snapshots at which an output file should be written.
            Has to be monotonously increasing.
        updater : Heartbeat, Updater, callable, optional, default : None
            Updater for calculating stepsize
        description : string, optional, default : ""
            Descriptive string for the field
        save : boolean, optional, default : True
            If False the integration variable is not written into output files
        copy : boolean, optional, default : True
            If True <value> will be copied, not referenced"""
        obj = super().__new__(cls, owner, value, updater=updater,
                              description=description, constant=False, save=save, copy=copy)
        obj.snapshots = snapshots
        obj._prevstepsize = 0.
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        super().__array_finalize__(obj)
        self.snapshots = getattr(obj, "snapshots", [])
        self._prevstepsize = 0.

    def __str__(self):
        ret = "{}".format(str(self.__name__))
        ret = super().__str__()
        ret += ", {}".format(colorize("Integration variable", "purple"))
        return ret

    def update(self):
        """Not used for ``IntVar``."""
        msg = "{}: {}".format(colorize("Warning", "yellow"),
                              "Do not update the integration variable by hand.")
        print(msg)

    def _update(self, u, *args, upd=False, **kwargs):
        msg = "{}: {}".format(colorize("Warning", "yellow"),
                              "Do not update the integration variable by hand.")
        print(msg)

    def suggest(self, value, reset=False):
        """Suggest a step size

        For adaptive integration schemes, this function can be used to suggest a step size for the next
        integration step. If many vaiables are integrated this safes the smallest suggested step size
        in a temporary buffer accessible via ``IntVar.suggested``.

        Parameters
        ----------
        value : Field
            Suggested step size
        reset : boolean, optional, default : False
            If True, the previous value will be descarded."""
        if reset:
            self._suggested = None
        self.suggested = value if self._suggested is None else np.minimum(
            self._suggested, value)

    @property
    def suggested(self):
        """Suggested step size."""
        if self._suggested is None:
            raise RuntimeError("No step size has been suggested, yet.")
        return self._suggested

    @suggested.setter
    def suggested(self, value):
        if value <= 0:
            raise ValueError(
                "Suggested step size has to be greater than zero.")
        self._suggested = value

    @property
    def stepsize(self):
        '''Current stepsize.'''
        if isinstance(self.updater, Heartbeat):
            return np.minimum(self.updater.beat(self._owner), self.maxstepsize)
        raise RuntimeError(
            "You need to set an Updater for stepsize function first.")

    @property
    def snapshots(self):
        '''Snapshots at which output should be written.

        Even if no outputs are written it needs to contain at least one value that specifies the end point of the
        simulation.'''
        return self._snapshots

    @snapshots.setter
    def snapshots(self, value):
        snaps = np.asarray(value)
        if snaps.size > 1:
            if not all(x < y for x, y in zip(snaps, snaps[1:])):
                raise ValueError("Snapshots have to be strictly increasing")
        self._snapshots = snaps

    @property
    def nextsnapshot(self):
        '''Value of the next snapshot.'''
        if self.snapshots.size < 1:
            raise ValueError("Snapshots are emtpy")
        return self.snapshots[np.argmax(self < self.snapshots)]

    @property
    def prevsnapshot(self):
        '''Value of the previous snapshot.'''
        if self.snapshots.size < 1:
            raise ValueError("Snapshots are emtpy")
        if self < self.snapshots[0]:
            return None
        else:
            return self.snapshots[np.argmin(self >= self.snapshots)-1]

    @property
    def maxstepsize(self):
        '''Maximum possible step size, i.e., to next snapshot.'''
        return self.nextsnapshot - self.getfield(dtype=self.dtype)

    @property
    def prevstepsize(self):
        """Previously taken step size."""
        return self._prevstepsize
