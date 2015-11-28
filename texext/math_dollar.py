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
from functools import partial

from docutils.utils import escape2null, unescape
from docutils.nodes import Text, SparseNodeVisitor, paragraph
from sphinx.errors import ExtensionError
from sphinx.ext.mathbase import math


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


MATH_MARKER = "__D2M__"
txt_dollars_to_math = partial(rst_dollars_to_math,
                              protector=in_dollars_protector,
                              dollar_repl=MATH_MARKER + r"\1" + MATH_MARKER)


class MathDollarMaker(SparseNodeVisitor):

    def visit_Text(self, node):
        # Avoid literals etc
        if not isinstance(node.parent, paragraph):
            return
        in_str = node.rawsource
        processed = txt_dollars_to_math(in_str)
        if MATH_MARKER not in processed:
            return
        parts = processed.split(MATH_MARKER)
        new_nodes = []
        for i, part in enumerate(parts):
            with_nulls = escape2null(part)
            to_backslashes = unescape(with_nulls, restore_backslashes=True)
            if part == '':
                continue
            if i % 2:  # See sphinx.ext.mathbase
                new_node = math(latex=to_backslashes)
            else:
                new_node = Text(unescape(with_nulls), to_backslashes)
            new_node.parent = node.parent
            new_nodes.append(new_node)
        # Put new nodes into parent's list of children
        new_children = []
        for child in node.parent.children:
            if not child is node:
                new_children.append(child)
            else:
                new_children += new_nodes
        node.parent.children = new_children

    def unknown_visit(self, node):
        pass


def dt_process_dollars(app, doctree):
    doctree.walk(MathDollarMaker(doctree.document))


def mathdollar_docstrings(app, what, name, obj, options, lines):
    d2m_source(lines)


def setup(app):
    # Process pages after parsing ReST to avoid false positives
    app.connect("doctree-read", dt_process_dollars)
    try:
        # We have to process docstrings as text, it's the Wild Wild West.
        app.connect('autodoc-process-docstring', mathdollar_docstrings)
    except ExtensionError:
        warn("Need autodoc extension loaded for math_dollar to work on "
             "docstrings")
