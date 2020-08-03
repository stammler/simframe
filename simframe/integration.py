import numpy as np
from simframe.frame import Field

class Scheme:

    __name__ = "Scheme"

    _scheme = None

    def __init__(self, scheme, description=""):
        self.scheme = scheme
        self.description = description

    @property
    def scheme(self):
        return self._scheme
    @scheme.setter
    def scheme(self, value):
        if not hasattr(value, "__call__"):
            raise TypeError("Scheme function needs to be callable.")
        self._scheme = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if not isinstance(value, (str, type(None))):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    def __call__(self, dx, Y):
        return self.scheme(dx, Y)

    def __str__(self):
        ret = str(self.__name__)
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret

    def __repr__(self):
        return self.__str__()


class Instruction(Scheme):

    __name__ = "Instruction"

    _Y = None
    _fstep = 1.
    _instant = False

    def __init__(self, scheme, Y, fstep=1., instant=False, description=""):
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
        ret = self.scheme(self.fstep*dx, self.Y)
        if self.instant:
            if not ret:
                raise RuntimeError("Integration scheme failed with instant tag.")
            self.Y += ret
            return True
        else:
            return ret



def _f_expl_1_euler(dx, Y):
    return dx*Y.updater.update(Y.owner, Y)
expl_1_euler = Scheme(_f_expl_1_euler, description="Explicit 1st order Euler")