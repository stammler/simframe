# Tests for progress bar


from simframe.io import Progressbar
from simframe.io.progress import Spinner
from simframe.utils import Color


def test_progress_init_with_color():
    c = Color()
    pb = Progressbar(color=c)
    assert pb._color == c


def test_progress_init_with_spinner():
    s = Spinner()
    pb = Progressbar(spinner=s)
    assert pb._spinner == s


def test_progress_print():
    pb = Progressbar()
    pb._print = True
    pb.print(0.25, 0.2, 0.3, 0., 1.)
    pb.print(0.25, 0.2, 0.3, 0., 1.)
    assert pb._speed == 0.
    pb.print(0.26, 0.2, 0.3, 0., 1.)
    pb.print(0.3, 0.3, 0.4, 0., 1.)
