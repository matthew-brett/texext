""" Tests for tinypages build using sphinx extensions """

from os.path import (join as pjoin, dirname, isdir)

import sphinx
SPHINX_ge_1p5 = sphinx.version_info[:2] >= (1, 5)

from sphinxtesters import PageBuilder

HERE = dirname(__file__)
PAGES = pjoin(HERE, 'tinypages')

from texext.tests.test_plotdirective import format_math_block

def _pdiff(str1, str2):
    # For debugging
    from difflib import ndiff
    print(''.join(ndiff(str1.splitlines(True), str2.splitlines(True))))


class TestTinyPages(PageBuilder):
    # Test build and output of tinypages project
    page_source_template = PAGES

    def test_some_math(self):
        assert isdir(self.out_dir)
        assert isdir(self.doctree_dir)
        doctree = self.get_doctree('some_math')
        assert len(doctree.document) == 1
        tree_str = self.doctree2str(doctree)
        if SPHINX_ge_1p5:
            back_ref = (
                '<paragraph>Refers to equation at '
                '<pending_xref refdoc="some_math" refdomain="math" '
                'refexplicit="False" reftarget="some-label" '
                'reftype="eq" refwarn="True">'
                '<literal classes="xref eq">some-label</literal>'
                '</pending_xref>')
        else:
            back_ref=(
                '<paragraph>Refers to equation at '
                '<eqref docname="some_math" '
                'target="some-label">(?)</eqref>')
        expected = (
            '<title>Some math</title>\n'
            '<paragraph>Here <math latex="a = 1"/>, except '
            '<title_reference>$b = 2$</title_reference>.</paragraph>\n'
            '<paragraph>Here <math latex="c = 3"/>, except '
            '<literal>$d = 4$</literal>.</paragraph>\n'
            '<literal_block xml:space="preserve">'
            'Here $e = 5$</literal_block>\n'
            '<bullet_list bullet="*">'
            '<list_item>'
            '<paragraph>'
            'A list item containing\n'
            '<math latex="f = 6"/> some mathematics.'
            '</paragraph>'
            '</list_item>'
            '<list_item>'
            '<paragraph>'
            'A list item containing '
            '<literal>a literal across\nlines</literal> '
            'and also <math latex="g = 7"/> some mathematics.'
            '</paragraph>'
            '</list_item>'
            '</bullet_list>\n'
            + format_math_block('some_math', "10 a + 2 b + q") +
            '\n<paragraph>More text</paragraph>\n'
            '<target refid="equation-some-label"/>\n'
            + format_math_block(
                'some_math', "5 a + 3 b",
                label='some-label',
                number='1',
                ids='equation-some-label') +
            '\n<paragraph>Yet more text</paragraph>\n'
            + format_math_block(
                "some_math", latex="5 w + 3 x") + '\n' +
            r'<paragraph>Math with <math latex="\beta"/> a backslash.'
            '</paragraph>\n'
            '<paragraph>'  # What happens to backslashes?
            'A protected whitespace with <math latex="dollars"/>.'
            '</paragraph>\n'
            '<paragraph>'
            'Some * asterisks *.  <math latex="dollars"/>. '
            r'A line break.  Protected \ backslash.  '
            'Protected n in <math latex="a"/> line.</paragraph>\n'
            # Do labels get set as targets?
            + back_ref +
            '.</paragraph>')
        assert tree_str == expected


class TestTopLevel(TestTinyPages):
    # Test we can import math_dollar with just `texext`

    @classmethod
    def modify_source(cls):
        conf_fname = pjoin(cls.page_source, 'conf.py')
        with open(conf_fname, 'rt') as fobj:
            contents = fobj.read()
        contents = contents.replace("'texext.mathcode',\n", "")
        contents = contents.replace("'texext.math_dollar'", "'texext'")
        with open(conf_fname, 'wt') as fobj:
            fobj.write(contents)
