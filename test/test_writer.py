import h5py
import numpy as np
import os
import shutil
from simframe.frame import Frame
from simframe.io import hdf5writer
from simframe.io import Writer

import pytest

N = 100
myfieldname = "myfield"
sim = Frame()
sim.addfield(myfieldname, np.arange(N))
sim.addfield("_" + myfieldname, np.arange(N))
sim.writer = hdf5writer

# Make sure there is no data directory
datadir = "data"
if os.path.isdir(datadir):
    shutil.rmtree(datadir)

# Check of writer class

# Check if write function is executed
def writer_function(sim, s):
    sim.string = "Test"
writer = Writer(writer_function)
sim.string = None
writer.write(sim, 0, "test", False)
assert sim.string == "Test"
del(sim.string)

# Checks of hdf5 writer

# Check if file was written
sim.writeoutput(0)
filename = "data0000.hdf5"
pathtofile = os.path.join(datadir, filename)
assert os.path.isfile(pathtofile) == True

# Check if data was written to file
with h5py.File(pathtofile, "r") as File:
    assert np.all(File[myfieldname][()] == np.arange(N))

# Check if data with underscore was not written to file
with h5py.File(pathtofile, "r") as File:
    with pytest.raises(KeyError):
        File["_" + myfieldname][()]

# Check if it prevents overwrites
with pytest.raises(RuntimeError):
    sim.writeoutput(0)

# Check if forceful overwrites work
sim.myfield += 1
sim.writer.overwrite = True
sim.writeoutput(0)
with h5py.File(pathtofile, "r") as File:
    assert np.all(File[myfieldname][()] == np.arange(N)+1)

# Clean up directory
datadir = "data"
if os.path.isdir(datadir):
    shutil.rmtree(datadir)