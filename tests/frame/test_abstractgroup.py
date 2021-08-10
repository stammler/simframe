# Tests for AbstractGroup class


import pytest
from simframe.frame import AbstractGroup


def test_abstract_group_init_attributes():
    ag = AbstractGroup()
    string = "test"
    ag.description = string
    assert ag.description == string
    with pytest.raises(TypeError):
        ag.description = 1


def test_abstractgroup_repr_str():
    ag = AbstractGroup()
    assert isinstance(repr(ag), str)
    assert isinstance(str(ag), str)
