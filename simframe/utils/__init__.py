"""Package contains utility classes that facilitate the use of ``simframe``

``Color`` is a generic class that can be used to colorize text. ``colorize``
is an instance of ``Color``, that can be called to add decorators to a string
for colored output."""

from simframe.utils.color import Color
from simframe.utils.color import colorize
from simframe.utils.format import byteformat
from simframe.utils.simplenamespace import SimpleNamespace

__all__ = [
    "Color",
    "colorize",
    "byteformat",
    "SimpleNamespace",
]
