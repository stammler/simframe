# Tests for Scheme class


import pytest
from simframe.integration import Scheme


def test_scheme_repr_str():
    def f():
        pass
    s = Scheme(f)
    assert isinstance(repr(s), str)
    assert isinstance(str(s), str)


def test_scheme_attributes():
    def f():
        pass
    with pytest.raises(TypeError):
        s = Scheme(f, controller=None)
    with pytest.raises(TypeError):
        s = Scheme(None)
    s = Scheme(f)
    with pytest.raises(TypeError):
        s.description = None
