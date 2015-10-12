""" Tests for plotdirective build using sphinx extensions

Test ability to combine plot_directive with mathcode
"""

import pickle
from os.path import dirname, join as pjoin

from .pagebuilder import setup_module, PageBuilder

from nose.tools import assert_true, assert_equal

PAGES = pjoin(dirname(__file__), 'plotdirective')


class TestPlotDirective(PageBuilder):
    # Test build and output of tinypages project
    page_path = PAGES

    def test_plot_and_math(self):
        with open(pjoin(self.doctree_dir, 'plot_and_math.doctree'), 'rb') as fobj:
            content = fobj.read()
        doctree = pickle.loads(content)
        assert_equal(len(doctree.document), 1)
        para_strs = [str(p) for p in doctree.document[0]]
        assert_equal(para_strs[:2],
                     ['<title>Plot directive with mathcode</title>',
                      '<paragraph>Some text</paragraph>'])
        if 'highlight_args' in para_strs[2]:  # sphinx 1.3.1 back to ?
            assert_equal(
                para_strs[2],
                '<literal_block highlight_args="{}" language="python" '
                'linenos="False" xml:space="preserve">a = 101</literal_block>')
        else:  # sphinx 1.1.3 up until ?
            assert_equal(
                para_strs[2],
                '<literal_block language="python" '
                'linenos="False" xml:space="preserve">a = 101</literal_block>')
        assert_equal(para_strs[3:],
                     ['<only expr="html"/>',
                      '<only expr="latex"/>',
                      '<only expr="texinfo"/>',
                      '<paragraph>More text</paragraph>',
                      '<displaymath docname="plot_and_math" label="None" '
                      'latex="101" nowrap="False"/>'])
