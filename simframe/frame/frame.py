import numpy as np

from simframe.frame.group import Group
from simframe.integration.integrator import Integrator
from simframe.io.writer import Writer

class Frame(Group):
    """Frame class.
    This is the parent object that contains all other objects
    
    Parameters
    ----------
    description : string, optional, default : None
        Descriptive string of the frame object
    writer : Writer, optional, default : None
        Object of type Writer fir writing output files
        
    Examples
    --------
    >>> sim = Frame(description="My Simulation")
    >>> sim
    Frame (My Simulation):"""

    __name__ = "Frame"
    _integrator = None
    _writer = None
    
    def __init__(self, description=None, integrator=None, writer=None):
        super().__init__(self, description=description)
        self.integrator = integrator
        self.writer = writer

    @property
    def integrator(self):
        return self._integrator
    @integrator.setter
    def integrator(self, integrator):
        if integrator is not None and type(integrator) is not Integrator:
            raise TypeError("<simframe.Frame.integrator> hat to be of type <simframe.integration.integrator.Integrator> or None.")
        self._integrator = integrator

    @property
    def writer(self):
        return self._writer
    @writer.setter
    def writer(self, writer):
        if writer is not None and type(writer) is not Writer:
            raise TypeError("<simframe.Frame.writer> hat to be of type <simframe.io.Writer> or None.")
        self._writer = writer

    def writeoutput(self, i=0, filename="", forceoverwrite=False, **kwargs):
        """Writes output to file, if writer is specified.
        
        Parameters
        ----------
        i : int, optional, default : 0
            Number of output
        filename : string, optional, default = ""
            if given this will write the output to this file. Otherwise, it uses the standard scheme.
        forceoverwrite : boolean, optional, default : False
            If True, this overrules the seetings of the Writer and enforces the file to be overwritten."""

        if self.writer is not None:
            self.writer.write(self, i, filename, forceoverwrite, **kwargs)

    def run(self):

        if not isinstance(self.integrator, Integrator):
            raise RuntimeError("No integrator set.")

        # Write initial conditions
        if self.integrator.var <= self.integrator.var.snapshots[0]:
            self.writeoutput(0)

        starting_index = np.argmin(self.integrator.var >= self.integrator.var.snapshots)
        for i in range(starting_index, len(self.integrator.var.snapshots)):

            varnext = self.integrator.var.nextsnapshot
            while self.integrator.var < varnext:
                self.integrator.integrate()
                self.integrator.var += self.integrator.var.stepsize
                self.update()
            
            self.writeoutput(i+1)