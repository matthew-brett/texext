""" Tests for plotdirective build using sphinx extensions

Test ability to combine plot_directive with mathcode
"""

from os.path import dirname, join as pjoin
import re

import sphinx
SPHINX_1p8 = sphinx.version_info[:2] >= (1, 8)

from sphinxtesters import PageBuilder

from texext.tests.test_plotdirective import EXP_PLOT_AND_MATH

PAGES = pjoin(dirname(__file__), 'plotdirective')


class TestCustomPlotDirective(PageBuilder):
    # Test build and output of custom_plotdirective project
    page_source_template = PAGES

    @classmethod
    def modify_pages(cls):
        conf_fname = pjoin(cls.page_source, 'conf.py')
        with open(conf_fname, 'rt') as fobj:
            contents = fobj.read()
        contents = contents.replace(
            "'matplotlib.sphinxext.plot_directive'",
            '"plot_directive"')
        contents += """
< # Use custom plot_directive
< sys.path.insert(0, abspath(pjoin('.')))
< import plot_directive
< mathcode_plot_directive = plot_directive
"""
        with open(conf_fname, 'wt') as fobj:
            fobj.write(contents)

    def test_plot_and_math(self):
        doctree = self.get_doctree('plot_and_math')
        assert len(doctree.document) == 1
        tree_str = self.doctree2str(doctree)
        # Sphinx by 1.3 adds "highlight_args={}", Sphinx at 1.1.3 does not
        assert re.compile(EXP_PLOT_AND_MATH).search(tree_str)
