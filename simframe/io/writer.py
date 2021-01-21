import dill
import numpy as np
import random
import string
import os

from simframe.frame.field import Field
from simframe.frame.intvar import IntVar
from simframe.io.reader import Reader
from simframe.io.dump import writedump
from simframe.frame.abstractgroup import AbstractGroup
from simframe.utils.color import colorize


class Writer(object):
    """General class for writing output files. It should be used as wrapper for customized ``Writer``."""

    __name__ = "Writer"

    _datadir = "data"
    _description = ""
    _dumping = True
    _extension = "out"
    _filename = "data"
    _options = {}
    _read = None
    _overwrite = False
    _verbosity = 1
    _zfill = 4

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
        if not isinstance(value, str):
            raise TypeError("datadir has to be of type str.")
        self._datadir = value

    @property
    def description(self):
        '''Description of ``Writer``.'''
        return self._description

    @description.setter
    def description(self, value):
        if value is None:
            self._description = ""
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
        if not isinstance(value, np.int):
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
        if not isinstance(value, np.int):
            raise TypeError("<dumping> has to be of type bool.")
        if value:
            self._dumping = True
            self._preparedump()
        else:
            self._dumping = False

    @property
    def verbosity(self):
        '''Verbosity of the writer.'''
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value):
        if not isinstance(value, np.int):
            raise TypeError("<verbosity> has to be of type int.")
        self._verbosity = value

    @property
    def zfill(self):
        '''Zero padding of numbered files names.'''
        return self._zfill

    @zfill.setter
    def zfill(self, value):
        value = np.int(value)
        if not isinstance(value, np.int):
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

        if not os.path.exists(self.datadir) and createdir:
            if self.verbosity > 0:
                msg = "Creating data directory '{:s}'.".format(self.datadir)
                print(msg)
            os.makedirs(self.datadir)

        return os.path.exists(self.datadir)

    def __str__(self):
        ret = AbstractGroup.__str__(self)
        return ret

    def __repr__(self):
        ret = self.__str__()+"\n"
        ret += "-" * (len(ret)-1) + "\n"
        ret += "    Data directory : {}\n".format(self.datadir)
        ret += "    File names     : {}\n".format(self._getfilename(0))
        ret += "    Overwrite      : {}\n".format(
            colorize(self.overwrite, "yellow") if self.overwrite else self.overwrite)
        ret += "    Dumping        : {}\n".format(
            colorize(self.dumping, "yellow") if not self.dumping else self.dumping)
        ret += "    Options        : {}\n".format(self.options)
        ret += "    Verbosity      : {}".format(self.verbosity)
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
            if ext[0] != ".":
                ext = "." + ext

        number = str(i).zfill(self.zfill)
        filename = self.filename + number + ext

        return os.path.join(self.datadir, filename)

    def writedump(self, frame, filename=""):
        """Writes the ``Frame`` to dump file

        Parameters
        ----------
        frame : object
            object to be written to file
        filename : str, optional, default : ""
            path to file to be written
            if not set, filename will be <writer.datadir>/frame.dmp."""

        filename = os.path.join(
            self.datadir, "frame.dmp") if filename == "" else filename
        self.checkdatadir(createdir=True)

        if self.verbosity > 0:
            msg = "Writing dump file {}".format(colorize(filename, "blue"))
            print(msg)

        writedump(frame, filename)

    def _preparedump(self):
        """This function dumps a template ``<simframe.frame.Field>`` and ``<simframe.frame.IntVar>`` to file
        and deletes the file directly afterwards. For some reason ``dill`` does not correctly save ``Field`` and ``IntVar``
        correctly the first time. This function is called everytime ``<Writer.dumping>`` is set to ``True``
        to make sure dumping works correctly when needed.

        This is a "dirty fix". The reason why ``dill`` does not work correctly the first time is unknown.
        """
        while(True):
            filename = "temp_" + "".join(random.choice(string.ascii_uppercase)
                                         for i in range(5)) + ".dmp"
            if not os.path.isfile(filename):
                break
        temp = IntVar(None, 0., snapshots=[0.])
        writedump(temp, filename)
        temp = Field(None, 0.)
        writedump(temp, filename)
        os.remove(filename)

    def write(self, owner, i, forceoverwrite, filename=""):
        """Writes output to file

        Parameters
        ----------
        owner : Frame
            Parent ``Frame`` object
        i : int
            Number of output
        forceoverwrite : boolean
            If ``True`` it will forces and overwrite of the file if it exists.
        filename : string
            If this is not "" the writer will use this filename instead of the standard scheme"""

        if filename == "":
            filename = self._getfilename(i)
            self.checkdatadir(createdir=True)
        if not forceoverwrite:
            if not self.overwrite:
                if os.path.isfile(filename):
                    raise RuntimeError(
                        "File {} already exists.".format(filename))
        self._func(owner, filename, **self.options)
        if self.verbosity > 0:
            msg = "Writing file {}".format(colorize(filename, "blue"))
            print(msg)
        if self.dumping:
            self.writedump(owner)
