r""" A module to test docstring parsing with math such as $\gamma = \cos(\alpha)$

Need to test other markup - so: `a link <https://github.com>`_.
"""


def func():
    r""" A docstring with math in first line $z = \beta$

    With some more $a = 1$ math. Math across lines - $b
    = 2$.

    Further, there is a link_ and a |substitution|.

    .. _link: https://python.org
    .. |substitution| replace:: substituted
    """
