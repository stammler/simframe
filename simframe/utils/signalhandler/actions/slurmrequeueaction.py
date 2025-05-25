import os
from simframe.utils.signalhandler.action import Action
import subprocess


class SlurmRequeueAction(Action):
    """
    Action to requeue a SLURM job.
    """

    def __init__(self):
        """
        Action to requeue a currently running SLURM job.
        """
        super().__init__()

    def _do(self, frame):
        """
        Requeue the job.
        Does not requeue if `$SLURM_JOB_ID` environment variable is
        not present.

        Parameters
        ----------
        frame : Frame
            Simulation frame
        """
        if "SLURM_JOB_ID" in os.environ:
            job_id = os.environ["SLURM_JOB_ID"]
            subprocess.run(
                args=f"scontrol requeue incomplete {job_id}".split()
            )
