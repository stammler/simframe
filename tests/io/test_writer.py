# Tests for the Writer class

import pytest
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
    def f():
        pass
    writer = Writer(f)
    writer.verbosity = 0
    writer.checkdatadir(createdir=True)
    assert writer.datadir.is_dir()
    writer.datadir.rmdir()


def test_writer_extension_handling():
    def f():
        pass
    writer = Writer(f)
    writer._extension = ".out"
    assert writer._getfilename(0) == writer.datadir.joinpath("data0000.out")
    writer.extension = ""
    assert writer._getfilename(0) == writer.datadir.joinpath("data0000")


def test_write():
    f = Frame()
    f.writer = writers.hdf5writer
    f.writer.verbosity = 0
    filename = f.writer.datadir.joinpath("test.out")
    f.writer.write(f, 0, True, filename=filename)
    assert filename.is_file()
    with pytest.raises(RuntimeError):
        f.writer.write(f, 0, False, filename=filename)
    filename.unlink()
    f.writer.overwrite = True
    f.writer.dumping = False
    f.writer.verbosity = 1
    f.writer.write(f, 0, False, filename=filename)
    assert filename.is_file()
    files = f.writer.datadir.glob("*")
    for file in files:
        file.unlink()
    f.writer.datadir.rmdir()
