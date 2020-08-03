"""main initialization file of the simframe module"""
from simframe.frame import Frame
from simframe.frame import Integrator
from simframe.integration import Scheme
from simframe.integration import Instruction

from pkg_resources import get_distribution
__version__ = get_distribution(__name__).version

__all__ = ["Frame", "Integrator", "Scheme", "Instruction"]