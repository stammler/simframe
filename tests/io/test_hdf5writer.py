# Tests for the hdf5writer writer


import numpy as np
import pytest
from simframe import Frame
from simframe import writers


def test_hdf5writer_skip():
    f = Frame()
    f.writer = writers.hdf5writer()
    f.addfield("x", 0., save=False)
    f.writeoutput(0)
    with pytest.raises(KeyError):
        f.writer.read.sequence("x")
    files = f.writer.datadir.glob("*")
    for file in files:
        file.unlink()
    f.writer.datadir.rmdir()


def test_hdf5writer_strings():
    string = "test"
    # When read from HDF5 the string will be a byte literal
    string_cmpr = string.encode()
    f = Frame()
    f.addfield("s", [string, string])
    f.t = string
    f.writer = writers.hdf5writer()
    f.writeoutput(0)
    f.writeoutput(1)
    data0000 = f.writer.read.output(0)
    assert np.all(data0000.s == string_cmpr)
    assert data0000.t == string_cmpr
    s = f.writer.read.sequence("s")
    assert np.all(s == string_cmpr)
    t = f.writer.read.sequence("t")
    assert np.all(t == string_cmpr)
    data = f.writer.read.all()
    assert np.all(data.s == string_cmpr)
    assert np.all(data.t == string_cmpr)
    files = f.writer.datadir.glob("*")
    for file in files:
        file.unlink()
    f.writer.datadir.rmdir()


def test_hdf5writer_none():
    f = Frame()
    f.n = None
    f.writer = writers.hdf5writer()
    with pytest.raises(ValueError):
        f.writeoutput(0)
    f.n = [1, None]
    with pytest.raises(ValueError):
        f.writeoutput(1)
    f.n = (1, None)
    with pytest.raises(ValueError):
        f.writeoutput(2)
    files = f.writer.datadir.glob("*")
    for file in files:
        file.unlink()
    f.writer.datadir.rmdir()


def test_hdf5writer_dict():
    f = Frame()
    f.n = {1: 1}
    f.writer = writers.hdf5writer()
    with pytest.raises(NotImplementedError):
        f.writeoutput(0)
    files = f.writer.datadir.glob("*")
    for file in files:
        file.unlink()
    f.writer.datadir.rmdir()


def test_hdf5writer_number():
    f = Frame()
    f.n = 1
    f.writer = writers.hdf5writer()
    f.writeoutput(0)
    f.writeoutput(1)
    data0000 = f.writer.read.output(0)
    assert data0000.n == 1
    n = f.writer.read.sequence("n")
    assert np.all(n == [1, 1])
    data = f.writer.read.all()
    assert np.all(data.n == [1, 1])
    files = f.writer.datadir.glob("*")
    for file in files:
        file.unlink()
    f.writer.datadir.rmdir()


def test_hdf5writer_single_value_array():
    f = Frame()
    f.n = np.array(1)
    f.writer = writers.hdf5writer()
    f.writeoutput(0)
    f.writeoutput(1)
    data0000 = f.writer.read.output(0)
    assert data0000.n == 1
    n = f.writer.read.sequence("n")
    assert np.all(n == [1, 1])
    data = f.writer.read.all()
    assert np.all(data.n == [1, 1])
    files = f.writer.datadir.glob("*")
    for file in files:
        file.unlink()
    f.writer.datadir.rmdir()


def test_hdf5writer_list():
    f = Frame()
    f.n = [1, 1]
    f.writer = writers.hdf5writer()
    f.writeoutput(0)
    f.writeoutput(1)
    data0000 = f.writer.read.output(0)
    assert np.all(data0000.n == [1, 1])
    n = f.writer.read.sequence("n")
    assert np.all(n == [[1, 1], [1, 1]])
    data = f.writer.read.all()
    assert np.all(data.n == [[1, 1], [1, 1]])
    files = f.writer.datadir.glob("*")
    for file in files:
        file.unlink()
    f.writer.datadir.rmdir()
