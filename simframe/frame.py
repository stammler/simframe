from functools import partial
import numpy as np

class AbstractGroup(object):
    """This is an abstract class that should not be instanced directly. It only serves as templates for other classes."""
    
    _fields = {}
    _Updater = None
    _SystoleUpdater = None
    _DiastoleUpdater = None
    
    def __getattribute__(self, name):
        """Getter function to read fields from object."""
        _fields = super().__getattribute__("_fields")
        if name in _fields.keys():
            return self._fields[name]
        else:
            return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        """Setter function to write fields to object."""
        if name in self._fields.keys():
            field = self._fields[name]
            value = np.asarray(value)
            field._setvalue(value)
        else:
            super().__setattr__(name, value)
            
    def __delattr__(self, name):
        """Function to delete fields."""
        if name in self._fields.keys():
            self._fields.pop(name, None)
        super().__delattr__(name)
        
    def setdescription(self, description):
        """Sets description of class.

        Parameters
        ----------
        description : string
            descriptive string for the class

        Examples
        --------
        >>> sim.setdescription("standard model")
        """
        self._description = description
        
    def _constructupdater(self, func=None, updater=None):
        """Helper method for type checks. Don't call this directly."""

        if not (updater or func):
            raise ValueError("Either <func> or <updater> has to be given.")
        if (updater and func):
            raise ValueError("Giving both, <func> and <updater>, is ambiguous.")
        if updater:
            if type(updater) is not Updater:
                raise TypeError("<updater> has to be of type Updater.")
            updtr = updater
        if func:
            if not hasattr(func, '__call__'):
                raise TypeError("<func> is not callable.")
            updtr = Updater(func)
        return updtr
        
    def setupdater(self, func=None, updater=None):
        """Sets Updater of the class.
        
        Parameters
        ----------
        func : callable, optional, default : None
            Object that is called when class is updated
        updater : Updater, optional, default : None
            Object of type Updater
            
        Notes
        -----
        Exactly one of <func> or <updater> has to be given.
        
        See Also
        --------
        setsystole : function that sets the systole of the class
        setdiastole : function that sets the diastole of the class
        
        Examples
        --------
        >>> sim.setupdater(func=myupdatefunction)
        
        >>> sim.setupdater(updater=myupdater)            
        """
        updtr = self._constructupdater(func, updater)
        self._Updater = updtr
        
    def setsystole(self, func=None, updater=None):
        """Sets Updater of the systole of the class. The systole is called immediately before the updater is called.
        
        Parameters
        ----------
        func : callable, optional, default : None
            Object that is called before class is updated
        updater : Updater, optional, default : None
            Object of type Updater
            
        Notes
        -----
        Exactly one of <func> or <updater> has to be given.
        
        See Also
        --------
        setupdater : function that sets the updater of the class
        setdiastole : function that sets the diastole of the class
        
        Examples
        --------
        >>> sim.setsystole(func=myupdatefunction)
        
        >>> sim.setsystole(updater=myupdater)            
        """
        updtr = self._constructupdater(func, updater)
        self._SystoleUpdater = updtr
        
    def setdiastole(self, func=None, updater=None):
        """Sets Updater of the diastole of the class. The diastole is called immediately after the updater has been called.
        
        Parameters
        ----------
        func : callable, optional, default : None
            Object that is called after class has been updated
        updater : Updater, optional, default : None
            Object of type Updater
            
        Notes
        -----
        Exactly one of <func> or <updater> has to be given.
        
        See Also
        --------
        setupdater : function that sets the updater of the class
        setsystole : function that sets the systole of the class
        
        Examples
        --------
        >>> sim.setdiastole(func=myupdatefunction)
        
        >>> sim.setdiastole(updater=myupdater)            
        """
        updtr = self._constructupdater(func, updater)
        self._DiasystoleUpdater = updtr


class Group(AbstractGroup):
    """Class for grouping fields.
    
    Parameters
    ----------
    owner : Simulation
        Parent simulation object to which the group belongs
    func : callable, optional, default : None
        Update function for the group
    updater : Updater, optional, default : None
        Updater class for the group
    description : string, optional, default : None
        Descriptive string for the group
        
    Notes
    -----
    Only one of <func> or <updater> can be given. If neither one is given, the group does nothing when being updated.
    
    Examples
    --------
    >>> grp = Group(sim, description="My group")
    """
    
    _type = "Group"
    
    def __init__(self, owner, func=None, updater=None, description=None):
        self._description = description
        self._owner = owner
        if (func or updater):
            self.setupdater(func=func, updater=updater)
        else:
            self._Updater = None
        
    def update(self):
        """Function to update the object."""
        
        if self._SystoleUpdater is not None:
            self._SystoleUpdater.update(self._owner)
        if self._Updater is not None:
            self._Updater.update(self._owner)
        if self._DiastoleUpdater is not None:
            self._DiastoleUpdater.update(self._owner)
            
    def addfield(self, name, value, func=None, updater=None, description=None, constant=False):
        """Function to add a field to the object.
        
        Parameters
        ----------
        name : string
            Name of the field
        value : number, array, string
            Initial value of the field. Needs to have correct type and shape
        func : callable, optional, default : None
            Function to be called to update the field
        updater : Updater, optional, default : None
            Updater class for the field
        description : string, optional, default : None
            Descriptive string for the field
        constant : boolean, optional, default : False
            Should this field be constant?
            
        Notes
        -----
        Only one of <func> or <updater> can be given. If neither one is given, the field does nothing when being updated.
        
        See Also
        --------
        addgroup : Function to add a group to the object
        
        Examples
        --------
        >>> sim.addfield("myfield", np.ones(5), description="My Field")
        >>> sim.myfield
        Field (My Field):
        [1 1 1 1 1]
        """
        self._fields[name] = Field(self._owner, value, func=func, updater=updater, description=description, constant=constant)
        self.__dict__[name] = self._fields[name]
        
    def addgroup(self, name, func=None, updater=None, description=None):
        """Function to add a group to the object.
        
        Parameters
        ----------
        name : string
            Name of the group
        func : callable, optional, default : None
            Function to be called to update the group
        updater : Updater, optional, default : None
            Updater class for the group
        description : string, optional, default : None
            Descriptive string for the group
            
        Notes
        -----
        Only one of <func> or <updater> can be given. If neither one is given, the group does nothing when being updated.
        
        See Also
        --------
        addfield : Function to add a field to the object
        
        Examples
        --------
        >>> sim.addgroup("mygroup, description="My Group")
        >>> sim.mygroup
        Group (My Group):
        """
        self.__dict__[name] = Group(self._owner, func=func, updater=updater, description=description)
        
    def __repr__(self):
        s = self._type+"{}\n\n".format(" ("+self._description+"):" if self._description else ":")
        
        for key in sorted(self.__dict__.keys(), key=str.casefold):
            
            val = self.__dict__[key]
            
            if key.startswith("_"): continue
            
            if len(key) > 12:
                name = key[:9]+"..."
            else:
                name = key
            if type(val) is Group:
                s += "{:11s}{:7s}: {:12s} {}\n".format("", "Group", name, "("+val._description+")" if val._description else "")
            elif type(val) is Field:
                s += "{:11s}{:7s}: {:12s} {}\n".format("    Const. " if val._constant else "", "Field", name, "("+val._description+")" if val._description else "")
            else:
                s += "{:11s}{:7s}: {:12s}\n".format("", type(val).__name__, name)
            
        return s


