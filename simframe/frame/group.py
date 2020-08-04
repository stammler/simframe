from simframe.frame.abstractgroup import AbstractGroup
from simframe.frame.field import Field
from simframe.frame.intvar import IntVar
from simframe.frame.updater import Updater

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
    
    def __init__(self, owner, updater=None, description=None):
        self._description = description
        self._owner = owner
        self.updater = updater
            
    def __setattr__(self, name, value):
        """Function to set an attribute including fields."""
        if isinstance(value, Field):
            self.__dict__[name] = value
        elif name in self.__dict__ and isinstance(self.__dict__[name], Field):
            self.__dict__[name]._setvalue(value)
        else:
            super().__setattr__(name, value)
        
    def update(self, *args, **kwargs):
        """Function to update the object."""
        self.updater.beat(self._owner, *args, **kwargs)
            
    def addfield(self, name, value, updater=None, differentiator=None, description=None, constant=False):
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
        self.__dict__[name] = Field(self._owner, value, updater=updater, differentiator=differentiator, description=description, constant=constant)

    def addintegrationvariable(self, name, value, snapshots=[], updater=None, description=None):
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
        self.__dict__[name] = IntVar(self._owner, value, updater=updater, snapshots=snapshots, description=description)

    def addgroup(self, name, updater=None, description=None):
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
        self.__dict__[name] = Group(self._owner, updater=updater, description=description)

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