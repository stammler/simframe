from simframe import Frame
from simframe.frame import Field
from simframe.frame import Group
from simframe.frame import Updater

import pytest

sim = Frame()

# Adding group to frame
sim.addgroup("g")
assert isinstance(sim.g, Group)

# Adding fields to group
sim.g.addfield("a", 0)
sim.g.addfield("b", 1)
assert isinstance(sim.g.a, Field)
assert isinstance(sim.g.b, Field)

# Adding function as updater to group
def update_group(sim):
    sim.g.a.update()
    sim.g.b.update()
sim.g.updater = update_group
assert isinstance(sim.g.updater, Updater)

# Executing updater
def increment_a(sim):
    return sim.g.a + 1
def increment_b(sim):
    return sim.g.b + 1
sim.g.a.updater = increment_a
sim.g.b.updater = increment_b
sim.g.update()
assert sim.g.a == 1
assert sim.g.b == 2

# Adding Updater directly to group
u = Updater(update_group)
sim.g.updater = u
assert isinstance(sim.g.updater, Updater)
sim.g.update()
assert sim.g.a == 2
assert sim.g.b == 3

# Adding list as update instruction to group
sim.g.updater = ["a", "b"]
assert isinstance(sim.g.updater, list)
sim.g.update()
assert sim.g.a == 3
assert sim.g.b == 4

# Checking that the list instructions are executed in the correct order
sim.addfield("c", 1)
def increment_a_update_c(sim):
    sim.c += sim.c
    return sim.g.a + 1
def increment_b_update_c(sim):
    sim.c *= sim.c
    return sim.g.b + 1
sim.g.a.updater = increment_a_update_c
sim.g.b.updater = increment_b_update_c
sim.g.update()
assert sim.g.a == 4
assert sim.g.b == 5
assert sim.c == 4
sim.g.updater = ["b", "a"]
sim.g.update()
assert sim.g.a == 5
assert sim.g.b == 6
assert sim.c == 32

# Checking for updater of frame works
sim.updater = ["g"]
sim.update()
assert sim.g.a == 6
assert sim.g.b == 7
assert sim.c == 2048