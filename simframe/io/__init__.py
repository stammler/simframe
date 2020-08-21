"""This package is for input/output operations. It contains template ``Writer`` and ``Reader`` classes that can be used
to create customized writing and reading methods. The package ``writers`` contains pre-defined ``Writer`` instances for
writing and reading ``simframe`` data. The package furthermore contains a method for reading dump files and for printing
a progress bar in an interactive shell."""

from simframe.io.reader import Reader
from simframe.io.writer import Writer
from simframe.io import writers
from simframe.io.dump import readdump
from simframe.io.progress import Progressbar

__all__ = ["Reader",
           "Writer",
           "writers",
           "readdump",
           "Progressbar"]
