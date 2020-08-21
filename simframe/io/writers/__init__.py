"""This package contains pre-defined ``Writer`` instances that can be used for writing and reading ``Frame`` objects.
The ``hdf5writer`` writes data files in the HDF5 file format. The ``namespacewriter`` does not write output files
(except for dump files if required). The data is stored locally in the ``Writer`` object itself."""

from simframe.io.writers.hdf5writer import hdf5writer
from simframe.io.writers.namespacewriter import namespacewriter

__all__ = ["hdf5writer",
           "namespacewriter"]
