class AbstractScheme:

    __name__ = "Scheme"

    _scheme = None

    def __init__(self, scheme, description=""):
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
        if not isinstance(value, (str, type(None))):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    def __call__(self, dx, Y):
        return self.scheme(dx, Y)

    def __str__(self):
        ret = str(self.__name__)
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret

    def __repr__(self):
        return self.__str__()