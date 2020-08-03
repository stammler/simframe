from simframe.frame.updater import Updater

class AbstractGroup(object):
    """This is an abstract class that should not be instanced directly. It only serves as templates for other classes."""
    
    __name__ = None
    _updater = None
    _systole = None
    _diastole = None
    _description = None
        
    def _constructupdater(self, u=None):
        """Helper method to construct updaters including type checks.
        Do not call this method directly!"""

        if isinstance(u, Updater):
            return u
        if hasattr(u, '__call__'):
            return Updater(u)
        if isinstance(u, list):
            for val in u:
                if not isinstance(val, str):
                    raise ValueError("<u> has to be list of str.")
            return u
        if u is None:
            return u
        raise ValueError("<u> has invalid type.")

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if not isinstance(value, (str, type(None))):
            raise ValueError("<value> has to be of type str.")
        self._description = value

    @property
    def updater(self):
        return self._updater
    @updater.setter
    def updater(self, value):
        self._updater = self._constructupdater(value)

    @property
    def systole(self):
        return self._systole
    @systole.setter
    def systole(self, value):
        self._systole = self._constructupdater(value)

    @property
    def diastole(self):
        return self._diastole
    @diastole.setter
    def diastole(self, value):
        self._diastole = self._constructupdater(value)

    def __str__(self):
        ret = "{:6s}".format(str(self.__name__))
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret

    def _cyclethrough(self, haystack, needle):
        """Function that cycles through object structure to find object.
        This is meant to find an object within a frame structure and replace it with another object.
        
        Parameters
        ----------
        haystack : object
            Uppermost object to search through
        needle : object
            Object to look for in haystack
            
        Returns
        -------
        dict, key
            Dictionary and key of object location"""

        for key, val in haystack.__dict__.items():
            if key == "_owner": continue    # To prevent recursion
            if val is needle:
                return haystack.__dict__, key
            else:
                if hasattr(val, "__dict__"):
                    self._cyclethrough(val, needle)