class Field(np.ndarray, AbstractGroup):
    """Class for quantities or fields.
    
    Parameters
    ----------
    owner : Simulation
        Parent simulation object to which the field belongs
    value : number, array, string
        Initial value of the field. Needs to have correct type and shape
    func : callable, optional, default : None
        Update function for the field
    updater : Updater, optional, default : None
        Updater class for the field
    description : string, optional, default : None
        Descriptive string for the field
    constant : boolean, optional, default : False
        Should this field be a constant?
        
    Notes
    -----
    Only one of <func> or <updater> can be given. If neither one is given, the field does nothing when being updated.
    
    Examples
    --------
    >>> fld = Field(sim, np.ones(5), description="My Field")
    >>> fld
    Field (My Field):
    [1 1 1 1 1]
    """
    
    def __new__(cls, owner, value, func=None, updater=None, description=None, constant=False):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(value).view(cls)
        # add the new attribute to the created instance
        obj._owner = owner
        if (func or updater):
            obj._Updater = obj.setupdater(func=func, updater=updater)
        obj._description = description
        obj._constant = constant
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        self._owner = getattr(obj, "_owner", None)
        self._Updater = getattr(obj, "Updater", None)
        self._description = getattr(obj, "description", None)
        self._constant = getattr(obj, "constant", False)
        
    def __repr__(self):
        return "{}Field{}\n{}".format("Constant " if self._constant else "", " ("+self._description+"):" if self._description else ":", self.getfield(self.dtype))
    
    def update(self):
        """Function to update the object."""
        if self._Updater is not None:
            self._setvalue(self._Updater.update(self._owner))
        
    def _setvalue(self, value):
        """Function to set a value to the field. Direct assignement of values does overwrite the Field object.
        
        Parameters
        ----------
        value : number, array, string
            Value to be written into the field. Needs to have correct type and shape"""
        if self._constant:
            raise TypeError("Field is constant.")
        if not value.shape == self.shape:
            raise ValueError("Shape mismatch: "+repr(self.shape)+", "+repr(value.shape))
        self.setfield(value, self.dtype)


class Updater():
    """Class that manages how a group or field is updated
    
    Parameter
    ---------
    func : callable
        Object that is called when group or field is being updated.
        For field: has to return the new value of the field.
    simulation : Simulation
        The Simulation object to which the Updater belongs
        
    Examples
    --------
    >>> myupdater = Updater(myfunction, mysimulation)
    """
    
    def __init__(self, func):
        if not hasattr(func, '__call__'):
            raise TypeError("<func> is not callable.")
        self._func = func
        
    def update(self, owner):
        """Function that is called when group or field to which Updater belongs is being updated."""
        
        return self._func(owner)


class Simulation(Group):
    """Simulation class.
    This is the parent object that contains all other objects
    
    Parameters
    ----------
    description : string, optional, default : None
        Descriptive string of the simulation object
    writer : Writer, optional, default : None
        Object of type Writer fir writing output files
        
    Examples
    --------
    >>> sim = Simulation(description="My Simulation")
    >>> sim
    Simulation (My Simulation):"""
    
    _type = "Simulation"
    
    def __init__(self, description=None, writer=None):
        self._description = description
        self._owner = self
        self._writer = None

    def setwriter(self, writer):
        """Function to bind a writer class to the simulation object
        
        Parameters
        ----------
        writer : Writer
            Object of type Writer"""

        self._writer = writer

    def writeoutput(self, i=0, filename="", forceoverwrite=False, **kwargs):
        """Writes output to file, if writer is specified.
        
        Parameters
        ----------
        i : int, optional, default : 0
            Number of output
        filename : string, optional, default = ""
            if given this will write the output to this file. Otherwise, it uses the standard scheme.
        forceoverwrite : boolean, optional, default : False
            If True, this overrules the seetings of the Writer and enforces the file to be overwritten."""

        if self._writer is not None:
            self._writer.write(self, i, filename, forceoverwrite, **kwargs)