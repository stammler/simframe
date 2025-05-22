from simframe.utils.signalhandler.action import Action

class DumpAction(Action):
    """
    Action writes a dump file of the simulation frame.
    """

    def __init__(self):
        """
        Action to write a dump of the simulation frame.
        Only works if the simulation frame has a writer
        with dumping instructions assigned.
        """
        super().__init__()


    def _do(self, frame):
        """
        Write a dump file. Only works if simulation frame
        has writer with dumping instructions assigned.
        """
        if frame.writer is not None:
            frame.writer.writedump(frame)