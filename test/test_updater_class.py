import numpy as np
from simframe.frame import Frame
from simframe.frame import Updater

import pytest

sim = Frame()
sim.N = 5

# Check if Updater returns a value
def myfunc_ret(sim):
    return np.ones(sim.N, dtype=np.int)
u = Updater(myfunc_ret)
assert np.all(u.update(sim) == np.ones(sim.N, dtype=np.int))

# Check if Updater executes operation
def myfunc_inst(sim):
    sim.N += 1
u = Updater(myfunc_inst)
u.update(sim)
assert sim.N == 6

# Check if updating with additional positional arguments work
def myfunc_string_arg(sim, string):
    return string
u = Updater(myfunc_string_arg)
assert "test" == u.update(sim, "test")

# Check if updating with additional keyword arguments work
def myfunc_string_kwarg(sim, string=""):
    return string
u = Updater(myfunc_string_kwarg)
assert "" == u.update(sim)
assert "test" == u.update(sim, string="test")

# Check if updating with additional positional arguments and keyword arguments work
def myfunc_string_arg_kwarg(sim, string1, string2=""):
    return string1 + string2
u = Updater(myfunc_string_arg_kwarg)
assert "test" == u.update(sim, "test")
assert "test" == u.update(sim, "", string2="test")
assert "testtest" == u.update(sim, "test", string2="test")

# Check if Updater raises error upon wrong initialization
with pytest.raises(TypeError):
    u = Updater("test")