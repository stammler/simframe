import os
import pytest
import signal
from simframe import Frame
from simframe import writers
from simframe.utils.signalhandler import actions
from simframe.utils.signalhandler import Event
from simframe.utils.signalhandler import signals


def test_event_class():
    f = Frame(writer=writers.hdf5writer())
    event = Event(signal=signal.Signals.SIGTERM, actions=actions.STOP)
    assert not event(f)
    with pytest.raises(TypeError):
        event.signal = None
    with pytest.raises(TypeError):
        event.actions = None
    event.signal = signals.STOPFILE
    f.writer.datadir.mkdir()
    stopfile = f.writer.datadir / "STOP"
    stopfile.touch()
    with pytest.raises(SystemExit):
        event(f)
    assert not stopfile.is_file()
    f.writer.datadir.rmdir()


def test_slurm_requeue_event():
    f = Frame(writer=writers.hdf5writer())
    os.environ["SLURM_JOB_ID"] = "1"
    with pytest.raises(FileNotFoundError):
        signal.raise_signal(signal.SIGTERM)
    datafile = f.writer.datadir / "__OUTPUT__"
    dumpfile = f.writer.datadir / "frame.dmp"
    datafile.unlink()
    dumpfile.unlink()
    f.writer.datadir.rmdir()
