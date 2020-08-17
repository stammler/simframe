from simframe.frame.abstractgroup import AbstractGroup


class Scheme:
    """Class for an abstract integration scheme that can be used as template for creating custom schemes.

    Notes
    -----
    The integration scheme needs to return False if the integration failed. The integrator will then
    perform a fail operation and will try it again. This can be used to implement schemes with adaptive
    step sizes. If the step size was not small enough the fail operation can reduce it further."""

    __name__ = "Scheme"

    _description = ""
    _controller = {}
    _scheme = None

    def __init__(self, scheme, controller={}, description=""):
        """Abstract integration scheme.
        The integration scheme itself is callable.

        Parameters
        ----------
        scheme : callable
            Function that returns the delta of the variable to be integrated
        description : string, optional, default : ""
            Descriptive string of the integration scheme"""
        self.scheme = scheme
        self.controller = controller
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
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        if not isinstance(value, dict):
            raise TypeError("controller has to be of type dict.")
        self._controller = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    def __call__(self, x0, Y0, dx, controller={}):
        """Method for returning the delta of the variable to be integrated.

        Parameters
        ----------
        x0 : Intvar
            Integration variable at beginning of scheme
        Y0 : Field
            Variable to be integrated at the beginning of scheme
        dx : IntVar
            Stepsize of integration variable
        controller : dict, optional, default : {}
            Additional keyword arguments passed to integration scheme


        Returns
        -------
        dY : Field or False
            Delta of the integration variable.
            Functions needs to return False if integration failed."""
        return self.scheme(x0, Y0, dx, controller=self.controller)

    def __str__(self):
        return AbstractGroup.__str__(self)

    def __repr__(self):
        return self.__str__()
