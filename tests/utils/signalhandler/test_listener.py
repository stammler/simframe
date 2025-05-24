import pytest
import signal
from simframe import Frame
from simframe import writers
from simframe.utils.signalhandler import actions
from simframe.utils.signalhandler import Event
from simframe.utils.signalhandler import Listener
from simframe.utils.signalhandler import signals


def test_listener():
    f = Frame(writer=writers.hdf5writer())
    event = Event(signals.STOPFILE, actions.STOP)
    listener = Listener(f, event)
    with pytest.raises(TypeError):
        listener.events = None
    events = [event, Event(signal.SIGUSR2, actions.STOP)]
    listener.events = events
    with pytest.raises(SystemExit):
        signal.raise_signal(signal.SIGUSR2)
    f.writer.datadir.mkdir()
    stopfile = f.writer.datadir / "STOP"
    stopfile.touch()
    with pytest.raises(SystemExit):
        listener.listen()
    f.writer.datadir.rmdir()
