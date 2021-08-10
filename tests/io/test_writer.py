# Tests for the Writer class


import os
import pytest
import shutil
from simframe import Frame
from simframe import writers
from simframe.io import Writer


def test_writer_attributes():
    string = "data"

    def f():
        pass
    writer = Writer(f)
    with pytest.raises(TypeError):
        writer.datadir = 1
    with pytest.raises(TypeError):
        writer.description = 1
    writer.description = string
    assert writer.description == string
    with pytest.raises(TypeError):
        writer.extension = 1
    with pytest.raises(ValueError):
        writer.extension = "." + string
    with pytest.raises(TypeError):
        writer.filename = 1
    with pytest.raises(ValueError):
        writer.filename = ""
    with pytest.raises(TypeError):
        writer.options = 1
    with pytest.raises(TypeError):
        writer.read = 1
    with pytest.raises(TypeError):
        writer.overwrite = string
    writer.overwrite = True
    assert writer.overwrite
    with pytest.raises(TypeError):
        writer.dumping = string
    writer.dumping = False
    assert not writer.dumping
    with pytest.raises(TypeError):
        writer.verbosity = string
    with pytest.raises(TypeError):
        writer.zfill = string
    assert isinstance(repr(writer), str)
    assert isinstance(str(writer), str)


def test_writer_checkdatadir():
    string = "data"

    def f():
        pass
    writer = Writer(f)
    writer.verbosity = 0
    writer.datadir = string
    writer.checkdatadir(createdir=True)
    assert os.path.isdir(writer.datadir)
    shutil.rmtree(writer.datadir)


def test_writer_extension_handling():
    def f():
        pass
    writer = Writer(f)
    writer._extension = ".out"
    assert writer._getfilename(0) == "data/data0000.out"
    writer.extension = ""
    assert writer._getfilename(0) == "data/data0000"


def test_write():
    f = Frame()
    f.writer = writers.hdf5writer
    filename = os.path.join(f.writer.datadir, "test.out")
    f.writer.write(f, 0, True, filename=filename)
    assert os.path.isfile(filename)
    with pytest.raises(RuntimeError):
        f.writer.write(f, 0, False, filename=filename)
    os.remove(filename)
    f.writer.overwrite = True
    f.writer.dumping = False
    f.writer.verbosity = 1
    f.writer.write(f, 0, False, filename=filename)
    assert os.path.isfile(filename)
    shutil.rmtree(f.writer.datadir)
