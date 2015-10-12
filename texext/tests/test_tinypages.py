""" Tests for tinypages build using sphinx extensions """

import pickle

from os.path import (join as pjoin, dirname, isdir)

from .pagebuilder import setup_module, PageBuilder

from nose.tools import assert_true, assert_equal

HERE = dirname(__file__)
TINY_PAGES = pjoin(HERE, 'tinypages')


class TestTinyPages(PageBuilder):
    # Test build and output of tinypages project
    page_path = TINY_PAGES

    def test_some_math(self):
        assert_true(isdir(self.html_dir))
        assert_true(isdir(self.doctree_dir))
        with open(pjoin(self.doctree_dir, 'some_math.doctree'), 'rb') as fobj:
            content = fobj.read()
        doctree = pickle.loads(content)
        assert_equal(len(doctree.document), 1)
        para_strs = [str(p) for p in doctree.document[0]]
        assert_equal(
            para_strs,
            ['<title>Some math</title>',
             '<paragraph>Here <math latex="a = 1"/>, except '
             '<title_reference>$b = 2$</title_reference>.</paragraph>',
             '<paragraph>Here <math latex="a = 1"/>, except '
             '<literal>$b = 2$</literal>.</paragraph>',
             '<literal_block xml:space="preserve">Here $a = 1$</literal_block>',
             '<displaymath docname="some_math" label="None" '
             'latex="10 a + 2 b + q" nowrap="False"/>',
             '<paragraph>More text</paragraph>',
             '<target refid="equation-some-label"/>',
             '<displaymath docname="some_math" '
             """ids="[u'equation-some-label']" """
             'label="some-label" '
             'latex="5 a + 3 b" nowrap="False"/>',
             '<paragraph>Yet more text</paragraph>',
             '<displaymath docname="some_math" label="None" '
             'latex="5 w + 3 x" nowrap="False"/>'])
