class Color(object):
    """Class to decorate strings with color tags."""

    _colors = {"black": "\033[30m",
               "red": "\033[91m",
               "green": "\033[92m",
               "yellow": "\033[93m",
               "blue": "\033[94m",
               "purple": "\033[95m",
               "cyan": "\033[96m",
               "white": "\033[98m",
               "reset": "\033[98m"}
    _cstr = "\033[0m"
    _reset = "\033[0m"
    _color = None

    def __init__(self, color="reset"):
        """Class colorizes strings

        Parameters
        ----------
        color : string, optional, default : "reset"
            Default color is user's standard"""
        self.color = color

    def __call__(self, s, color=None):
        """Colorizes string

        Parameters
        ----------
        s : string
            String to be colorized
        color : string, optional, default : None
            Color used to colorize. If None, standard color is used

        Returns
        -------
        cstr : string
            Colorized string"""
        if color is not None and self._checkcolor(color):
            cstr = self._colors[color]
        else:
            cstr = self._cstr
        return "{}{}{}".format(cstr, s, self._reset)

    def _checkcolor(self, color):
        if color in self._colors.keys():
            return True
        else:
            raise ValueError("'{}' is not a valid color.".format(color))

    @property
    def color(self):
        '''Of type ``Color`` with color information.'''
        return self._color

    @color.setter
    def color(self, value):
        if self._checkcolor(value):
            self._color = value
            self._cstr = self._colors[value]


colorize = Color()
