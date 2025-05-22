from simframe.utils.signalhandler.action import Action

class StopAction(Action):
    """
    Action stops the simulation.
    """

    def __init__(self):
        """
        Action to stop the simulation.
        """
        super().__init__()


    def _do(self, frame):
        """
        Stop the simulation by raising ``SystemExit``.

        Parameters
        ----------
        frame : Frame
            Simulation frame
        """
        raise SystemExit("Simframe detected STOP signal. Simulation aborted.")