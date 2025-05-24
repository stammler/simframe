import pytest
from simframe import Frame
from simframe import writers
from simframe.utils.signalhandler import Action
from simframe.utils.signalhandler import actions


def test_template_action_class():
    f = Frame()
    act = Action()
    with pytest.raises(NotImplementedError):
        act(f)


def test_dump_action():
    f = Frame(writer=writers.hdf5writer())
    actions.DUMP(f)
    assert f.writer.datadir.is_dir()
    dumpfile = f.writer.datadir / "frame.dmp"
    assert dumpfile.is_file()
    dumpfile.unlink()
    f.writer.datadir.rmdir()


def test_stop_action():
    f = Frame(writer=writers.hdf5writer())
    with pytest.raises(SystemExit):
        actions.STOP(f)


def test_write_action():
    f = Frame(writer=writers.hdf5writer())
    actions.WRITE(f)
    datafile = f.writer.datadir / "__OUTPUT__"
    dumpfile = f.writer.datadir / "frame.dmp"
    assert datafile.is_file()
    assert dumpfile.is_file()
    datafile.unlink()
    dumpfile.unlink()
    f.writer.datadir.rmdir()
