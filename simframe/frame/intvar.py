import numpy as np

from simframe.frame.field import Field
from simframe.frame.heartbeat import Heartbeat
from simframe.frame.updater import Updater

class IntVar(Field):
    """Integration variable.
    
    Field for storing integration variables. Same as regular Field, but containing infrastructure for getting
    step size, snapshots, etc.
    
    Parameters
    ----------
    owner : Frame
        Parent frame object to which the field belongs
    value : number, optional, default : 0
        Initial value of the field
    snapshots : list, array, optional, default : []
        List or array of snapshots at which an output file should be written.
        Has to be monotonously increasing.
    updater : Updater, callable or list, optional, default : None
        Updater for field update
    systole : Updater, callable or list, optional, default : None
        Systole for field update
    diastole : Updater, callable or list, optional, default : None
        Diastole for field update 
    description : string, optional, default : None
        Descriptive string for the field

    Notes
    -----
    When <Intvar>.update() is called the Intvar will by adding the stepsize to the current value.
    Before the Intvar is updated the systole updater is called. After the Intvar update the diastole updater is called.
    The updater, systoles, and diastoles for Intvars can either be of type Updater, can be a callable function which
    executes the desired operation, or can be None, if no operation should be performed. If it is set to a callable
    function the function's only argument has to be the parent Frame object. The callable function of the updater has
    to return the stepsize of the integration variable

    Examples
    --------
    >>> t = Intvar(sim, 0., description="Time")
    >>> t
    Intvar (Time):
    0
    """

    def __new__(cls, owner, value=0, snapshots=[], updater=None, description=None):
        obj = super().__new__(cls, owner, value, updater=updater, description=description, constant=False)
        obj.snapshots = snapshots
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        super().__array_finalize__(obj)
        self.snapshots = getattr(obj, "snapshots", [])

    def update(self):
        msg = "Warning: Do not update any integration variable by hand."
        print(msg)

    def _update(self, u, *args, upd=False, **kwargs):
        msg = "Warning: Do not update any integration variable by hand."
        print(msg)

    @property
    def stepsize(self):
        if isinstance(self.updater, Heartbeat):
            return np.minimum(self.updater.beat(self._owner), self.maxstepsize)
        raise RuntimeError("You need to set an Updater for stepsize function first.")

    @property
    def snapshots(self):
        return self._snapshots
    @snapshots.setter
    def snapshots(self, value):
        snaps = np.asarray(value)
        if snaps.size > 1:
            if not all(x<y for x, y in zip(snaps, snaps[1:])):
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

    def __str__(self):
        ret = "{:5s}".format(str(self.__name__))
        if((self._description != "") and (self._description != None)):
            ret += " ({})".format(self._description)
        ret += ", \033[95mIntegration variable\033[0m"
        return ret