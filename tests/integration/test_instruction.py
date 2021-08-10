# Tests for the Instruction class


import pytest
from simframe import Frame
from simframe import Instruction
from simframe import schemes
from simframe.frame import Field


def test_instruction_no_field():
    with pytest.raises(TypeError):
        i = Instruction(schemes.expl_1_euler, None)


def test_instruction_wrong_step_factor():
    f = Frame()
    fi = Field(f, 0.)
    with pytest.raises(TypeError):
        i = Instruction(schemes.expl_1_euler, fi, fstep=None)
    with pytest.raises(ValueError):
        i = Instruction(schemes.expl_1_euler, fi, fstep=0.)
    with pytest.raises(ValueError):
        i = Instruction(schemes.expl_1_euler, fi, fstep=1.1)
