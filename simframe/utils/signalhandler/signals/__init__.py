"""
Pre-defined signals that can be used for scanning.
"""

from simframe.utils.signalhandler.signals.filesignal import FileSignal as _FS

# File signals scanning for "DUMP", "STOP", and "WRITE" files.
DUMPFILE = _FS("DUMP")
STOPFILE = _FS("STOP")
WRITEFILE = _FS("WRITE")

__all__ = [
    "DUMPFILE",
    "STOPFILE",
    "WRITEFILE",
]
