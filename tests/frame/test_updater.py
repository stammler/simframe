# Tests for Updater class


from simframe.frame import Updater


def test_updater_repr_str():
    upd = Updater()
    assert isinstance(repr(upd), str)
    assert isinstance(str(upd), str)
