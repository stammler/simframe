"""This package contains infrastructure for solving differential equations within ``simframe``. The ``Integrator`` class
is the basic class that advances the simulation from snapshot to snapshot by executing one integration ``Instruction`` at
a time. Instructions contain a list of integration ``Scheme``. The ``schemes`` package contains pre-defined integration
schemes that are ready to use in ``simframe``."""

from simframe.integration.instruction import Instruction
from simframe.integration.integrator import Integrator
from simframe.integration.scheme import Scheme
import simframe.integration.schemes as schemes

__all__ = ["Instruction",
           "Integrator",
           "Scheme",
           "schemes"]
