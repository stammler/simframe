"""main initialization file of the simframe module"""
from simframe.frame import Simulation
from simframe.io import Writer
from pkg_resources import get_distribution
__version__ = get_distribution(__name__).version

__all__ = ["Simulation", "Writer"]