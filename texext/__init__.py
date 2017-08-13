""" Texext package """

from . import math_dollar
from . import mathcode

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


def setup_package():
    # Prevent nose tests running setup function
    pass


def setup(app):
    math_dollar.setup(app)
    mathcode.setup(app)
