from functools import partial
import numpy as np
from simframe.io import Writer

class AbstractGroup(object):
    """This is an abstract class that should not be instanced directly. It only serves as templates for other classes."""
    
    __name__ = None
    _updater = None
    _systole = None
    _diastole = None
    _description = None
            
    def __setattr__(self, name, value):
        """Function to set an attribute including fields."""
        if isinstance(value, Field):
            self.__dict__[name] = value
        elif name in self.__dict__ and isinstance(self.__dict__[name], Field):
            self.__dict__[name]._setvalue(value)
        else:
            super().__setattr__(name, value)
        
    def _constructupdater(self, u=None):
        """Helper method to construct updaters including type checks.
        Do not call this method directly!"""

        if isinstance(u, Updater):
            return u
        if hasattr(u, '__call__'):
            return Updater(u)
        if isinstance(u, list):
            for val in u:
                if not isinstance(val, str):
                    raise ValueError("<u> has to be list of str.")
            return u
        if u is None:
            return u
        raise ValueError("<u> has invalid type.")

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if not isinstance(value, (str, type(None))):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    @property
    def updater(self):
        return self._updater
    @updater.setter
    def updater(self, value):
        self._updater = self._constructupdater(value)

    @property
    def systole(self):
        return self._systole
    @systole.setter
    def systole(self, value):
        self._systole = self._constructupdater(value)

    @property
    def diastole(self):
        return self._diastole
    @diastole.setter
    def diastole(self, value):
        self._diastole = self._constructupdater(value)

    def __str__(self):
        ret = "{:6s}".format(str(self.__name__))
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret

    def __repr__(self):
    
        fields = {}
        groups = {}
        misc = {}
    
        for key, val in self.__dict__.items():
    
            # Don't show private attributes
            if key.startswith("_"): continue
    
            # Sort attributes by group, field and else
            if isinstance(val, Field):
                fields[key] = val
            elif isinstance(val, Group):
                groups[key] = val
            else:
                misc[key] = val
    
        ret = self.__str__()+"\n"
        ret += "-" * (len(ret)-1) + "\n"
    
        if len(groups) > 0:
            for key in sorted(groups.keys(), key=str.casefold):
                if len(key) > 12:
                    name = key[:9]+"..."
                else:
                    name = key
                ret += "    {:12s} : {}\n".format(name, groups[key])
            ret += "  -----\n"
    
        if len(fields) > 0:
            for key in sorted(fields.keys(), key=str.casefold):
                if len(key) > 12:
                    name = key[:9]+"..."
                else:
                    name = key
                ret += "    {:12s} : {}\n".format(name, fields[key].__str__())
            ret += "  -----\n"
    
        if len(misc) > 0:
            for key in sorted(misc.keys(), key=str.casefold):
                if len(key) > 12:
                    name = key[:9]+"..."
                else:
                    name = key
                ret += "    {:12s} : {}\n".format(name, type(misc[key]).__name__)
            ret += "  -----\n"
    
        # If the object has an integrator
        if "_integrator" in self.__dict__.keys():
            integrator = self.__dict__["_integrator"]
            txt = "\033[93mnot specified\033[0m"
            if integrator is not None:
                txt = integrator.__str__()
            ret += "    {:12s} : {}".format("Integrator", txt)
            ret += "\n"
        #else:
        #    ret = ret[:-9]

        # If the object has a writer
        if "_writer" in self.__dict__.keys():
            writer = self.__dict__["_writer"]
            txt = "\033[93mnot specified\033[0m"
            if writer is not None:
                txt = writer.__str__()
            ret += "    {:12s} : {}".format("Writer", txt)
            ret += "\n"
        #else:
        #    ret = ret
    
        return ret

    def _cyclethrough(self, haystack, needle):
        """Function that cycles through object structure to find object.
        This is meant to find an object within a frame structure and replace it with another object.
        
        Parameters
        ----------
        haystack : object
            Uppermost object to search through
        needle : object
            Object to look for in haystack
            
        Returns
        -------
        dict, key
            Dictionary and key of object location"""

        for key, val in haystack.__dict__.items():
            if key == "_owner": continue    # To prevent recursion
            if val is needle:
                return haystack.__dict__, key
            else:
                if hasattr(val, "__dict__"):
                    self._cyclethrough(val, needle)


