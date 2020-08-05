import glob
import numpy as np
from types import SimpleNamespace
import os

from simframe.frame.abstractgroup import AbstractGroup

class Reader(object):
    """General class for reading outputs that can be used as template.
    Every writer class should also provide a reader for its data files.
    
    Custom readers must provide a method <output> that reads a single output file
    and returns the data set as type SimpleNamespace.
    
    The general reader class provides a function that can stitch together all SimpleNamespaces
    the <output> method provides into a single SimpleNamespace by adding another dimension
    along the integration variable."""

    __name__ = "Reader"

    _description = ""
    _writer = None

    def __init__(self, writer, description=""):
        """General reader class
        
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
        data : SimpleNamespace
            Data set of a single output file."""
        pass

    def listfiles(self, datadir=None):
        """Method to list all data files in a directory
        
        Parameters
        ----------
        datadir : str, optional, default : None
            Path to dara directory. If None it looks automatically in the data directory specified by the writer.
            
        Returns
        -------
        files : list
            List of strings of all found data files sorted alphanumerically.
            
        Notes
        -----
        Function only searches for files that match the pattern specified by the writers
        filename and extension attributes."""
        datadir = datadir or self._writer.datadir
        ext = self._writer.extension if self._writer.extension != "" else "." + self._writer.extension
        wildcard = os.path.join(datadir, self._writer.filename + "*" + ext)
        files = glob.glob(wildcard)
        files = sorted(files, key=str.casefold)
        return files

    def all(self, datadir=None):
        """Functions that reads all output files and combines them into a single namespace.
        
        Parameters
        ----------
        datadir : str, optional, default : None
            Path to data directory. File need to be found by Reader.listfiles()
            
        Returns
        -------
        dataset : SimpleNamespace
            Namespace of data set."""
        files = self.listfiles(datadir)
        dicts = []
        for file in files:
            dicts.append(self.output(file).__dict__)
        return  self._zip(dicts)

    def _zip(self, dicts):
        """Helper function that stitches toghether SimpleNamespaces. The depth of the data sets if caught by iteratively
        calling the function.
        
        Parameters
        ----------
        dicts : list
            List of dictionaries containing the data
        
        Returns
        -------
        dataset : SimpleNamespace
            Namespace of the datasets."""
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