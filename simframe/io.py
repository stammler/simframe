import h5py
import numbers
import numpy as np
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
    options : dict, optional, default : {}
        Optional keyword arguments that need to be passed to writing algorithm
    
    Example filename:
    <datadir>/<data>0001.<extension>"""

    __name__ = "Writer"

    def __init__(self, func, datadir="data", filename="data", zfill=4, extension="out", overwrite=False, description=None, options={}):
        self._func = func
        self.datadir = datadir
        self.filename = filename
        self.zfill = zfill
        self.extension = extension
        self.overwrite = overwrite
        self.description = description
        self.options = options

    @property
    def overwrite(self):
        return self._overwrite
    @overwrite.setter
    def overwrite(self, value):
        if not isinstance(value, np.int):
            raise TypeError("<overwrite> has to be of type bool.")
        if value:
            self._overwrite = True
        else:
            self._overwrite = False

    def checkdatadir(self, datadir=None, createdir=False):
        """Function checks if data directory exists and creates it if desired.
        
        Parameters
        ----------
        datadir : string, optinal, default : None
            Datadirectory to be checked. If None it assumes the data directory of the parent writer.
        createdir : boolen, optional, default : False
            If True function creates data directory if it does not exist.
            
        Returns
        -------
        datadirexists : boolean
            True if directory exists, False if not"""
        
        datadir = self.datadir if datadir is None else datadir

        if not os.path.exists(self.datadir) and createdir:
            msg = "Creating data directory '{:s}'.".format(self.datadir)
            print(msg)
            os.makedirs(self.datadir)

        return os.path.exists(self.datadir)

    def __str__(self):
        ret = str(self.__name__)
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret

    def __repr__(self):
        ret = self.__str__()+"\n"
        ret += "-" * (len(ret)-1) + "\n"
        ret += "    Data directory : {}\n".format(self.datadir)
        ret += "    File names     : {}\n".format(self._getfilename(0))
        ret += "    Overwrite      : {}\n".format("\033[93m{}\033[0m".format(self.overwrite) if self.overwrite else self.overwrite)
        ret += "    options        : {}".format(self.options)
        return ret

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
            self.checkdatadir(createdir=True)
        if not forceoverwrite:
            if not self.overwrite:
                if os.path.isfile(filename):
                    raise RuntimeError("File {} already exists.".format(filename))
        self._func(sim, filename, **self.options, **kwargs)
        msg = "Writing file \033[94m'{}'\033[0m".format(filename)
        print(msg)


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

    if obj._description is not None and prefix == "":
        file.create_dataset(
            "description",
            data=obj._description
        )

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


hdf5writer = Writer(_hdf5wrapper, extension="hdf5", description="HDF5 file format using h5py", options={"com":"lzf", "comopts":None})