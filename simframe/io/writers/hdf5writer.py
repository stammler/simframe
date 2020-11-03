import glob
import h5py
import numbers
import numpy as np
from types import SimpleNamespace
import os

from simframe.io.reader import Reader
from simframe.io.writer import Writer
from simframe.frame.field import Field


def _hdf5wrapper(obj, filename, com="lzf", comopts=None):
    """Wrapper to write object to HDF5 file.

    This function recursively calls a another functions thats goes through the object tree.

    Parameters
    ----------
    obj : object
        the object to be stored in a file
    filename : string
        path to file

    Keywords
    --------
    com : string
        compression method to be used by `h5py`
    comopt : compression_opts
        compression options, see `h5py.File`'s `create_dataset` for details
    """

    with h5py.File(filename, "w") as hdf5file:
        _writehdf5(obj, hdf5file, com=com, comopts=comopts)


def _writehdf5(obj, file, com="lzf", comopts=None, prefix=""):
    """Writes a given object to a h5py file.

    By default all attributes of the object are written out, excluding the ones that start with an underscore.
    Fields with attribute Field.save == False will be skipped.

    Parameters:
    ----------
    obj : object
        the object to be stored in a file
    file : hdf5 file
        open hdf5 file object

    Keywords
    --------
    com : string
        compression method to be used by `h5py`
    comopt : compression_opts
        compression options, see `h5py.File`'s `create_dataset` for details
    prefix : str
        a prefix prepended to the name of each attribute when storing with h5py
    """

    if hasattr(obj, "_description") and obj._description is not None and prefix == "":
        file.create_dataset(
            "description",
            data=obj._description
        )

    for key, val in obj.__dict__.items():

        # Ignore hidden variables
        if key.startswith('_'):
            continue
        # Skip fields that should not be stored
        if isinstance(val, Field) and val.save == False:
            continue

        name = prefix + key

        # Check if numpy.ndarray of strings and convert to list
        if isinstance(val, np.ndarray) and val.dtype.type is np.str_:
            val = val.tolist()

        # Check for number
        if isinstance(val, (numbers.Number, np.number)):
            file.create_dataset(
                name,
                data=val
            )
        # Check for tuple/list/dict
        elif type(val) in [tuple, list, dict]:
            # special case for list of strings
            if all([type(_v) == str for _v in val]):
                file.create_dataset(
                    name,
                    data=np.array(val, dtype=object),
                    dtype=h5py.special_dtype(vlen=str),
                    compression=com,
                    compression_opts=comopts)
            else:
                file.create_dataset(
                    name,
                    data=val,
                    compression=com,
                    compression_opts=comopts
                )
        # Check for string
        elif type(val) is str:
            file.create_dataset(
                name,
                data=val
            )
        # Check for Numpy array
        elif isinstance(val, np.ndarray):
            if val.shape == ():
                file.create_dataset(
                    name,
                    data=val,
                )
            else:
                file.create_dataset(
                    name,
                    data=val,
                    compression=com,
                    compression_opts=comopts
                )
        # Check for None
        elif val is None:
            file.create_dataset(
                name,
                data=0
            )
        # Other objects
        else:
            _writehdf5(val, file, com=com,
                       comopts=comopts, prefix=name + "/")


class hdf5reader(Reader):
    """Reader class for the HDF5 writer."""

    def __init__(self, writer):
        """HDF5 reader

        Parameters
        ----------
        writer : Writer
            Writer object to which the reaer belongs."""
        super().__init__(writer)

    def output(self, filename):
        """Reads a single output file.

        Parameters
        ----------
        filename : str
            Path to filename to be read

        Returns
        -------
        data : SimpleNamespace
            Namespace of data in file."""

        if not isinstance(filename, str):
            filename = self._writer._getfilename(filename)

        if not os.path.isfile(filename):
            raise RuntimeError("File does not exist.")

        with h5py.File(filename, "r") as hdf5file:
            return self._readgroup(hdf5file)

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
        files = self.listfiles()
        if files == []:
            raise RuntimeError("<datadir> does not exist or is empty.")
        if not isinstance(field, str):
            raise TypeError("<field> has to be of type string.")
        loc = field.replace(".", "/")
        ret = []
        for f in files:
            with h5py.File(f, "r") as hdf5file:
                A = np.array(hdf5file[loc][()])
                if A.shape == (1,):
                    ret.append(A[0])
                else:
                    ret.append(A)
        return np.array(ret)

    def _readgroup(self, gr):
        """Helper function that is iteratively called to get the depth of the data set.

        Parameters
        ----------
        gr : Group of type h5py._hl.group.Group
            The h5py data set to be read

        Returns
        -------
        data : SimpleNamespace
            Namespace of data"""
        ret = {}
        for ds in gr.keys():
            if isinstance(gr[ds], h5py._hl.group.Group):
                ret[ds] = self._readgroup(gr[ds])
            else:
                ret[ds] = gr[ds][()]
        return SimpleNamespace(**ret)


hdf5writer = Writer(_hdf5wrapper, extension="hdf5", description="HDF5 file format using h5py", options={
                    "com": "lzf", "comopts": None}, reader=hdf5reader)
