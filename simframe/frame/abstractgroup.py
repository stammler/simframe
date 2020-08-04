from simframe.frame.updater import Updater
from simframe.frame.heartbeat import Heartbeat

class AbstractGroup(object):
    """This is an abstract class that should not be instanced directly. It only serves as templates for other classes."""
    
    __name__ = None
    _updater = None
    _description = None
        
    def _constructheartbeat(self, u=None):
        """Helper method to construct updaters including type checks.
        Do not call this method directly!"""
        return Heartbeat(updater=u)

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
        self._updater = self._constructheartbeat(value)

    def __str__(self):
        ret = "{:6s}".format(str(self.__name__))
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret