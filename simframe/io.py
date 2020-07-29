import os


class Writer(object):
    """Class for writing outputs
    
    Parameters
    ----------
    func : callable
        Function that is writing the outputs to file
    datadir : string, optional, default : "data"
        relative path to data directory
    filename : string, optional, default : "data"
        basic name of the files to be written
    zfill : int, optional, default : 4
        leading zeros of numbered files
    extension : string, optional, default : "out"
        filename extension of the data files
    overwrite : boolean, optional, default : False
        If existing files should be overwritten
    
    Example filename:
    <datadir>/<data>0001.<extension>
    """

    def __init__(self, func, datadir="data", filename="data", zfill=4, extension="out", overwrite=False):
        self._func = func
        self.datadir = datadir
        self.filename = filename
        self.zfill = zfill
        self.extension = extension
        self.overwrite = overwrite

    def checkdatadir(self):
        """Function checks if data directory exists and creates it if not."""
        
        if not os.path.exists(self.datadir):
            msg = "Creating data directory '{:s}'.".format(self.datadir)
            print(msg)
            os.makedirs(self.datadir)

    def _getfilename(self, i):
        """This function creates <path>/<filename> for a given output number

        Parameters
        ----------
        i : integer
            Number of output

        Returns
        -------
        filename : str
            The constructed filename"""

        # Removing . from extension if given
        ext = self.extension
        if ext[0] != ".":
            ext = "." + ext

        number = str(i).zfill(self.zfill)
        filename = self.filename + number + ext

        return os.path.join(self.datadir, filename)

    def write(self, sim, i, filename, forceoverwrite, **kwargs):
        """Writes output to file
        
        Parameters
        ----------
        filname : string
            Path to file to be written
        i : int
            Number of output
        filename : string
            If this is not "" the writer will use this filename instead of the standard scheme
        forceoverwrite : boolean
            If True it will forces and overwrite of the file if it exists."""
        
        if filename == "":
            filename = self._getfilename(i)
            self.checkdatadir()
        if not forceoverwrite:
            if not self.overwrite:
                if os.path.isfile(filename):
                    raise RuntimeError("File {} already exists.".format(filename))
        self._func(sim, filename, **kwargs)


def _hdf5wrapper(obj, filename, com="lzf", comopts=None):
    """Wrapper to write object to hdf5 file.

    This function recursively calls a another functions thats goes through the object tree.

    Parameters:
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

    import h5py

    with h5py.File(filename, "w") as hdf5file:
            _writehdf5(obj, hdf5file, com=com, comopts=comopts)

def _writehdf5(obj, file, com="lzf", comopts=None, prefix=""):
    """Writes a given object to a h5py file.

    By default all attributes of the object are written out, excluding the ones that start with an underscore.

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
    import numbers
    import numpy as np

    for key, val in obj.__dict__.items():

        # Ignore private variables
        if key.startswith('_'):
            continue

        name = prefix + key

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


hdf5 = Writer(_hdf5wrapper)