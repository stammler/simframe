# This unit test writes and reads a dump file


import os
import shutil
from simframe import Frame
from simframe import writers
from simframe.io import readdump


def test_write_read_dump():
    f = Frame()
    f.addfield("x", 0.)
    f.addgroup("A")
    f.A.addfield("x", 1.)
    f.writer = writers.hdf5writer
    dumpfile = os.path.join(f.writer.datadir, "test.dmp")
    f.writer.writedump(f, filename=dumpfile)
    f.writer.verbosity = 0
    f.writer.writedump(f, filename=dumpfile)
    d = readdump(dumpfile)
    assert d.x == 0.
    assert d.A.x == 1.
    shutil.rmtree(f.writer.datadir)
