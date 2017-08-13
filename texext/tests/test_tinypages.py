""" Tests for tinypages build using sphinx extensions """

from os.path import (join as pjoin, dirname, isdir)

import six

from sphinxtesters import ModifiedPageBuilder

from nose.tools import assert_true, assert_equal

HERE = dirname(__file__)
PAGES = pjoin(HERE, 'tinypages')


class TestTinyPages(ModifiedPageBuilder):
    # Test build and output of tinypages project
    page_source_template = PAGES

    def test_some_math(self):
        assert_true(isdir(self.out_dir))
        assert_true(isdir(self.doctree_dir))
        doctree = self.get_doctree('some_math')
        assert_equal(len(doctree.document), 1)
        tree_str = self.doctree2str(doctree)
        expected_base = (
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
            '<displaymath docname="some_math" label="None" '
            'latex="10 a + 2 b + q" nowrap="False"{number_default}/>\n'
            '<paragraph>More text</paragraph>\n'
            '<target refid="equation-some-label"/>\n'
            '<displaymath docname="some_math" '
            """ids="[{u_if_py2}'equation-some-label']" """
            'label="some-label" '
            'latex="5 a + 3 b" nowrap="False"{eq_number}/>\n'
            '<paragraph>Yet more text</paragraph>\n'
            '<displaymath docname="some_math" label="None" '
            'latex="5 w + 3 x" nowrap="False"{number_default}/>\n'
            r'<paragraph>Math with <math latex="\beta"/> a backslash.'
            '</paragraph>\n'
            '<paragraph>'  # What happens to backslashes?
            'A protected whitespace with <math latex="dollars"/>.'
            '</paragraph>\n'
            '<paragraph>'
            'Some * asterisks *.  <math latex="dollars"/>. '
            'A line break.  Protected \ backslash.  '
            'Protected n in <math latex="a"/> line.</paragraph>\n'
            # Do labels get set as targets?
            '{back_ref}.</paragraph>')
        u_if_py2 = '' if six.PY3 else 'u'
        expected_late = (
            expected_base.format(
                # Sphinx 1.5.1
                eq_number=' number="1"',
                u_if_py2=u_if_py2,
                number_default=' number="None"',
                back_ref=(
                    '<paragraph>Refers to equation at '
                    '<pending_xref refdoc="some_math" refdomain="math" '
                    'refexplicit="False" reftarget="some-label" '
                    'reftype="eq" refwarn="True">'
                    '<literal classes="xref eq">some-label</literal>'
                    '</pending_xref>')))
        expected_early = (
            expected_base.format(
                # Sphinx 1.3.1
                eq_number='',
                u_if_py2=u_if_py2,
                number_default='',
                back_ref=(
                    '<paragraph>Refers to equation at '
                    '<eqref docname="some_math" '
                    'target="some-label">(?)</eqref>')))
        assert_true(tree_str in (expected_late, expected_early))


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
