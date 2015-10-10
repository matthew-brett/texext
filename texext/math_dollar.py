# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the texext package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
""" Sphinx source processor to replace $a=b$ with :math:`a=b`
"""
from warnings import warn

import re

from sphinx.errors import ExtensionError


def dollars_to_math(source):
    r"""
    Replace dollar signs with backticks.

    More precisely, do a regular expression search.  Replace a plain dollar
    sign ($) by a backtick (`).  Replace an escaped dollar sign (\$) by a
    dollar sign ($).  Don't change a dollar sign preceded or followed by a
    backtick (`$ or $`), because of strings like "``$HOME``".  Don't make any
    changes on lines starting with spaces, because those are indented and hence
    part of a block of code or examples.

    This also does not replace dollar signs enclosed in curly braces, to avoid
    nested math environments, such as::

      $f(n) = 0 \text{ if $n$ is prime}$

    Thus the above line would get changed to

      `f(n) = 0 \text{ if $n$ is prime}`

    Parameters
    ----------
    source : sequence of str
        Sequence of strings, usually read from a ReST source file.  `source`
        modified in place.  There should only be one element, a single string.
    """
    s = "\n".join(source)
    if s.find("$") == -1:
        return
    _data = {}
    def repl(matchobj):
        s = matchobj.group(0)
        t = "___XXX_REPL_%d___" % len(_data)
        _data[t] = s
        return t
    # matches any line starting with whitespace
    s = re.sub(r"^([\t ]+.*)$", repl, s, flags=re.MULTILINE)
    # Anything between double backticks
    s = re.sub(r"(``[^`]*?``)", repl, s)
    # Anything between single backticks
    s = re.sub(r"(`[^`]*?`)", repl, s)
    # This searches for "$blah$" inside a pair of curly braces --
    # don't change these, since they're probably coming from a nested
    # math environment.  So for each match, we replace it with a temporary
    # string, and later on we substitute the original back.
    s = re.sub(r"({[^{}$]*\$[^{}$]*\$[^{}]*})", repl, s)
    # matches $...$
    dollars = re.compile(r"(?<!\$)(?<!\\)\$([^\$]+?)\$")
    # regular expression for \$
    slashdollar = re.compile(r"\\\$")
    s = dollars.sub(r":math:`\1`", s)
    s = slashdollar.sub(r"$", s)
    # change everything back that we pulled out before our dollar replacement
    for r in _data:
        s = s.replace(r, _data[r])
    # now save results in "source"
    source[:] = [s]


def process_dollars(app, docname, source):
    dollars_to_math(source)


def mathdollar_docstrings(app, what, name, obj, options, lines):
    dollars_to_math(lines)


def setup(app):
    app.connect("source-read", process_dollars)
    try:
        app.connect('autodoc-process-docstring', mathdollar_docstrings)
    except ExtensionError:
        warn("Need autodoc extension loaded for math_dollar to work on "
             "docstrings")
