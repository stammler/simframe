# Tests for Updater class


from simframe.frame.frame import Frame
from simframe.frame import Updater


def test_updater_repr_str():
    upd = Updater()
    assert isinstance(repr(upd), str)
    assert isinstance(str(upd), str)

    f = Frame()

    def func(f):
        pass

    f.updater = func
    assert isinstance(repr(f.updater.updater), str)
    assert isinstance(str(f.updater.updater), str)
