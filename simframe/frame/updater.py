class Updater():
    """Class that manages how a group or field is updated
    
    Parameter
    ---------
    func : callable, optional, default : None
        Function that is called when update function is called. None is a null operation.
        
    Examples
    --------
    >>> myupdater = Updater(myfunction)"""

    __name__ = "Updater"

    _func = None
    
    def __init__(self, func=None):
        self._func = func
        
    def update(self, owner, *args, **kwargs):
        """Function that is called when group or field to which Updater belongs is being updated."""
        if self._func is not None:  return self._func(owner, *args, **kwargs)

    def __str__(self):
        return "{:5s}".format(str(self.__name__))

    def __repr__(self):
        return self.__str__()