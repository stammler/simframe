from collections import deque
import glob
import numpy as np
from types import SimpleNamespace
import os

from simframe.frame.abstractgroup import AbstractGroup


class Reader(object):
    """General class for reading output files.
    Every ``Writer`` class should also provide a reader for its data files.

    Custom ``Reader`` must provide a method ``Reader.output()`` that reads a single output file
    and returns the data set as type ``SimpleNamespace``.

    The general ``Reader`` class provides a function that stitches together all ``SimpleNamespaces``
    the ``Reader.output()`` method provides into a single ``SimpleNamespace`` by adding another dimension
    along the integration variable ``IntVar``."""

    __name__ = "Reader"

    _description = ""
    _writer = None

    def __init__(self, writer, description=""):
        """General ``Reader`` class

        Parameters
        ----------
        writer : Writer
            The writer object to which the reader belongs
        description : str, optional, default = ""
            Descriptive string of reader."""
        self.description = description
        self._writer = writer

    @property
    def description(self):
        '''Description of the ``Reader``.'''
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, (str, type(None))):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    def __str__(self):
        return AbstractGroup.__str__(self)

    def __repr__(self):
        return self.__str__()

    def output(self, file):
        """Function that returns the data of a single output file.

        Parameters
        ----------
        file : str
            Path to file that should be read.

        Returns
        -------
        data : SimpleNamespace
            Data set of a single output file."""
        raise NotImplementedError("<read.output> is not implemented.")

    def sequence(self, field):
        """Function that returns the entire sequence of a specific field.

        Parameters
        ----------
        field : str
            String with location of requested field

        Returns
        -------
        seq : array
            Array with requested values

        Notes
        -----
        ``field`` is addressing the values just as in the parent frame object.
        E.g. ``"groupA.groupB.fieldC"`` is addressing ``Frame.groupA.groupB.fieldC``."""
        raise NotImplementedError("<read.sequence> is not implemented.")

    def listfiles(self):
        """Method to list all data files in a directory

        Returns
        -------
        files : list
            List of strings of all found data files sorted alphanumerically.

        Notes
        -----
        Function only searches for files that match the pattern specified by the ``Writer``'s
        ``filename`` and ``extension`` attributes."""
        datadir = self._writer.datadir
        ext = self._writer.extension if self._writer.extension != "" else "." + \
            self._writer.extension
        wildcard = os.path.join(datadir, self._writer.filename + "*" + ext)
        files = glob.glob(wildcard)
        files = sorted(files, key=str.casefold)
        return files

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
        files = self.listfiles()
        if files == []:
            raise RuntimeError("Data directory does not exist or is empty.")
        # Read first file to get structure
        data0 = self.output(files[0])
        # print(data0.__dict__.keys())
        return self._expand(data0)

    def _expand(self, ns, prefix=""):
        """This is a function that get recursively called to fill a data structure with sequences.

        Parameters
        ----------
        ns : SimpleNamespace
            Name space to read sequences from
        prefix : string, optional default: ""
            prefix of data to get into depth of the structure"""
        ret = {}
        for key, val in ns.__dict__.items():
            new_prefix = ".".join(filter(None, [prefix, key]))
            if isinstance(val, SimpleNamespace):
                ret[key] = self._expand(val, prefix=new_prefix)
            else:
                ret[key] = self.sequence(new_prefix)
        return SimpleNamespace(**ret)
