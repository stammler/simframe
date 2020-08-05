import numpy as np

from simframe.frame.field import Field
from simframe.integration.abstractscheme import AbstractScheme

class Instruction(AbstractScheme):
    """Integration instruction that controls the execution of integration schemes."""

    __name__ = "Instruction"

    _Y = None
    _fstep = 1.
    _instant = False

    def __init__(self, scheme, Y, fstep=1., instant=False, description=""):
        """Integration instruction
        
        Parameters
        ----------
        scheme : AbstractScheme
            Integration scheme
        Y : Field
            Variable to be integrated
        fstep : float, optional, default : 1.0
            Fraction of stepsize that this scheme should be used
        instant : boolean, optional, default : False
            If True the variable Y is updated right after performing the instruction successfully.
            If False if will be updated after all instructions have be executed.
        description : str, optional, default : ""
            Description of integration instruction
            
        Notes
        -----
        If the integration failed while the instant tag is True, a RuntimeError will be raised."""
        super().__init__(scheme, description)
        self.Y = Y
        self.fstep = fstep
        self.instant = instant

    @property
    def Y(self):
        return self._Y
    @Y.setter
    def Y(self, value):
        if not isinstance(value, Field):
            raise TypeError("<Y> has to be of type Field.")
        self._Y = value

    @property
    def fstep(self):
        return self._fstep
    @fstep.setter
    def fstep(self, value):
        value = np.float(value)
        if value <= 0. or value > 1.:
            msg = "\033[93mWarning:\033[0m <fstep> is not in (0, 1]."
            print(msg)
        self._fstep = value

    @property
    def instant(self):
        return self._instant
    @instant.setter
    def instant(self, value):
        if not isinstance(value, np.int):
            raise TypeError("<instantly> has to be of type bool.")
        if value:
            self._instant = True
        else:
            self._instant = False

    def __call__(self, dx):
        """Execution of the integration instruction
        
        Parameters
        ----------
        dx : IntVar
            Stepsize of the integration variable
            
        Return
        ------
        dY : Field
            Delta of the variable to be integrated"""
        ret = self.scheme(self.fstep*dx, self.Y)
        if self.instant:
            if not ret:
                raise RuntimeError("Integration scheme failed with instant tag.")
            self.Y += ret
            return True
        else:
            return ret