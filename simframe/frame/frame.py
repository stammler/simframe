import numpy as np

from simframe.frame.group import Group
from simframe.frame.intvar import IntVar

from simframe.integration.integrator import Integrator
from simframe.io.writer import Writer


class Frame(Group):
    """Frame class.
    This is the parent object of type Group that contains all other objects.

    During integration the update() function of the frame object will be called.
    You have to sub-delegete the updates of your other groups and fields with this function.

    Frame has additional functionality for writing output files and for integration.

    writeoutput(file) : writes output file according writer instructions
    run() : starts the simulation"""

    __name__ = "Frame"

    _integrator = None
    _writer = None

    def __init__(self, integrator=None, writer=None, updater=None, description=""):
        """
        The parent Frame object.

        Parameters
        ----------
        writer : Writer, optional, default : None
            Object of type Writer fir writing output files
        integrator : Integrator, optional, default : None
            Integrator with integration instructions
        updater : Heartbeat, Updater, callable, list or None, optional, default : None
            Updater for updating the frame
        description : string, optional, default : ""
            Descriptive string of the frame object"""
        super().__init__(self, updater=None, description=description)
        self.integrator = integrator
        self.writer = writer

    @property
    def integrator(self):
        return self._integrator

    @integrator.setter
    def integrator(self, integrator):
        if integrator is not None and type(integrator) is not Integrator:
            raise TypeError("integrator has to be of type Integrator or None.")
        self._integrator = integrator

    @property
    def writer(self):
        return self._writer

    @writer.setter
    def writer(self, value):
        if value is not None and not isinstance(value, Writer):
            raise TypeError("writer hat to be of type Writer or None.")
        self._writer = value

    def writeoutput(self, i=0, forceoverwrite=False, filename="", **kwargs):
        """Writes output to file, if writer is specified.

        Parameters
        ----------
        i : int, optional, default : 0
            Number of output
        filename : string, optional, default = ""
            if given this will write the output to this file. Otherwise, it uses the standard scheme.
        forceoverwrite : boolean, optional, default : False
            If True, this overrules the seetings of the Writer and enforces the file to be overwritten.
        kwargs : additional keyword arguments
            Additional options that can be passed to the writer"""

        if self.writer is not None:
            self.writer.write(self, i, forceoverwrite, filename, **kwargs)

    def run(self):
        """This method starts the simulation run. An integrator has to be set beforehand."""

        if not isinstance(self.integrator, Integrator):
            raise RuntimeError("No integrator set.")

        # Check if integration variable is set
        if not isinstance(self.integrator.var, IntVar):
            raise RuntimeError(
                "No integration variable assigned to integrator.")

        # If there are no snapshots set
        if not len(self.integrator.var.snapshots):
            raise RuntimeError(
                "No snapshots set. At least one snapshot has to be given.")

        # If integration variable passed maximum value of snapshots
        if self.integrator.var >= self.integrator.var.snapshots[-1]:
            raise RuntimeError(
                "Integration variable already passed the largest snapshot.")

        # Write initial conditions
        if self.integrator.var < self.integrator.var.snapshots[0]:
            self.writeoutput(0)

        starting_index = np.argmin(
            self.integrator.var >= self.integrator.var.snapshots)
        for i in range(starting_index, len(self.integrator.var.snapshots)):

            # Nextsnapshot cannot be referenced directly, because it dynamically changes.
            nextsnapshot = self.integrator.var.nextsnapshot
            while self.integrator.var < nextsnapshot:
                self.integrator.integrate()
                self.integrator.var += self.integrator.var.stepsize
                self.update()

            self.writeoutput(i + 1)
