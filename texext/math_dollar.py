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

    See: :func:`rst_dollars_to_math` for details.

    Parameters
    ----------
    source : sequence of str
        Sequence of strings, usually read from a ReST source file.  `source`
        modified in place.  There should only be one element, a single string.
    """
    s = "\n".join(source)
    source[:] = [rst_dollars_to_math(s)]


class StringProtector(object):
    """ Replace / restore text in regexp groups with markers.

    Replace identified text with markers using ``obj.protect(in_str)``
    Restore replaced text in place of markers with ``obj.restore(in_str)``
    """

    def __init__(self, regexps):
        self.regexps = tuple(re.compile(r) for r in regexps)
        self._marker_contents = []
        # Marker unique to this instance
        self._marker_fmt = "___XXX_REPL_{:d}_{{:d}}___".format(id(self))

    def _repl(self, matchobj):
        content = matchobj.group(0)
        marker_contents = self._marker_contents
        marker = self._marker_fmt.format(len(marker_contents))
        marker_contents.append((marker, content))
        return marker

    def protect(self, in_str):
        out_str = in_str
        for regexp in self.regexps:
            out_str = regexp.sub(self._repl, out_str)
        return out_str

    def restore(self, in_str):
        # Change everything back that we pulled out
        # Put back in reverse order of removal.
        out_str = in_str
        for marker, content in self._marker_contents[::-1]:
            out_str = out_str.replace(marker, content)
        self._marker_contents = []
        return out_str

    def __add__(self, other):
        return self.__class__(self.regexps + other.regexps)


in_dollars_protector = StringProtector(
    (
    # This searches for "$blah$" inside a pair of curly braces --
    # don't change these, since they're probably coming from a nested
    # math environment.  So for each match, we replace it with a temporary
    # string, and later on we substitute the original back.
    re.compile(r"({[^{}$]*\$[^{}$]*\$[^{}]*})"),
    )
)

rst_protector = StringProtector(
    (
    # Line entirely containing backticks ending with optional whitespace
    # These happen in unusual heading underlines
    re.compile(r"^(`+\s*)$", flags=re.MULTILINE),
    # Anything between double backticks
    re.compile(r"(``[^`]*?``)"),
    # Anything between single backticks
    re.compile(r"(`[^`]*?`)"),
    # matches any line starting with whitespace
    re.compile(r"^([\t ]+.*)$", flags=re.MULTILINE),
    )
) + in_dollars_protector


def rst_dollars_to_math(rst_str,
                        protector=rst_protector,
                        dollar_repl=r":math:`\1`"):
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
    protector : :class:`StringProtector` instance
        Object defining which regexps should be protected from dollar
        replacement.  Default is module global ``rst_protector`` instance.
    dollar_repl : string or callable
        Replacement expression for found text between (and including) dollars.

    Returns
    -------
    out_str : str
        Possibly modified string after replacing math dollar markers.
    """
    if rst_str.find("$") == -1:
        return rst_str
    out_str = protector.protect(rst_str)
    # matches $...$
    dollars = re.compile(r"(?<!\$)(?<!\\)\$([^\$]+?)\$")
    # regular expression for \$
    slashdollar = re.compile(r"\\\$")
    out_str = dollars.sub(dollar_repl, out_str)
    out_str = slashdollar.sub(r"$", out_str)
    return rst_protector.restore(out_str)


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
