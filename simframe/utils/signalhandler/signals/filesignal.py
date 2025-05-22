from pathlib import Path
from simframe.utils.signalhandler.signal import Signal

class FileSignal(Signal):
    """
    Signal class that is scaning for a file.
    Only works if a writer is assigned to the simulation frame
    and a data directory is set.
    """

    def __init__(self, file):
        """
        Signal that is scanning for a file.
        Only works if a writer is assigned to the simulation frame
        and a data directory is set.
        """
        super().__init__()
        self.file = file


    @property
    def file(self):
        """File to scan for."""
        return self._file
    
    @file.setter
    def file(self, val):
        self._file = Path(val)

    def _listen(self, frame):
        """
        Function checks if a file is present.

        Parameters
        ----------
        frame : Frame
            Simulation frame

        Returns
        -------
        signal_flag : bool
            True : file is present
            False : file is not present
        """
        if frame.writer is not None:
            # Contruct filename from writer
            file = frame.writer.datadir / self.file
            if file.is_file():
                return True
        return False
    
    def _cleanup(self, frame):
        """
        Function deletes the file which was scanned for.

        Parameters
        ----------
        frame : Frame
            Simulation frame
        """
        if frame.writer is not None:
            file = frame.writer.datadir / self.file
            file.unlink()
