from collections.abc import Iterable
from functools import partial
import signal
from simframe.utils.signalhandler.event import Event

class Listener(object):
    """
    Listener class to handle multiple events.
    """

    def __init__(self, owner, events):
        """
        Listerner for signal handling.

        Parameters
        ----------
        owner : Frame
            Parent simulation frame.
        events : list of simframe.utils.signalhandler.Event
            Events to listen for.
        """
        super().__init__()
        self._owner = owner
        self.events = events
        self._handlers = []
        
    @property
    def events(self):
        """List of events to listen for."""
        return self._events
    
    @events.setter
    def events(self, val):
        events = []
        handlers = [] # Handlers for system signals
        if not isinstance(val, Iterable):
            val = [val]
        for event in val:
            if not isinstance(event, Event):
                raise RuntimeError("Invalid event.")
            # If signal is system signal, prepare asyncronous handler and
            # remove from events.
            if isinstance(event.signal, signal.Signals):
                handlers.append(self._sethandler(event.signal, event.actions))
            else:
                events.append(event)
        self._events = events
        self._handler = handlers

    def listen(self):
        """
        Listen for all events and perform actions if signal triggered.
        """
        for event in self.events:
            event(self._owner)

    @staticmethod
    def _handler(signum, sigframe, frame, *args, actions=[], **kwargs):
        """
        Static template method for system signal handling.
        
        Parameters
        ----------
        signum : Int
            Signal number
        sigframe : None or frame object
            Current stack frame
        frame : Frame
            Simulation frame
        args : Additional positional arguments
        actions : list of simframe.utils.signalhandler.Action
            Actions to be performed
        kwargs : Additional keyword arguments
        """
        signame = signal.Signals(signum).name
        print(f"Signal detected: {signame} ({signum})")
        for action in actions:
            action(frame)

    def _sethandler(self, sig, actions):
        """
        Function returns a valid handler for system signal handling.
        The additional parameters are reduced with functools.partial.
        """
        handler = partial(Listener._handler, frame=self._owner, actions=actions)
        return signal.signal(sig, handler)