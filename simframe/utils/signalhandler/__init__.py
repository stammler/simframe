"""
Package contains infrastructure to interact with a Simframe simulation from outside its own process.

It can be used to trigger the immeadiate write out data and/or dump files to the disk or to stop
a simulation. By default Simframe check if the files "DUMP", "WRITE", or "STOP" are present in
the data directory of the writer, if any is set. When the "DUMP" files is detected, Simframe
will write a dump file immeadiately at the beginning of the next timestep. When the "WRITE" file is
detected, Simframe will write a regular output file with the name "__OUTPUT__" and a dumpfile.
Existing files will be overwritten. Both actions will only be executed if the Frame has a writer
with write and dump instructions assigned. If the writer is automatically writes dump files during
normal outputs, this will write the dump file twice. If the "STOP" file is detected, Simframe
will perform both operations and then abort the simulation. In all cases the "DUMP", "WRITE", or
"STOP" files will be deleted afterwards.

By default, if the system signal SIGUSR2 (12) is detected, Simframe will behave as if the "STOP"
file was present. This can be used to safe data shortly before the timeout limit of a SLURM job.
"""

from simframe.utils.signalhandler import actions
from simframe.utils.signalhandler.action import Action
from simframe.utils.signalhandler.event import Event
from simframe.utils.signalhandler.listener import Listener
from simframe.utils.signalhandler.signal import Signal
from simframe.utils.signalhandler import signals


__all__ = [
    "actions",
    "Action",
    "Event",
    "Listener",
    "Signal",
    "signals",
]