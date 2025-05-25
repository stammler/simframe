"""
Pre-defined events to be used in a Listener.

``DUMPFILEEVENT`` writes a dump file, if the file ``DUMP`` is detected.
``STOPFILEEVENT`` writes an output file, a dump file and stops the simulation,
if the file "STOP" is detected.
``WRITEFILEEVENT`` writes an output file, if the file ``WRITE`` is detected.
``STOPSIGNALEVENT`` writes an output file, a dump file, requeues the SLURM job,
if a job id is found, and stops the simulation, if the termination system
signal ``SIGTERM (15)`` is detected.
"""

from signal import SIGTERM
from simframe.utils.signalhandler.event import Event
from simframe.utils.signalhandler.actions import DUMP
from simframe.utils.signalhandler.actions import SLURMREQUEUE
from simframe.utils.signalhandler.actions import STOP
from simframe.utils.signalhandler.actions import WRITE
from simframe.utils.signalhandler.signals import DUMPFILE
from simframe.utils.signalhandler.signals import STOPFILE
from simframe.utils.signalhandler.signals import WRITEFILE

DUMPFILEEVENT = Event(DUMPFILE, [DUMP])
STOPFILEEVENT = Event(STOPFILE, [WRITE, DUMP, STOP])
WRITEFILEEVENT = Event(WRITEFILE, [WRITE, DUMP])
STOPSIGNALEVENT = Event(SIGTERM, [WRITE, DUMP, SLURMREQUEUE, STOP])

__all__ = [
    "DUMPFILEEVENT",
    "STOPFILEEVENT",
    "WRITEFILEEVENT",
    "STOPSIGNALEVENT",
]
