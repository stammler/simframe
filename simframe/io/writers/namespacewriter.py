from simframe.frame.abstractgroup import AbstractGroup
from simframe.frame.field import Field
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
        self._buffer.clear()


class namespacereader(Reader):
    """Class to read namespace outputs"""

    def __init__(self, writer):
        super().__init__(writer)

    def all(self):
        """Functions that reads all output files and combines them into a single ``SimpleNamespace``.

        Returns
        -------
        dataset : SimpleNamespace
            Namespace of data set.

        Notes
        -----
        This function is reading one output files to get the structure of the data and
        calls ``read.sequence()`` for every field in the data structure."""
        if self._writer._buffer == deque([]):
            raise RuntimeError("Writer buffer is empty.")
        # Read first file to get structure
        data0 = self._writer._buffer[0]
        return self._expand(data0)

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

        return self._writer._buffer[i]

    def sequence(self, field):
        """Reading the entire sequence of a specific field.

        Parameters
        ----------
        field : string
            String with location of requested field

        Returns
        -------
        seq : array
            Array with requested values

        Notes
        -----
        ``field`` is addressing the values just as in the parent frame object.
        E.g. ``"groupA.groupB.fieldC"`` is addressing ``Frame.groupA.groupB.fieldC``."""
        if self._writer._buffer == deque([]):
            raise RuntimeError("Writer buffer is empty.")
        if not isinstance(field, str):
            raise TypeError("<field> has to be string.")
        loc = field.split(".")
        N = len(self._writer._buffer)
        ret = []
        for i in range(N):
            A = np.array(_getvaluefrombuffer(self._writer._buffer[i], loc))
            if A.shape == (1,):
                ret.append(A[0])
            else:
                ret.append(A)
        return np.array(ret)


def _getvaluefrombuffer(buf, loc):
    """Returns a requested value from buffer.
    Function is called recursively.

    Parameters
    ----------
    buf : dict
        Buffer object
    loc : list
        List of strings with the requested location within buf

    Returns
    -------
    ret : object
        Reqested value in buf at position loc"""
    if len(loc) > 1:
        return _getvaluefrombuffer(buf.__dict__[loc[0]], loc[1:])
    if not hasattr(buf, loc[0]):
        raise KeyError("Requested <field> does not exist.")
    return buf.__dict__[loc[0]]


def _converttonamespace(o):
    """Converts an object into a namespace

    Parameters
    ----------
    o : object
        object

    Returns
    -------
    ns : SimpleNamespace
        Nested namespace with the data in Frame object

    Notes
    -----
    Attributes beginning with underscore _ are being ignored.
    So are fields with Field.save == False."""
    ret = {}

    # These things are written directy into the dictionary.
    direct = (numbers.Number, np.number, tuple,
              list, np.ndarray, str)

    for key, val in o.__dict__.items():

        # Ignore hidden variables
        if key.startswith("_"):
            continue
        # Skip fields that should not be stored
        if isinstance(val, Field) and val.save == False:
            continue

        if val is not None and isinstance(val, direct):
            ret[key] = copy.copy(val)
        else:
            ret[key] = _converttonamespace(val)

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
    d = _converttonamespace(frame)
    return d


namespacewriter = _namespacewriter(
    _writeframetonamespace, reader=namespacereader, description="Namespace writer")
