import numpy as np

from simframe.frame.field import Field
from simframe.integration.scheme import Scheme
from simframe.utils.color import colorize


class Instruction(Scheme):
    """Integration ``Instruction`` that controls the execution of an integration ``Scheme``."""

    __name__ = "Instruction"

    _Y = None
    _fstep = 1.

    def __init__(self, scheme, Y, fstep=1., controller={}, description=""):
        """Integration instruction

        Parameters
        ----------
        scheme : Scheme
            Integration scheme
        Y : Field
            Variable to be integrated
        fstep : float, optional, default : 1.0
            Fraction of stepsize that this scheme should be used
        controller : dict, optional, default : {}
            Additional keyword arguments passed to integration scheme
        description : str, optional, default : ""
            Description of integration instruction"""
        super().__init__(scheme, controller, description)
        self.Y = Y
        self.fstep = fstep

    @property
    def Y(self):
        '''The ``Field`` to be integrated'''
        return self._Y

    @Y.setter
    def Y(self, value):
        if not isinstance(value, Field):
            raise TypeError("<Y> has to be of type Field.")
        self._Y = value

    @property
    def fstep(self):
        '''Fraction of step size the ``Scheme`` will be applied to ``Field``'''
        return self._fstep

    @fstep.setter
    def fstep(self, value):
        value = np.float(value)
        if value <= 0. or value > 1.:
            msg = "{}: {}".format(
                colorize("Warning", "yellow"), "<fstep> is not in (0, 1].")
            print(msg)
        self._fstep = value

    def __call__(self, dx=None):
        """Execution of the integration instruction

        Parameters
        ----------
        dx : IntVar, optional, default : None
            Stepsize of the integration variable

        Return
        ------
        Y1 : Field
            New value of the variable to be integrated"""
        x0 = self.Y._owner.integrator.var
        Y0 = self.Y
        ret = self.scheme(x0, Y0, self.fstep*dx, **self.controller)
        if ret is False:
            return False
        if ret is True:
            return ret
        else:
            self.Y._buffer = ret
            return True
