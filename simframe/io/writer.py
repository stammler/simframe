from pathlib import Path

from simframe.io.reader import Reader
from simframe.io.dump import writedump
from simframe.frame.abstractgroup import AbstractGroup
from simframe.utils.color import colorize


class Writer(object):
    """General class for writing output files. It should be used as wrapper for customized ``Writer``."""

    __name__ = "Writer"

    def __init__(self, func, datadir="data", filename="data", zfill=4, extension="out", overwrite=False, dumping=True,
                 reader=None, verbosity=1, description="", options={}):
        """Parameters
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
        dumping : boolean, optional, default : True
            If True dump files will be written
        reader : Reader, optional, default : None
            reader to read files
        verbosity : int, optional, default : 1
            Verbosity of writer
        options : dict, optional, default : {}
            Optional keyword arguments that need to be passed to writing algorithm"""
        self._func = func
        self.datadir = datadir
        self.filename = filename
        self.zfill = zfill
        self.extension = extension
        self.overwrite = overwrite
        self.dumping = dumping
        self.description = description
        self.options = options
        self.verbosity = verbosity
        self.read = reader(self) if reader is not None else None

    @property
    def datadir(self):
        '''Data directory of output files.'''
        return self._datadir

    @datadir.setter
    def datadir(self, value):
        self._datadir = Path(value)

    @property
    def description(self):
        '''Description of ``Writer``.'''
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("description has to be of type str or None.")
        self._description = value

    @property
    def extension(self):
        '''Filename extension of output files.'''
        return self._extension

    @extension.setter
    def extension(self, value):
        if not isinstance(value, str):
            raise TypeError("extension has to be of type str.")
        if value.startswith("."):
            raise ValueError("extension should not start with '.'")
        self._extension = value

    @property
    def filename(self):
        '''Base filename of output files.'''
        return self._filename

    @filename.setter
    def filename(self, value):
        if not isinstance(value, str):
            raise TypeError("filename has to be of type str.")
        if value == "":
            raise ValueError("filename cannot be empty.")
        self._filename = value

    @property
    def options(self):
        '''Dictionary of keyword arguments passed to customized writing routine.'''
        return self._options

    @options.setter
    def options(self, value):
        if not isinstance(value, dict):
            raise TypeError("options has to be of type dict.")
        self._options = value

    @property
    def read(self):
        '''``Reader`` object for reading output files.'''
        return self._reader

    @read.setter
    def read(self, value):
        if isinstance(value, Reader) or (value is None):
            self._reader = value
        else:
            raise TypeError("<reader> has to be of type Reader or None.")

    @property
    def overwrite(self):
        '''If ``True`` existing output files will be overwritten.'''
        return self._overwrite

    @overwrite.setter
    def overwrite(self, value):
        if not isinstance(value, int):
            raise TypeError("<overwrite> has to be of type bool.")
        if value:
            self._overwrite = True
        else:
            self._overwrite = False

    @property
    def dumping(self):
        '''If ``True`` dump files will be written.'''
        return self._dumping

    @dumping.setter
    def dumping(self, value):
        if not isinstance(value, int):
            raise TypeError("<dumping> has to be of type bool.")
        if value:
            self._dumping = True
        else:
            self._dumping = False

    @property
    def verbosity(self):
        '''Verbosity of the writer.'''
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value):
        if not isinstance(value, int):
            raise TypeError("<verbosity> has to be of type int.")
        self._verbosity = value

    @property
    def zfill(self):
        '''Zero padding of numbered files names.'''
        return self._zfill

    @zfill.setter
    def zfill(self, value):
        if not isinstance(value, int):
            raise TypeError("zfill has to be integer.")
        self._zfill = value

    def checkdatadir(self, datadir=None, createdir=False):
        """Function checks if data directory exists and creates it if necessary.

        Parameters
        ----------
        datadir : string or None, optinal, default : None
            Data directory to be checked. If None it assumes the data directory of the parent writer.
        createdir : boolen, optional, default : False
            If True function creates data directory if it does not exist.

        Returns
        -------
        datadirexists : boolean
            True if directory exists, False if not"""

        datadir = self.datadir if datadir is None else datadir

        if (not datadir.exists()) and createdir:
            if self.verbosity > 0:
                msg = f"Creating data directory {str(datadir):s}."
                print(msg)
            datadir.mkdir(parents=True)

        return datadir.exists()

    def __str__(self):
        ret = AbstractGroup.__str__(self)
        return ret

    def __repr__(self):
        ret = self.__str__()+"\n"
        ret += f"""{"-" * (len(self.__str__()))}\n"""
        ret += f"""    Data directory : {str(self.datadir):s}\n"""
        ret += f"""    File names     : {str(self._getfilename(0)):s}\n"""
        ret += f"""    Overwrite      : {colorize(
            self.overwrite, "yellow") if not self.overwrite else self.overwrite}\n"""
        ret += f"""    Dumping        : {
            colorize(self.dumping, "yellow") if not self.dumping else self.dumping}\n"""
        ret += f"""    Options        : {self.options}\n"""
        ret += f"""    Verbosity      : {self.verbosity}"""
        return ret

    def _getfilename(self, i):
        """This function creates ``<path>/<filename>`` for a given output number

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
        if ext != "":
            if not ext.startswith("."):
                ext = "." + ext

        number = str(i).zfill(self.zfill)
        filename = self.filename + number + ext

        return self.datadir.joinpath(filename)

    def writedump(self, frame, filename=None):
        """Writes the ``Frame`` to dump file

        Parameters
        ----------
        frame : object
            object to be written to file
        filename : str, optional, default : ""
            path to file to be written
            if not set, filename will be <writer.datadir>/frame.dmp."""

        filename = self.datadir.joinpath(
            "frame.dmp") if filename is None else Path(filename)
        self.checkdatadir(createdir=True)

        if self.verbosity > 0:
            msg = f"Writing dump file {colorize(filename, 'blue')}"
            print(msg)

        writedump(frame, filename)

    def write(self, owner, i, forceoverwrite, filename=None):
        """Writes output to file

        Parameters
        ----------
        owner : Frame
            Parent ``Frame`` object
        i : int
            Number of output
        forceoverwrite : boolean
            If ``True`` it will forces and overwrite of the file if it exists independent of the writer attribute
        filename : string
            If this is not "" the writer will use this filename instead of the standard scheme"""

        if filename == None:
            filename = self._getfilename(i)
        else:
            filename = Path(filename)
        self.checkdatadir(createdir=True)
        if not forceoverwrite:
            if not self.overwrite:
                if filename.exists():
                    raise RuntimeError(
                        f"File {str(filename)} already exists.")
        if self.verbosity > 0:
            msg = f"Writing file {colorize(filename, 'blue')}"
            print(msg)
        self._func(owner, filename, **self.options)
        if self.dumping:
            self.writedump(owner)
