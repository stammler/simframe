from datetime import timedelta
import numpy as np
from time import monotonic

from simframe.frame.group import Group
from simframe.frame.intvar import IntVar

from simframe.integration.integrator import Integrator
from simframe.io.writer import Writer
from simframe.io.progress import Progressbar
from simframe.utils.color import colorize


class Frame(Group):
    """This is the parent object of type ``Group`` that contains all other objects.

    During integration the ``update()`` function of the ``Frame`` object will be called.
    You have to sub-delegete the updates of your other ``Group`` and ``Field`` objects within this function.

    ``Frame`` has additional functionality for writing output files and for integration."""

    __name__ = "Frame"

    _integrator = None
    _verbosity = None
    _progressbar = None
    _writer = None

    def __init__(self, integrator=None, writer=None, updater=None, verbosity=2, progressbar=None, description=""):
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
        verbosity : int, optional, default : 2
            Level of verbosity
        progressbar : Progresbar or None, optional, default : None
            Progressbar. If None, standard is used
        description : string, optional, default : ""
            Descriptive string of the frame object"""
        super().__init__(self, updater=updater, description=description)
        self.integrator = integrator
        self.progressbar = progressbar
        self.verbosity = verbosity
        self.writer = writer

    @property
    def integrator(self):
        '''``Integrator`` that controls the simulation.'''
        return self._integrator

    @integrator.setter
    def integrator(self, integrator):
        if integrator is not None and type(integrator) is not Integrator:
            raise TypeError("integrator has to be of type Integrator or None.")
        self._integrator = integrator

    @property
    def progressbar(self):
        '''``Progressbar`` for displaying current status.'''
        return self._progressbar

    @progressbar.setter
    def progressbar(self, value):
        if value is None:
            self._progressbar = Progressbar()
        else:
            if not isinstance(value, Progressbar):
                raise TypeError("<progressbar> has to be of type Progressbar.")
            self._progressbar = value

    @property
    def verbosity(self):
        '''Verbosity of the ``Frame`` objects.'''
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value):
        if not isinstance(value, np.int):
            raise TypeError("<verbosity> has to be of type int.")
        self._verbosity = value

    @property
    def writer(self):
        '''``Writer`` object for writing output files.'''
        return self._writer

    @writer.setter
    def writer(self, value):
        if value is not None and not isinstance(value, Writer):
            raise TypeError("writer hat to be of type Writer or None.")
        self._writer = value

    def writeoutput(self, i=0, forceoverwrite=False, filename="", **kwargs):
        """Writes output to file, if ``Writer`` is specified.

        Parameters
        ----------
        i : int, optional, default : 0
            Number of output
        forceoverwrite : boolean, optional, default : False
            If True, this overrules the seetings of the Writer and enforces the file to be overwritten.
        filename : string, optional, default = ""
            if given this will write the output to this file. Otherwise, it uses the standard scheme.
        kwargs : additional keyword arguments
            Additional options that can be passed to the writer"""

        if self.writer is not None:
            self.writer.write(self, i, forceoverwrite, filename, **kwargs)

    def run(self):
        """This method starts the simulation. An ``Integrator`` has to be set beforehand."""

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

        # Timekeeping
        tini = monotonic()

        # Write initial conditions
        if self.integrator.var < self.integrator.var.snapshots[0]:
            self.writeoutput(0)

        # Staring index of snapshots
        starting_index = np.argmin(
            self.integrator.var >= self.integrator.var.snapshots)
        # Starting value of integration variable
        startingvalue = self.integrator.var.copy()
        for i in range(starting_index, len(self.integrator.var.snapshots)):

            # Nextsnapshot cannot be referenced directly, because it dynamically changes.
            nextsnapshot = self.integrator.var.nextsnapshot
            prevsnapshot = self.integrator.var.prevsnapshot if self.integrator.var.prevsnapshot is not None else startingvalue

            while self.integrator.var < nextsnapshot:

                if self.verbosity > 1:
                    self.progressbar(self.integrator.var,
                                     prevsnapshot,
                                     nextsnapshot,
                                     startingvalue,
                                     self.integrator.var.snapshots[-1])

                self.integrator.integrate()
                self.integrator.var += self.integrator.var.stepsize
                self.update()

            if self.verbosity > 1:
                self.progressbar._reset()

            self.writeoutput(i + 1)

        # Timekeeping
        tfin = monotonic()
        t_exec = timedelta(seconds=np.int(tfin-tini))
        if self.verbosity > 0:
            msg = "Execution time: {}".format(colorize(t_exec, color="blue"))
            print(msg)
