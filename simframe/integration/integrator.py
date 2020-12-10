from collections import deque
import numpy as np

from simframe.frame.abstractgroup import AbstractGroup
from simframe.frame.heartbeat import Heartbeat
from simframe.frame.intvar import IntVar
from simframe.integration.instruction import Instruction
from simframe.integration.schemes import update


class Integrator:
    """``Integrator`` class that manages the integration instructions"""

    __name__ = "Integrator"

    _description = ""
    _instructions = []
    _failop = Heartbeat(None)
    _finalizer = Heartbeat(None)
    _maxit = 500
    _preparator = Heartbeat(None)
    _var = None

    def __init__(self, var, instructions=[], failop=None, preparator=None, finalizer=None, maxit=500, description=""):
        """Integrator

        Parameters
        ----------
        var : IntVar
            Integration variable that controls the integration
        instructions : list of Instruction, optional, default : None
            List of the instegration instructions
        failop : Heartbeat, Updater, callable, or None, optional, default : None
            Fail operation that is executed if any instruction failed
        preparator : Heartbeat, Updater, callable, or None, optional, default : None
            Heartbeat that will be executed before the integration
        finalizer : Heartbeat, Updater, callable, or None, optional, default : None
            Heartbeat that will be executed after the integration
        maxit : int, optional, default : 5000
            Maximum number of integration iterations
        description : str, optional, default : ""
            Description of integrator"""
        self.description = description
        self.failop = failop
        self.finalizer = finalizer
        self.instructions = instructions
        self.maxit = maxit
        self.preparator = preparator
        self.var = var

    def __str__(self):
        return AbstractGroup.__str__(self)

    def __repr__(self):
        return self.__str__()

    @property
    def description(self):
        '''Description of integrator'''
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    @property
    def failop(self):
        '''``Heartbeat`` objects that is called if any integration ``Instruction`` returned ``False``'''
        return self._failop

    @failop.setter
    def failop(self, value):
        if isinstance(value, Heartbeat):
            self._failop = value
        else:
            self._failop = Heartbeat(value)

    @property
    def finalizer(self):
        '''``Heartbeat`` object that is called after the integration was successful.'''
        return self._finalizer

    @finalizer.setter
    def finalizer(self, value):
        if isinstance(value, Heartbeat):
            self._finalizer = value
        else:
            self._finalizer = Heartbeat(value)

    @property
    def instructions(self):
        '''List of integration ``Instructions`` that will be executed in that order.'''
        return self._instructions

    @instructions.setter
    def instructions(self, value):
        if not isinstance(value, list):
            raise TypeError("<instructions> has to be of type list.")
        for val in value:
            if not isinstance(val, Instruction):
                raise TypeError(
                    "<instructions> has to be list of Instructions")
        self._instructions = value

    @property
    def maxit(self):
        '''Maximum number of integration tries until program will be aborted.'''
        return self._maxit

    @maxit.setter
    def maxit(self, value):
        value = np.int(value)
        if not isinstance(value, np.int):
            raise TypeError("maxit has to be of type int.")
        if value <= 0:
            raise ValueError("maxit has to be larger 0.")
        self._maxit = value

    @property
    def preparator(self):
        '''``Heartbeat`` object that is called before the integration instructions will be executed.'''
        return self._preparator

    @preparator.setter
    def preparator(self, value):
        if isinstance(value, Heartbeat):
            self._preparator = value
        else:
            self._preparator = Heartbeat(value)

    @property
    def var(self):
        '''The integration variable ``IntVar`` that is associated with this ``Integrator``.'''
        return self._var

    @var.setter
    def var(self, value):
        if not isinstance(value, IntVar):
            raise TypeError("<var> has to be of type Intvar.")
        self._var = value

    def integrate(self):
        """Method that executes one integration step."""
        # Preparation
        self._prepare()
        # Loop over all instructions. Exit the loop only if all instructions were executed successfully
        # And count the loops
        i = 0
        status = False
        while(not status):
            # The suggested stepsize has to be reset in the beginning of every try.
            # We therefore have to copy the current stepsize in case the user is returning
            # the suggested stepsize in the stepsize function.
            stepsize = self.var.stepsize.copy()
            self.var._suggested = None
            if i >= self.maxit:
                raise StopIteration(
                    "Maximum number of integration attempts exceeded.")
            # Safe all return values in list
            ret = deque([])
            for inst in self.instructions:
                ret.append(inst(stepsize))
            # If no instruction returned False, Integration was successful. Exit the loop.
            if not np.any(np.array(ret) == False):
                status = True
            else:
                # Reset buffers if integration failed
                for inst in self.instructions:
                    inst.Y._buffer = None
                self._failoperation()
                i += 1
        # Update the variables.
        for i, inst in enumerate(self.instructions):
            if inst.Y._buffer is None:
                continue
            update(None, inst.Y, None)
        # Store the taken stepsize
        self.var._prevstepsize = stepsize
        # Finalization
        self._finalize()

    def _failoperation(self, *args, **kwargs):
        """This operation will be executed if any integration ``Instruction`` failed and before the
        ``Integrator`` tries it again. It will execute the ``Heartbeat`` of ``Integrator.failop``.

        Parameters
        ----------
        args : additional positional arguments
        kwargs : additional keyword arguments

        Notes
        -----
        args, and kwargs will only be passed to the ``updater``, NOT ``systole`` and ``diastole``."""
        self.failop.beat(self.var._owner, *args, **kwargs)

    def _prepare(self, *args, **kwargs):
        """This operation will be executed before the integration. It will execute the
        ``Heartbeat`` of ``Integrator.preparator``.

        Parameters
        ----------
        args : additional positional arguments
        kwargs : additional keyword arguments

        Notes
        -----
        args, and kwargs will only be passed to the ``updater``, NOT ``systole`` and ``diastole``."""
        self.preparator.beat(self.var._owner, *args, **kwargs)

    def _finalize(self, *args, **kwargs):
        """This operation will be executed before the integration. It will execute the
        ``Heartbeat`` of ``Integrator.finalizer``.

        Parameters
        ----------
        args : additional positional arguments
        kwargs : additional keyword arguments

        Notes
        -----
        args, and kwargs will only be passed to the ``updater``, NOT ``systole`` and ``diastole``."""
        self.finalizer.beat(self.var._owner, *args, **kwargs)
