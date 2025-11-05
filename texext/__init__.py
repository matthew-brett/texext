""" Texext package """

from . import math_dollar
from . import mathcode

from . import _version
__version__ = _version.get_versions()['version']


def setup(app):
    math_dollar.setup(app)
    mathcode.setup(app)
    metadata = {"version": __version__, "parallel_read_safe": True}
    return metadata
