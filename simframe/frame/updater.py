class Updater():
    """Class that manages how a group or field is updated
    
    Parameter
    ---------
    func : callable
        Function that is called when update function is called.
        
    Examples
    --------
    >>> myupdater = Updater(myfunction)"""

    __name__ = "Updater"
    
    def __init__(self, func):
        if not hasattr(func, '__call__'):
            raise TypeError("<func> is not callable.")
        self._func = func
        
    def update(self, owner, *args, **kwargs):
        """Function that is called when group or field to which Updater belongs is being updated."""
        return self._func(owner, *args, **kwargs)

    def __str__(self):
        return "{:6s}".format(str(self.__name__))

    def __repr__(self):
        return self.__str__()