from datetime import timedelta
from itertools import cycle
import numpy as np
from time import monotonic
from time import strftime
import sys

from simframe.utils.color import Color


class Progressbar(object):
    """Class for printing progress bar to terminal."""

    _line1 = ""
    _line2 = ""
    _N1 = 0
    _N2 = 0

    def __init__(self, prefix=" ", suffix="| ", fill="▶", empty=" ", length=25, color="blue", spinner=None):
        """This class controls the output of a progress bar on screen.

        Parameters
        ----------
        prefix, string, optional, default : " "
            Initial character of bar
        suffix, string, optional, default : "| "
            Final character of bar
        fill, string, optional, default : "▶"
            Progress character
        empty, string, optional, default : " "
            Character progress has not reached, yet
        length, int, optional, default : 25
            Number of fill/empty characters between prefix and suffix
        color, string or Color, optional, default : "blue"
            Color of bar and spinner
        spinner, Spinner or None, optional, default : None
            Work indicator. If None, standard spinner is used"""
        self._prefix = prefix
        self._suffix = suffix
        self._fill = fill
        self._empty = empty
        self._length = length
        if isinstance(color, Color):
            self._color = color
        else:
            self._color = Color(color)
        if isinstance(spinner, Spinner):
            self._spinner = spinner
        else:
            self._spinner = Spinner()
        # Check if we're in an interactive shell. If not, we don't print progress bar.
        self._print = sys.stdout.isatty()
        # Time keeping for calculating ETA
        self._N_speed = 25
        self._speedbuffer = np.zeros(self._N_speed)
        self._speed = None
        self._t = monotonic()
        self._x = None

    def _getbar(self, filled):
        """Returns actual progress bar between and including prefix and suffix

        Parameters
        ----------
        filled : int
            Number of filled characters in bar.

        Returns
        -------
        bar : string
            String between and including prefix and suffix"""
        bar = "{}{}{}{}".format(
            self._prefix, self._color(filled*self._fill), self._color((self._length-filled)*self._empty), self._suffix)
        return bar

    def _update_speed(self, x):
        '''Updates the current speed.

        Parameters
        ----------
        x : number
            current position of process'''
        t = monotonic()
        if self._x is not None:
            dx = x - self._x
            dt = t - self._t
            speed = dx/dt
            self._speedbuffer = np.insert(self._speedbuffer, 0, speed)[
                :self._N_speed]
            self._speed = self._speedbuffer.mean()
        self._t = t
        self._x = x.copy()

    def _geteta(self, x, s1):
        '''Returns the current ETA

        Parameters
        ----------
        x : number
            current positon of process
        s1 : number
            end position of process

        Returns
        -------
        ETA : string
            string with ETA.'''
        self._update_speed(x)
        if self._speed is None:
            return ""
        eta = (s1-x)/self._speed
        try:
            dt = timedelta(seconds=np.int(eta))
        except:
            dt = "N/A"
        ret = "ETA: {}".format(dt)
        return ret

    def _getline(self, text, x, x0, x1):
        """Returns complete progress bar line

        Parameters
        ----------
        text : string
            Legend of progress bar
        x : number
            Current state of progress
        x0 : number
            Starting point
        x1 : number
            End point

        Returns
        -------
        line : string
            Progress bar line"""
        f = (x-x0)/(x1-x0)
        filled = np.int(np.floor(f*self._length))
        line = "{:10s}{}{:5.1f} %".format(text, self._getbar(filled), f*100.)
        return line

    def _setlines(self, x, x0, x1, s0, s1):
        """Functions sets both progress bar lines for the current snapshot and
        the whole simulation into hidden attribute of class.

        Parameters
        ----------
        x : Number
            Current state of progress
        x0 : Number
            Starting point of snapshot
        x1 : Number
            End point of snapshot
        s0 : Number
            Starting point of simulation
        s1 : Number
            End point of simulation"""
        self._line1 = "{} {}".format(self._getline(
            "Snapshot", x, x0, x1), self._color(self._spinner.next()))
        eta = self._geteta(x, s1)
        self._line2 = "{} {}".format(
            self._getline("Simulation", x, s0, s1), self._color(eta))

    def print(self, x, x0, x1, s0, s1):
        """Function prints the current progress bar. If the end of either the snapshot
        or the simulation is reached, no progress bar will be printed.

        Parameters
        ----------
        x : Number
            Current state of progress
        x0 : Number
            Starting point of snapshot
        x1 : Number
            End point of snapshot
        s0 : Number
            Starting point of simulation
        s1 : Number
            End point of simulation"""
        # Only print if interactive
        if self._print:
            self._N1 = len(self._line1)
            self._N2 = len(self._line2)
            self._setlines(x, x0, x1, s0, s1)
            if not (x == x0 or x == s0):
                self._reset()
            msg = "\x1b[?25l\n{}\n{}".format(self._line1, self._line2)
            print(msg)
            sys.stdout.flush()

    def _reset(self):
        """Resets the current output of progress bar. Function resets the cursor to beginning
        of progress bar and overwrites it with whitespaces, then returns to beginning."""
        # Only print if interactive
        if self._print:
            msg = "\033[3A\r\n{}\n{}\033[3A\r\x1b[?25h".format(
                self._N1*" ", self._N2*" ")
            print(msg)
            sys.stdout.flush()

    def __call__(self, x, x0, x1, s0, s1):
        """Prints the current progress bar.

        Parameters
        ----------
        x : Number
            Current state of progress
        x0 : Number
            Starting point of snapshot
        x1 : Number
            End point of snapshot
        s0 : Number
            Starting point of simulation
        s1 : Number
            End point of simulation"""
        self.print(x, x0, x1, s0, s1)


class Spinner(object):
    """This is a class for displaying some information that the simulation is still runnging."""

    _cycle = None

    def __init__(self, charlist=["●", "○"]):
        """This class is cycling through a list of characters that are displayed after every successfully
        executed timestep.

        Parameters
        ----------
        charlist : list of strings, optional, default : ["●", "○"]
            List of characters to cycle through"""
        self._cycle = cycle(charlist)

    def next(self):
        """Function returns the next character in list"""
        return next(self._cycle)
