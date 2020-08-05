import numpy as np
from simframe.frame.abstractgroup import AbstractGroup
from simframe.frame.updater import Updater

class Field(np.ndarray, AbstractGroup):
    """Class for quantities or fields.
    
    Parameters
    ----------
    owner : Frame
        Parent frame object to which the field belongs
    value : number, array, string
        Initial value of the field. Needs to have correct type and shape
    updater : Updater, callable, optional, default : None
        Updater for field update
    systole : Updater, callable, optional, default : None
        Systole for field update
    diastole : Updater, callable, optional, default : None
        Diastole for field update 
    description : string, optional, default : None
        Descriptive string for the field
    constant : boolean, optional, default : False
        Should this field be constant?
        
    Notes
    -----
    When <field>.update() is called the field will be updated according return value of the updater..
    Before the field is updated the systole updater is called. After the field update the diastole updater is called.
    The updaters, systoles, and diastoles for fields can either be of type Updater, can be a callable function which
    executes the desired operation, or can be None, if no operation should be performed. If it is set to a callable
    function the function's only argument has to be the parent Frame object. The callable function of the updater has
    to return the new value of the field.
    
    Examples
    --------
    >>> fld = Field(sim, np.ones(5), description="My Field")
    >>> fld
    Field (My Field):
    [1 1 1 1 1]
    """
    
    __name__ = "Field"

    def __new__(cls, owner, value, updater=None, differentiator=None, description=None, constant=False):
        obj = np.asarray(value).view(cls)
        obj._owner = owner
        obj._updater = obj._constructheartbeat(updater)
        obj._differentiator = obj._constructheartbeat(differentiator)
        obj.description = description
        obj._constant = constant
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self._owner = getattr(obj, "_owner", None)
        self._updater = getattr(obj, "_updater", None)
        self._differentiator = getattr(obj, "_differentiatorystole", None)
        self.description = getattr(obj, "description", None)
        self._constant = getattr(obj, "_constant", False)

    @property
    def differentiator(self):
        return self._differentiator
    @differentiator.setter
    def differentiator(self, value):
        self._differentiator = self._constructheartbeat(value)

    @property
    def constant(self):
        return self._constant
    @constant.setter
    def constant(self, value):
        if isinstance(value, np.int):
            if value:
                self._constant = True
            else:
                self._constant = False
        else:
            raise TypeError("<value> hat to be of type bool.")

    @property
    def owner(self):
        return self._owner
    @owner.setter
    def owner(self, value):
        raise RuntimeError("The owner cannot be set directly.")

    def update(self, *args, **kwargs):
        """Function to update the field."""
        ret = self.updater.beat(self._owner, *args, **kwargs)
        self._setvalue(ret)

    def derivative(self, *args, **kwargs):
        """If differentiator is set, this returns the derivative of the field"""
        return self.differentiator.beat(self._owner, *args, **kwargs)
        
    def _setvalue(self, value):
        """Function to set a value to the field. Direct assignement of values does overwrite the Field object.
        
        Parameters
        ----------
        value : number, array, string
            Value to be written into the field. Needs to have correct type and shape"""
        if self._constant:
            raise RuntimeError("Field is constant.")
        value = np.asarray(value)
        if not value.shape == self.shape:
            raise ValueError("Shape mismatch: "+repr(self.shape)+", "+repr(value.shape))
        self.setfield(value, self.dtype)

    def __str__(self):
        ret = "{:5s}".format(str(self.__name__))
        if((self._description != "") and (self._description != None)):
            ret += " ({})".format(self._description)
        if self._constant:
            ret += ", \033[95mconstant\033[0m"
        return ret

    def __repr__(self):
        ret = "{}\n{}\n{}".format(self.__str__(), "-" * len(self.__str__()), np.ndarray.__str__(self.getfield(self.dtype)))
        return ret