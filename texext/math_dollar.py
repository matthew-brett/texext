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


def d2m_source(source):
    r"""
    Replace dollar signs with backticks in string within `source` list

    See: :func:`dollars_to_math` for details.

    Parameters
    ----------
    source : sequence of str
        Sequence of strings, usually read from a ReST source file.  `source`
        modified in place.  There should only be one element, a single string.
    """
    s = "\n".join(source)
    source[:] = [dollars_to_math(s)]


def dollars_to_math(rst_str):
    """
    Replace dollar signs with backticks in string `rst_str`

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
    rst_str : str
        String, usually read from a ReST source file.

    Returns
    -------
    out_str : str
        Possibly modified string after replacing math dollar markers.
    """
    if rst_str.find("$") == -1:
        return rst_str
    out_str = rst_str
    _data = []
    def repl(matchobj):
        s = matchobj.group(0)
        t = "___XXX_REPL_%d___" % len(_data)
        _data.append((t, s))
        return t
    # Line entirely containing backticks ending with optional whitespace
    # These happen in unusual heading underlines
    out_str = re.sub(r"^(`+\s*)$", repl, out_str, flags=re.MULTILINE)
    # Anything between double backticks
    out_str = re.sub(r"(``[^`]*?``)", repl, out_str)
    # Anything between single backticks
    out_str = re.sub(r"(`[^`]*?`)", repl, out_str)
    # matches any line starting with whitespace
    out_str = re.sub(r"^([\t ]+.*)$", repl, out_str, flags=re.MULTILINE)
    # This searches for "$blah$" inside a pair of curly braces --
    # don't change these, since they're probably coming from a nested
    # math environment.  So for each match, we replace it with a temporary
    # string, and later on we substitute the original back.
    out_str = re.sub(r"({[^{}$]*\$[^{}$]*\$[^{}]*})", repl, out_str)
    # matches $...$
    dollars = re.compile(r"(?<!\$)(?<!\\)\$([^\$]+?)\$")
    # regular expression for \$
    slashdollar = re.compile(r"\\\$")
    out_str = dollars.sub(r":math:`\1`", out_str)
    out_str = slashdollar.sub(r"$", out_str)
    # Change everything back that we pulled out before our dollar replacement.
    # Put back in reverse order of removal.
    for marker, content in _data[::-1]:
        out_str = out_str.replace(marker, content)
    return out_str


def process_dollars(app, docname, source):
    d2m_source(source)


def mathdollar_docstrings(app, what, name, obj, options, lines):
    d2m_source(lines)


def setup(app):
    app.connect("source-read", process_dollars)
    try:
        app.connect('autodoc-process-docstring', mathdollar_docstrings)
    except ExtensionError:
        warn("Need autodoc extension loaded for math_dollar to work on "
             "docstrings")