class Group(AbstractGroup):
    """Class for grouping fields.
    
    Parameters
    ----------
    owner : Frame
        Parent frame object to which the group belongs
    updater : Updater, callable or list, optional, default : None
        Updater for group update
    systole : Updater, callable or list, optional, default : None
        Systole for group update
    diastole : Updater, callable or list, optional, default : None
        Diastole for group update 
    description : string, optional, default : None
        Descriptive string for the group
        
    Notes
    -----
    When <group>.update() is called the group will be updated according the instruction set by <group>.updater.
    Before the group is updated the systole updater is called. After the group update the diastole updater is called.
    The updaters, systoles, and diastoles for groups can either be of type Updater, can be a callable function which
    executes the desired operation, can be a list of strings with the names of the group's attributes whose update
    function should be executes in exactly this order, or can be None, if no operation should be performed. If it is
    set to a callable function the function's only argument has to be the parent Frame object.
    
    Examples
    --------
    >>> grp = Group(sim, description="My group")
    """
    
    __name__ = "Group"
    
    def __init__(self, owner, updater=None, systole=None, diastole=None, description=None):
        self._description = description
        self._owner = owner
        self.updater = updater
        self.systole = systole
        self.diastole = diastole
        
    def update(self, *args, **kwargs):
        """Function to update the object."""
        
        self._update(self._systole, *args, **kwargs)
        self._update(self._updater, *args, **kwargs)
        self._update(self._diastole, *args, **kwargs)

    def _update(self, u, *args, **kwargs):
        """This functions calls either the updater directly or executes the update functions of the list entries"""
        if isinstance(u, Updater):
            u.update(self._owner, *args, **kwargs)
        elif isinstance(u, list):
            for val in u:
                self.__dict__[val].update(*args, **kwargs)
            
    def addfield(self, name, value, updater=None, systole=None, diastole=None, description=None, constant=False):
        """Function to add a field to the object.
        
        Parameters
        ----------
        name : string
            Name of the field
        value : number, array, string
            Initial value of the field. Needs to have already the correct type and shape
        updater : Updater, callable or list, optional, default : None
            Updater for field update
        systole : Updater, callable or list, optional, default : None
            Systole for field update
        diastole : Updater, callable or list, optional, default : None
            Diastole for field update 
        description : string, optional, default : None
            Descriptive string for the field
        constant : boolean, optional, default : False
            Should this field be constant?
            
        Notes
        -----
        When <field>.update() is called the field will be updated according return value of the updater..
        Before the field is updated the systole updater is called. After the group update the diastole updater is called.
        The updaters, systoles, and diastoles for fields can either be of type Updater, can be a callable function which
        executes the desired operation, or can be None, if no operation should be performed. If it is set to a callable
        function the function's only argument has to be the parent Frame object. The callable function of the updater has
        to return the new value of the field.
        
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
        self.__dict__[name] = Field(self._owner, value, updater=updater, systole=systole, diastole=diastole, description=description, constant=constant)

    def addgroup(self, name, updater=None, systole=None, diastole=None, description=None):
        """Function to add a group to the object.
        
        Parameters
        ----------
        name : string
            Name of the group
        updater : Updater, callable or list, optional, default : None
            Updater for group update
        systole : Updater, callable or list, optional, default : None
            Systole for group update
        diastole : Updater, callable or list, optional, default : None
            Diastole for group update 
        description : string, optional, default : None
            Descriptive string for the group
            
        Notes
        -----
        When <group>.update() is called the group will be updated according the instruction set by <group>.updater.
        Before the group is updated the systole updater is called. After the group update the diastole updater is called.
        The updaters, systoles, and diastoles for groups can either be of type Updater, can be a callable function which
        executes the desired operation, can be a list of strings with the names of the group's attributes whose update
        function should be executes in exactly this order, or can be None, if no operation should be performed. If it is
        set to a callable function the function's only argument has to be the parent Frame object.
        
        See Also
        --------
        addfield : Function to add a field to the object
        
        Examples
        --------
        >>> sim.addgroup("mygroup, description="My Group")
        >>> sim.mygroup
        Group (My Group):
        """
        self.__dict__[name] = Group(self._owner, updater=updater, systole=systole, diastole=diastole, description=description)


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

    def __new__(cls, owner, value, updater=None, systole=None, diastole=None, description=None, constant=False):
        obj = np.asarray(value).view(cls)
        obj._owner = owner
        obj._updater = obj._constructupdater(updater)
        obj._systole = obj._constructupdater(systole)
        obj._diastole = obj._constructupdater(diastole)
        obj.description = description
        obj._constant = constant
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self._owner = getattr(obj, "_owner", None)
        self._updater = getattr(obj, "_updater", None)
        self._systole = getattr(obj, "_systole", None)
        self._diastole = getattr(obj, "_diastole", None)
        self.description = getattr(obj, "description", None)
        self._constant = getattr(obj, "_constant", False)
    
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
        """Function to update the object."""
        self._update(self.systole, *args, **kwargs)
        self._update(self.updater, *args, upd=True, **kwargs)
        self._update(self.diastole, *args, **kwargs)

    def derivative(self):
        pass

    def _update(self, u, *args, upd=False, **kwargs):
        """This functions calls either the updater directly or executes the update functions of the list entries"""
        if upd:
            # Here we're not in systole or diastole. So we're updating.
            if isinstance(u, Updater):
                self._setvalue(u.update(self._owner, *args, **kwargs))
            elif isinstance(u, list):
                # Field updater cannot work with lists
                raise ValueError("Cannot update field with list.")
        else:
            # Here we're in systole or diastole.
            if isinstance(u, Updater):
                u.update(self._owner, *args, **kwargs)
            elif isinstance(u, list):
                for val in u:
                    self.__dict__[val].update(*args, **kwargs)
        
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
        ret = "{:6s}".format(str(self.__name__))
        if((self._description != "") and (self._description != None)):
            ret += " ({})".format(self._description)
        if self._constant:
            ret += ", \033[95mconstant\033[0m"
        return ret

    def __repr__(self):
        ret = "{}\n{}\n{}".format(self.__str__(), "-" * len(self.__str__()), np.ndarray.__str__(self.getfield(self.dtype)))
        return ret

    def makeintegrationvariable(self, snapshots=[]):
        """This function converts the field to an integration variable. This action cannot be reverted.
        Be advised that the updater of an integration variable should return the desired stepsize and
        the update function is adding the stepsize to the current value.
        
        Parameters
        ----------
        snapshots, list, array, optional, default : []
            Snapshots at which outputs should be written"""
        intvar = Intvar(self._owner, self.getfield(self.dtype), updater=self.updater, systole=self.systole, diastole=self.diastole, snapshots=snapshots, description=self._description)
        # Replace the old Field with the new Intvar
        d, k = self._cyclethrough(self._owner, self)
        d[k] = intvar


class Intvar(Field):
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

    def __new__(cls, owner, value=0, snapshots=[], updater=None, systole=None, diastole=None, description=None):
        obj = super().__new__(cls, owner, value, updater=updater, systole=systole, diastole=diastole, description=description, constant=False)
        obj.snapshots = snapshots
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        super().__array_finalize__(obj)
        self.snapshots = getattr(obj, "snapshots", [])

    def _update(self, u, *args, upd=False, **kwargs):
        """This functions calls either the updater directly or executes the update functions of the list entries"""
        if upd:
            # Here we are not in sytole or diastole. So we're updating.
            if isinstance(u, Updater):
                self._setvalue(self+self.stepsize)
            else:
                # We actually need an updater for an integration variable to progress the simulation
                raise TypeError("Can only update field with an updater.")
        else:
            # Here we're in systole or diastole
            if isinstance(u, Updater):
                u.update(self._owner, *args, **kwargs)
            elif isinstance(u, list):
                for val in u:
                    self.__dict__[val].update(*args, **kwargs)

    @property
    def stepsize(self):
        if not isinstance(self.updater, Updater):
            raise RuntimeError("You need to set an Updater for stepsize function first.")
        return np.minimum(self.updater.update(self._owner), self.maxstepsize)

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
        ret = "{:6s}".format(str(self.__name__))
        if((self._description != "") and (self._description != None)):
            ret += " ({})".format(self._description)
        ret += ", \033[95mIntegration variable\033[0m"
        return ret


class Updater():
    """Class that manages how a group or field is updated
    
    Parameter
    ---------
    func : callable
        Function that is called when update function is called.
        
    Examples
    --------
    >>> myupdater = Updater(myfunction)"""

    __name__ = "Updater"
    
    def __init__(self, func):
        if not hasattr(func, '__call__'):
            raise TypeError("<func> is not callable.")
        self._func = func
        
    def update(self, owner, *args, **kwargs):
        """Function that is called when group or field to which Updater belongs is being updated."""
        return self._func(owner, *args, **kwargs)

    def __str__(self):
        return "{:6s}".format(str(self.__name__))

    def __repr__(self):
        return self.__str__()


class Frame(Group):
    """Frame class.
    This is the parent object that contains all other objects
    
    Parameters
    ----------
    description : string, optional, default : None
        Descriptive string of the frame object
    writer : Writer, optional, default : None
        Object of type Writer fir writing output files
        
    Examples
    --------
    >>> sim = Frame(description="My Simulation")
    >>> sim
    Frame (My Simulation):"""

    __name__ = "Frame"
    _integrator = None
    _writer = None
    
    def __init__(self, description=None, integrator=None, writer=None):
        self.description = description
        self.integrator = integrator
        self.writer = writer
        self._owner = self

    @property
    def integrator(self):
        return self._integrator
    @integrator.setter
    def integrator(self, integrator):
        if integrator is not None and type(integrator) is not Integrator:
            raise TypeError("<simframe.Frame.integrator> hat to be of type <simframe.integration.integrator.Integrator> or None.")
        self._integrator = integrator

    @property
    def writer(self):
        return self._writer
    @writer.setter
    def writer(self, writer):
        if writer is not None and type(writer) is not Writer:
            raise TypeError("<simframe.Frame.writer> hat to be of type <simframe.io.Writer> or None.")
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

        if self.writer is not None:
            self.writer.write(self, i, filename, forceoverwrite, **kwargs)

    def run(self):

        if not isinstance(self.integrator, Integrator):
            raise RuntimeError("No integrator set.")

        # Write initial conditions
        if self.integrator.var <= self.integrator.var.snapshots[0]:
            self.writeoutput(0)

        starting_index = np.argmin(self.integrator.var >= self.integrator.var.snapshots)
        for i in range(starting_index, len(self.integrator.var.snapshots)):

            varnext = self.integrator.var.nextsnapshot
            while self.integrator.var < varnext:
                self.integrator.integrate()
                self.integrator.var.update()
                self.update()
            
            self.writeoutput(i+1)
            


class Integrator:
    
    __name__ = "Integrator"

    _description = None
    _instructions = []
    _var = None

    def __init__(self, var, instructions=[], description=None):
        self.var = var
        self.description = description
        self.instructions = instructions

    def __str__(self):
        ret = str(self.__name__)
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret

    def __repr__(self):
        ret = self.__str__()
        return ret

    def integrate(self):
        status = False
        while(not status):
            ret = []
            for inst in self.instructions:
                ret.append(inst(self.var.stepsize))
            if not np.any(ret == False):
                status = True
        for i, inst in enumerate(self.instructions):
            if inst.instant: continue
            if not ret[i]: continue
            inst.Y += ret[i]


    @property
    def instructions(self):
        return self._instructions
    @instructions.setter
    def instructions(self, value):
        if not isinstance(value, list):
            raise TypeError("<instructions> has to be of type list.")
        self._instructions = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if not isinstance(value, (str, type(None))):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    @property
    def var(self):
        return self._var
    @var.setter
    def var(self, value):
        if not isinstance(value, Intvar):
            raise TypeError("<var> has to be of type Intvar.")
        self._var = value