from simframe.frame.abstractgroup import AbstractGroup

class AbstractScheme:
    """Class for an abstract integration scheme that can be used as template for creating custom schemes.
    
    Notes
    -----
    The integration scheme needs to return False if the integration failed. The integrator will then
    perform a fail operation and will try it again. This can be used to implement schemes with adaptive
    step sizes. If the step size was not small enough the fail operation can reduce it further."""

    __name__ = "Scheme"

    _description = ""
    _scheme = None

    def __init__(self, scheme, description=""):
        """Abstract integration scheme.
        The integration scheme itself is callable.
        
        Parameters
        ----------
        scheme : callable
            Function that returns the delta of the variable to be integrated
        description : string, optional, default : ""
            Descriptive string of the integration scheme"""
        self.scheme = scheme
        self.description = description

    @property
    def scheme(self):
        return self._scheme
    @scheme.setter
    def scheme(self, value):
        if not hasattr(value, "__call__"):
            raise TypeError("Scheme function needs to be callable.")
        self._scheme = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    def __call__(self, Y, dx=None):
        """Method for returning the delta of the variable to be integrated.
        
        Parameters
        ----------
        Y : Field
            Variable to be integrated
        dx : Intvar, optional, default : None
            Stepsize
            
        Returns
        -------
        dY : Field or False
            Delta of the integration variable.
            Functions needs to return False if integration failed."""
        return self.scheme(Y, dx)

    def __str__(self):
        return AbstractGroup.__str__(self)

    def __repr__(self):
        return self.__str__()