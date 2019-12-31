""" Tests for plotdirective build using sphinx extensions

Test ability to combine plot_directive with mathcode
"""

from os.path import dirname, join as pjoin
import re

from six import PY3

import sphinx

SPHINX_ge_1p8 = sphinx.version_info[:2] >= (1, 8)
SPHINX_ge_1p7 = sphinx.version_info[:2] >= (1, 7)
SPHINX_ge_1p5 = sphinx.version_info[:2] >= (1, 5)

from sphinxtesters import PageBuilder

PAGES = pjoin(dirname(__file__), 'plotdirective')


def format_math_block(name, latex, label=None, number=None,
                      ids=None):
    """ Simulate math block output from Sphinx at different versions
    """
    if SPHINX_ge_1p8:
        number = 'True' if number is None else number
        label = 'True' if label is None else label
        id_part = '' if ids is None else 'ids="{}" '.format(ids)
        return (
            '<math_block docname="{}" {}label="{}" '
            'nowrap="False" number="{}" xml:space="preserve">{}'
            '</math_block>'.format(name, id_part, label, number, latex)
        )
    number = 'None' if number is None else number
    label = 'None' if label is None else label
    # Sphinx >= 1.5 has number="" clause in parameters
    number_part = ' number="{}"'.format(number) if SPHINX_ge_1p5 else ''
    u_prefix = '' if PY3 or SPHINX_ge_1p7 else 'u'
    id_part = '' if ids is None else """ids="[{}'{}']" """.format(
        u_prefix, ids)
    return (
        '<displaymath docname="{}" {}label="{}" '
        'latex="{}" nowrap="False"{}/>'.format(
            name, id_part, label, latex, number_part)
    )

EXP_PLOT_AND_MATH = (
    '<title>Plot directive with mathcode</title>\n'
    '<paragraph>Some text</paragraph>\n'
    r'<literal_block '
    '(force="False" )?'
    '(highlight_args="{}" )?'
    'language="python" '
    '(linenos="False" )?'
    'xml:space="preserve">a = 101</literal_block>\n'
    '<only expr="html"/>\n'
    '<only expr="(not html|latex"/>\n'
    '<only expr="texinfo)"/>\n'
    '<paragraph>More text</paragraph>\n'
    + format_math_block('plot_and_math', '101'))


class TestPlotDirective(PageBuilder):
    # Test build and output of custom_plotdirective project
    page_source_template = PAGES

    def test_plot_and_math(self):
        doctree = self.get_doctree('plot_and_math')
        assert len(doctree.document) == 1
        tree_str = self.doctree2str(doctree)
        assert re.compile(EXP_PLOT_AND_MATH).search(tree_str)


class TestTopPlotDirective(TestPlotDirective):
    # Test we can import mathcode with just `texext`

    @classmethod
    def modify_source(cls):
        conf_fname = pjoin(cls.page_source, 'conf.py')
        with open(conf_fname, 'rt') as fobj:
            contents = fobj.read()
        contents = contents.replace("'texext.mathcode'", "'texext'")
        with open(conf_fname, 'wt') as fobj:
            fobj.write(contents)
