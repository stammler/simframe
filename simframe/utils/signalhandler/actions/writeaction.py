from simframe.utils.signalhandler.action import Action
from pathlib import Path

class WriteAction(Action):
    """
    Action to write an output file named ``__OUTPUT__``.
    """

    def __init__(self):
        """
        Action to write an output file.
        Only works if the simulation frame has a writer
        with dumping instructions assigned.
        """
        super().__init__()

    def _do(self, frame):
        """
        Write the output file.

        Parameters
        ----------
        frame : Frame
            Simulation frame
        """
        if frame.writer is not None:
            filename = frame.writer.datadir / Path("__OUTPUT__")
            frame.writer.write(frame, 0, True, filename)