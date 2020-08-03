import numpy as np

from simframe.frame.intvar import IntVar

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
        if not isinstance(value, IntVar):
            raise TypeError("<var> has to be of type Intvar.")
        self._var = value