import numpy as np

from simframe.frame.field import Field
from simframe.frame.heartbeat import Heartbeat


class IntVar(Field):
    """This class behaves as Fields but has additional functionality with respect to
    stepsize management for integration.

    Notes
    -----
    The updater for integration variables is calculating the stepsize. The function assiciated to the
    updater needs the parent Frame object as first positional argument and needs to return the
    desired stepsize.

    IntVar has additional attribute:

    maxstepsize : the maximum stepsize until the next snapshot
    stepsize : minimum of the desired stepsize and maxstepsize
    nextsnapshot : value of the next snapshot

    update() does not update the integration variable. Try not to update the integration variable by hand.
    Let the integrator do it for you."""

    _snapshots = []
    _suggested = None

    def __new__(cls, owner, value=0, snapshots=[], updater=None, description="", copy=False):
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
        copy : boolean, optional, default : True
            If True <value> will be copied, not referenced"""
        obj = super().__new__(cls, owner, value, updater=updater,
                              description=description, constant=False, copy=copy)
        obj.snapshots = snapshots
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        super().__array_finalize__(obj)
        self.snapshots = getattr(obj, "snapshots", [])

    def __str__(self):
        ret = "{}".format(str(self.__name__))
        ret = super().__str__()
        ret += ", \033[95mIntegration variable\033[0m"
        return ret

    def update(self):
        msg = "\033[93mWarning:\033[0m Do not update the integration variable by hand."
        print(msg)

    def _update(self, u, *args, upd=False, **kwargs):
        msg = "\033[93mWarning:\033[0m Do not update the integration variable by hand."
        print(msg)

    def suggest(self, value):
        """Suggest a step size

        For adaptive integration schemes, this function can be used to suggest a step size for the next
        integration step. If many vaiables are integrated this safes the smallest suggested step size
        in a temporary buffer accessible via <IntVar>.suggested.

        Parameters
        ----------
        value : Field
            Suggested step size"""
        self.suggested = value if self._suggested is None else np.minimum(
            self._suggested, value)

    @property
    def suggested(self):
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
        if isinstance(self.updater, Heartbeat):
            return np.minimum(self.updater.beat(self._owner), self.maxstepsize)
        raise RuntimeError(
            "You need to set an Updater for stepsize function first.")

    @property
    def snapshots(self):
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
        if self.snapshots.size < 1:
            raise ValueError("Snapshots are emtpy")
        return self.snapshots[np.argmax(self < self.snapshots)]

    @property
    def maxstepsize(self):
        return self.nextsnapshot - self.getfield(dtype=self.dtype)
