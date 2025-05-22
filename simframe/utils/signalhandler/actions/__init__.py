"""
Pre-defined actions that can be performed if a signal is triggered.
"""

from simframe.utils.signalhandler.actions.dumpaction import DumpAction as _DA
from simframe.utils.signalhandler.actions.stopaction import StopAction as _SA
from simframe.utils.signalhandler.actions.writeaction import WriteAction as _WA

DUMP = _DA()
STOP = _SA()
WRITE = _WA()

__all__ = [
    "DUMP",
    "STOP",
    "WRITE",
]
