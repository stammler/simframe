from simframe.frame.abstractgroup import AbstractGroup
from simframe.frame.group import Group
from simframe.io.reader import Reader
from simframe.io.writer import Writer
from simframe.utils.color import colorize

from collections import deque
import copy
import numbers
import numpy as np
from types import SimpleNamespace


class _namespacewriter(Writer):
    """Modified class to write ``Frame`` object to namespace"""

    _buffer = deque([])

    def __init__(self, func, datadir="data", zfill=0, dumping=True, reader=None, description="Temporary namespace writer"):
        """
        Parameters
        ----------
        func : callable
            Function that writes Frame object.
        datadir : str, optional, default : "data"
            Path to data directory. Only used for dump files
        zfill : int, optional default : 4
            leading zeros of output numbers
        dumping : boolean, optional, default : True
            if True dump files are written
        reader, Reader, optional, default : None
            Reader to read the outputs
        description : str, optional, default : "Namespace writer"
        """
        super().__init__(func, datadir=datadir, filename="_", zfill=zfill, extension="",
                         overwrite=False, dumping=dumping, reader=reader, description=description)

    def __repr__(self):
        ret = self.__str__()+"\n"
        ret += "-" * (len(ret)-1) + "\n"
        ret += "    Data directory : {}\n".format(self.datadir)
        ret += "    Dumping        : {}\n".format(
            colorize(self.dumping, "yellow") if not self.dumping else self.dumping)
        ret += "    Verbosity      : {}".format(self.verbosity)
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
        if self.verbosity > 0:
            num = str(i).zfill(self._zfill)
            msg = "Saving frame {}".format(num)
            print(msg)
        if self.dumping:
            self.writedump(owner)

    def reset(self):
        """This resets the namespace.

        Notes
        -----
        WARNING: This cannot be undone."""
        self._buffer = deque([])


class namespacereader(Reader):
    """Class to read namespace outputs"""

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
              list, np.ndarray, str)

    for key, val in o.__dict__.items():

        if key.startswith("_"):
            continue

        if val is not None and isinstance(val, direct):
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
        Namespace of concatenated dicts
    """
    N = len(dicts)
    ret = {}
    for key, val in dicts[0].items():
        if isinstance(val, dict):
            d = deque([])
            for i in range(N):
                d.append(dicts[i][key])
            ret[key] = _zip(d)
        else:
            l = deque([])
            for i in range(N):
                v = dicts[i][key]
                if hasattr(v, "shape") and v.shape == (1,):
                    v = v[0]
                l.append(v)
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
