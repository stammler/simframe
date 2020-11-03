import numpy as np
from simframe.frame.abstractgroup import AbstractGroup
from simframe.frame.heartbeat import Heartbeat
from simframe.utils.color import colorize


class Field(np.ndarray, AbstractGroup):
    """Class for storing simulation quantities.

    In addition to ``Group``, ``Field`` can have an ``differentiator`` for calculating its derivative and/or an
    ``jacobinator`` for calculating its Jacobian. The function that is calculating the derivative needs the parent
    ``Frame`` object as first, the integration variable of type ``IntVar`` as second, and the ``Field`` itself as
    third positional argument

    ``Field`` behaves like ``numpy.ndarray`` and can perform the same numerical operations.

    Notes
    -----
    When ``Field.update()`` is called ``Field`` will be updated according return value of the ``updater`` of the
    ``Heartbeat`` object assigned to the ``Field``. The function that is updating ``Field`` needs the parent ``Frame``
    object as first positional argument."""

    __name__ = "Field"

    _differentiator = Heartbeat(None)
    _jacobinator = Heartbeat(None)
    _constant = False
    _save = True
    _buffer = None

    def __new__(cls, owner, value, updater=None, differentiator=None, jacobinator=None, description="", constant=False, save=True, copy=False):
        """Parameters
        ----------
        owner : Frame
            Parent frame object to which the field belongs
        value : number, array, string
            Initial value of the field. Needs to have correct type and shape
        updater : Heartbeat, Updater, callable or None, optional, default : None
            Instruction for field update
        differentiator : Heartbeat, Updater, callable or None, optional, default : None
            Instruction for calculating derivative
        jacobinator : Heartbeat, Updater, callable or None, optional, default : None
            Instruction for calculating the Jacobi matrix
        description : string, optional, default : ""
            Descriptive string for the field
        constant : boolean, optional, default : False
            True if the field is immutable.
        save : boolean, optional, default : True
            If False the field is not written into output files
        copy : boolean, optional, default : False
            If True <value> will be copied, not referenced"""
        obj = np.array(value, copy=copy).view(cls)
        if obj.shape == ():
            obj = np.array([value], copy=copy).view(cls)
        obj._owner = owner
        obj.updater = Heartbeat(updater)
        obj.differentiator = Heartbeat(differentiator)
        obj.jacobinator = Heartbeat(jacobinator)
        obj.description = description
        obj.constant = constant
        obj.save = save
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._owner = getattr(obj, "_owner", None)
        self.updater = getattr(obj, "updater", Heartbeat(None))
        self.differentiator = getattr(obj, "differentiator", Heartbeat(None))
        self.jacobinator = getattr(obj, "jacobinator", Heartbeat(None))
        self.description = getattr(obj, "description", "")
        self.constant = getattr(obj, "constant", False)

    def __str__(self):
        ret = AbstractGroup.__str__(self)
        if self.constant:
            ret += ", {}".format(colorize("constant", "purple"))
        return ret

    def __repr__(self):
        val = self.getfield(self.dtype)
        if val.shape == (1,):
            val = np.array(val[0])
        ret = "{}".format(np.ndarray.__str__(val))
        return ret

    def __format__(self, format_spec):
        if self.shape == (1,):
            return self[0].__format__(format_spec)
        else:
            return super().__format__(format_spec)

    @property
    def constant(self):
        '''If True, ``Field`` is immutable.'''
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
    def save(self):
        '''If False, ``Field`` will not be stored in output files.'''
        return self._save

    @save.setter
    def save(self, value):
        if isinstance(value, np.int):
            if value:
                self._save = True
            else:
                self._save = False
        else:
            raise TypeError("<value> hat to be of type bool.")

    @property
    def buffer(self):
        '''Temporary buffer that stores the new value of ``Field`` after successful integration.'''
        return self._buffer

    @buffer.setter
    def buffer(self, value):
        raise RuntimeError("Do not set buffer directly.")

    @property
    def differentiator(self):
        '''``Heartbeat`` object with instructions for calculating the derivative of ``Field``'''
        return self._differentiator

    @differentiator.setter
    def differentiator(self, value):
        if isinstance(value, Heartbeat):
            self._differentiator = value
        else:
            self._differentiator = Heartbeat(value)

    @property
    def jacobinator(self):
        '''``Heartbeat`` object with instructions for calculating the Jacobian of ``Field``'''
        return self._jacobinator

    @jacobinator.setter
    def jacobinator(self, value):
        if isinstance(value, Heartbeat):
            self._jacobinator = value
        else:
            self._jacobinator = Heartbeat(value)

    def update(self, *args, **kwargs):
        """Function to update the ``Field``.

        Parameter
        ---------
        args : additional positional arguments
        kwargs : additional keyword arguments

        Notes
        -----
        Function calls the Heartbeat object of the ``Field``. Additional positional and keyword arguments are only
        passed to the ``updater``, NOT to ``systole`` and ``diastole``."""
        self.updater.beat(self._owner, *args, Y=self, **kwargs)

    def derivative(self, x=None, Y=None, *args, **kwargs):
        """If ``differentiator`` or ``jacobinator`` is set, this returns the derivative of the ``Field``.

        Parameters
        ----------
        x : IntVar, optional, default : None
            Integration variable
            If None it uses the integration variable of the integrator of the parent Frame
        Y : Field, optional, default : None
            Derivative of Y with respect to the integration variable.
            If None it uses the field itself

        Returns
        -------
        deriv : derivative of the field according the differetiator or jacobinator

        Notes
        -----
        The function that calculates the derivative needs the parent ``Frame`` as first positional, the
        integration variable ``IntVar`` as second positional, and the ``Field`` itself as third positional argument.

        The ``differentiator`` is not set, it will try to calculate the derivative from the Jacobian.
        If ``jacobinator`` is also not set, it will return ``False``"""
        if x is None:
            if self._owner.integrator is None:
                raise RuntimeError("x not given and no integrator set.")
            if self._owner.integrator.var is None:
                raise RuntimeError(
                    "x not given and no integration variable set in integrator.")
            x = self._owner.integrator.var
        Y = Y if Y is not None else self
        deriv = self.differentiator.beat(self._owner, x, Y, *args, **kwargs)
        if deriv is not None:
            return deriv
        jac = self.jacobinator.beat(self._owner, x)
        if jac is not None:
            return jac @ Y
        else:
            # If no differentiator or jacobian is set we return zeros.
            return np.zeros_like(self)

    def jacobian(self, x=None, *args, **kwargs):
        """If ``jacobinator`` is set, this returns the Jacobi matrix of the ``Field``.

        Parameters
        ----------
        x : IntVar, optional, default : None
            Integration variable
            If None it uses the integration variable of the integrator of the parent Frame

        Returns
        -------
        jac : Jacobi matrix of the field according the differetiator

        The function that calculates the Jacobian needs the parent frame as first positional and the
        integration variable as second positional."""
        if x is None:
            if self._owner.integrator is None:
                raise RuntimeError("x not given and no integrator set.")
            if self._owner.integrator.var is None:
                raise RuntimeError(
                    "x not given and no integration variable set in integrator.")
            x = self._owner.integrator.var
        return self.jacobinator.beat(self._owner, x, *args, **kwargs)

    def _setvalue(self, value):
        """Function to set a value to the field. Direct assignement of values does overwrite the Field object.

        Parameters
        ----------
        value : number, array, string
            Value to be written into the field. Needs to have correct type and shape"""
        if self._constant:
            raise RuntimeError("Field is constant.")
        value = np.asarray(value)
        if value.shape == ():
            value = np.array([value])
        self.setfield(value, self.dtype)
