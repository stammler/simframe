import glob
import numpy as np
from types import SimpleNamespace
import os

class Reader(object):

    __name__ = "Reader"

    _description = ""
    _writer = None

    def __init__(self, writer, description=""):
        self.description = description
        self._writer = writer

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if not isinstance(value, (str, type(None))):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    def __str__(self):
        ret = str(self.__name__)
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret

    def __repr__(self):
        return self.__str__()

    def output(self, file):
        pass

    def listfiles(self, datadir=None):
        datadir = datadir or self._writer.datadir
        wildcard = os.path.join(datadir, self._writer.filename + "*." + self._writer.extension)
        files = glob.glob(wildcard)
        files = sorted(files, key=str.casefold)
        return files

    def all(self, datadir=None):
        files = self.listfiles(datadir)
        dicts = []
        for file in files:
            dicts.append(self.output(file).__dict__)
        return  self._zip(dicts)

    def _zip(self, dicts):
        N = len(dicts)
        ret = {}
        for key, val in dicts[0].items():
            if isinstance(val, SimpleNamespace):
                d = []
                for i in range(N):
                    d.append(dicts[i][key].__dict__)
                ret[key] = self._zip(d)
            else:
                l = []
                for i in range(N):
                    l.append(dicts[i][key])
                ret[key] = np.array(l)
        return SimpleNamespace(**ret)