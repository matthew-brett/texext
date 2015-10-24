""" Tests for tinypages build using sphinx extensions """

from os.path import (join as pjoin, dirname, isdir)

from .pagebuilder import setup_module, PageBuilder

from nose.tools import assert_true, assert_equal

HERE = dirname(__file__)
PAGES = pjoin(HERE, 'tinypages')


class TestTinyPages(PageBuilder):
    # Test build and output of tinypages project
    page_path = PAGES

    def test_some_math(self):
        assert_true(isdir(self.html_dir))
        assert_true(isdir(self.doctree_dir))
        doctree = self.get_doctree('some_math')
        assert_equal(len(doctree.document), 1)
        tree_str = self.doctree2str(doctree)
        assert_equal(
            '<title>Some math</title>\n'
            '<paragraph>Here <math latex="a = 1"/>, except '
            '<title_reference>$b = 2$</title_reference>.</paragraph>\n'
            '<paragraph>Here <math latex="a = 1"/>, except '
            '<literal>$b = 2$</literal>.</paragraph>\n'
            '<literal_block xml:space="preserve">'
            'Here $a = 1$</literal_block>\n'
            '<displaymath docname="some_math" label="None" '
            'latex="10 a + 2 b + q" nowrap="False"/>\n'
            '<paragraph>More text</paragraph>\n'
            '<target refid="equation-some-label"/>\n'
            '<displaymath docname="some_math" '
            """ids="[u'equation-some-label']" """
            'label="some-label" '
            'latex="5 a + 3 b" nowrap="False"/>\n'
            '<paragraph>Yet more text</paragraph>\n'
            '<displaymath docname="some_math" label="None" '
            'latex="5 w + 3 x" nowrap="False"/>',
            tree_str)
