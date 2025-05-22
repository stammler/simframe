class Signal(object):
    """Template class of an signal for which Simframe is scanning."""

    def __init__(self):
        """
        Callable signal class that is holding scanning instructions.
        """
        super().__init__()

    def _listen(self, *args, **kwargs):
        """
        Function that is performed to scan for signal.
        Has to be implemented by child class.

        Parameters
        ----------
        args : additional positional arguments
        kwargs : additional keyword arguments

        Returns
        -------
        signal_flag : bool
            True : signal detected
            False : signal not detected
        """
        return False

    def __call__(self, *args, **kwargs):
        """
        Scanning for signal.

        Parameters
        ----------
        args : additional positional arguments
        kwargs : additional keyword arguments

        Returns
        -------
        signal_flag : bool
            True : signal detected
            False : signal not detected
        """
        return self._listen(*args, **kwargs)
    
    def _cleanup(self, *args, **kwargs):
        """
        Instruction that is performed to clean up after signal is detected.
        Has to be implemented by child class.

        Parameters
        ----------
        args : additional positional arguments
        kwargs : additional keyword arguments
        """
        pass
