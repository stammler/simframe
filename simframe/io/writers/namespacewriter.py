from simframe.frame.abstractgroup import AbstractGroup
from simframe.frame.group import Group
from simframe.io.reader import Reader
from simframe.io.writer import Writer

import copy
import numbers
import numpy as np
from types import SimpleNamespace


class _namespacewriter(Writer):
    """Modified class to write Frame object to namespace"""

    _buffer = []

    def __init__(self, func, zfill=0, reader=None, description="Temporary namespace writer"):
        """
        Parameters
        ----------
        func : callable
            Function that writes Frame object.
        zfill : int, optional default : 4
            leading zeros of output numbers
        reader, Reader, optional, default : None
            Reader to read the outputs
        description : str, optional, default : "Namespace writer"
        """
        super().__init__(func, datadir="", filename="_", zfill=zfill, extension="",
                         overwrite=False, reader=reader, description=description)

    def __str__(self):
        ret = AbstractGroup.__str__(self)
        return ret

    def __repr__(self):
        ret = self.__str__()+"\n"
        ret += "-" * (len(ret)-1) + "\n"
        ret += "    Writer to convert Frame objects into namespace.\n"
        ret += "    Can be accessed with <Writer>.read.output(i) and\n"
        ret += "    <Writer>.read.all()."
        return ret

    def _getfilename(self):
        """Filenames are not required for this class."""
        pass

    def write(self, owner, i=0, forceoverwrite=False, filename=""):
        """Writes output to namespace

        Parameters
        ----------
        owner : Frame
            Parent frame object
        i : int
            Not used in this class
        forceoverwrite : boolean
            Not used in this class
        filename : string
            Not used in this class"""
        self._buffer.append(self._func(owner))
        num = str(i).zfill(self._zfill)
        msg = "Saving frame {}".format(num)
        print(msg)


class namespacereader(Reader):
    """Class to read namespaceoutputs"""

    def __init__(self, writer):
        super().__init__(writer)

    def all(self):
        """Reads all outputs

        Returns
        -------
        n : SimpleNamespace
            Namespace containing data"""
        return _zip(self._writer._buffer)

    def output(self, i):
        """Reading a single output

        Parameters
        ----------
        i : int
            Number of output to be read

        Returns
        -------
        n : SimpleNamespace
            Namespace of desired output"""
        if i >= len(self._writer._buffer):
            raise RuntimeError("Output {} does not exist.".format(i))

        return _converttodict(SimpleNamespace(**self._writer._buffer[i]))


def _converttodict(o):
    """Converts an object into a dictionary

    Parameters
    ----------
    o : object
        object

    Returns
    -------
    d : dict
        Nested dictionary with the data in Frame object

    Notes
    -----
    Attributes beginning with underscore _ are being ignored."""
    ret = {}

    # These things are written directy into the dictionary.
    direct = (numbers.Number, np.number, tuple,
              list, dict, np.ndarray, str, None)

    for key, val in o.__dict__.items():

        if key.startswith("_"):
            continue

        if isinstance(val, direct):
            ret[key] = copy.copy(val)
        else:
            ret[key] = _converttodict(val)

    return ret


def _zip(dicts):
    """Stitches together list of dicts and creates namespace

    Parameters
    ----------
    dicts : list
        list of dicts

    Returns
    -------
    n : SimpleNamespace
        Namespace of contanuated dicts
    """
    N = len(dicts)
    ret = {}
    for key, val in dicts[0].items():
        if isinstance(val, SimpleNamespace):
            d = []
            for i in range(N):
                d.append(dicts[i][key].__dict__)
            ret[key] = _zip(d)
        else:
            l = []
            for i in range(N):
                l.append(dicts[i][key])
            ret[key] = np.array(l)
    return SimpleNamespace(**ret)


def _writeframetonamespace(frame):
    """Takes a list of dicts and a frame, stitches them together and returns namespace.

    Paramters
    ---------
    frame : Frame
        Frame object to add

    Returns
    -------
    n : SimpleNamespace
        Namespace with data"""
    d = _converttodict(frame)
    return d


namespacewriter = _namespacewriter(
    _writeframetonamespace, reader=namespacereader, description="Namespace writer")
