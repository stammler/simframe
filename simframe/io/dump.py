import dill
from functools import partial
import signal


def writedump(object, filename="frame.dmp"):
    """Writes object to dump file

    Parameters
    ----------
    object : object
        object to be written to file
    filename : str, optional, default : "frame.dmp"
        path to file to be written"""
    with open(filename, "wb") as dumpfile:
        dill.dump(object, dumpfile)


def readdump(filename):
    """Reads dumpfile and returns ``Frame`` object

    Parameters
    ----------
    filename : str
        Path to file to be read

    Returns
    -------
    obj : object
        object read from dump file

    Notes
    -----
    Only read dump files from sources you trust.
    Malware can be injected."""
    with open(filename, "rb") as dumpfile:
        obj = dill.load(dumpfile)
    # Repair listener when using system signals
    obj = _repairlistener(obj)
    return obj


def _repairlistener(frame):
    """
    Function to repair the listener when loaded from a dump file and
    containing system signal events. The handler for system signals
    is a wrapper with functools.partial which has the simulation frame
    as keyword argument. This is somehow not identical to the parent
    simulation frame when loaded from a dump file and has to be fixed.
    """
    # Check if frame has a listerner. If not, do nothing.
    if frame.listener is not None:
        # Go through all registered events
        for event in frame.listener.events:
            # Check if signal is a system signal and not a file signal
            if isinstance(event.signal, signal.Signals):
                handler = signal.getsignal(event.signal)
                # Check if the handler is functools.partial and not a default signal
                if isinstance(handler, partial):
                    # Safety check to make sure the handler was created from Simframe
                    if handler.keywords.get("from_simframe") == True:
                        # Replace with actual frame
                        signal.getsignal(event.signal).keywords["frame"] = frame
    return frame