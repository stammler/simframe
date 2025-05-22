from collections.abc import Iterable
from signal import Signals
from simframe.utils.signalhandler.action import Action
from simframe.utils.signalhandler.signal import Signal

class Event(object):
    """
    Callable event class that holds signal-actions combinations.
    If an assigned signal is detected, the assigned actions are performed.
    """

    def __init__(self, signal, actions):
        """
        Callable event class for signal handling.

        Parameters
        ----------
        signal : simframe.utils.signalhandler.Signal or signal.Signals
            Trigger signal
        actions : list of simframe.utils.signalhandler.Action
            Actions to be performed at signal
        """
        super().__init__()
        self.actions = actions
        self.signal = signal

    @property
    def actions(self):
        """Action to be performed after triggered signal."""
        return self._actions
    
    @actions.setter
    def actions(self, val):
        # Make list if not iterable
        if not isinstance(val, Iterable):
            val = [val]
        # Check fo valid actions.
        for action in val:
            if not isinstance(action, Action):
                raise RuntimeError("Invalid Action.")
        self._actions = val
        
    @property
    def signal(self):
        """Signal to scan for."""
        return self._signal
    
    @signal.setter
    def signal(self, val):
        # Check for valid signal
        if not isinstance(val, (Signal, Signals)):
            raise RuntimeError("Invalid Signal.")
        self._signal = val
        
    def __call__(self, frame):
        """
        Scanning for signal and performing actions if triggered.
        
        Parameters
        ----------
        frame : Frame
            Simulation frame
        """
        # Ignore system signal, which are treated separately.
        if isinstance(self.signal, Signals):
            return False
        # Check for signal
        if self.signal(frame):
            # Clean up signal
            self.signal._cleanup(frame)
            for action in self.actions:
                action(frame)
