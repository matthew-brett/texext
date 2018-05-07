""" Tests for plotcontext build using sphinx extensions

Test ability to combine plot_context with mathcode
"""

import re
from os.path import join as pjoin

from .test_custom_plotdirective import TestCustomPlotDirective


class TestPlotContext(TestCustomPlotDirective):
    # Test build and output of custom_plotcontext project

    @classmethod
    def modify_pages(cls):
        conf_fname = pjoin(cls.page_source, 'conf.py')
        with open(conf_fname, 'rt') as fobj:
            contents = fobj.read()
        contents = contents.replace(
            "'matplotlib.sphinxext.plot_directive'",
            '"plot_directive"')
        contents += """
# Use mpl plot_context
mathcode_plot_context = 'matplotlib.sphinxext.plot_directive.plot_context'
"""

    def test_plot_and_math(self):
        doctree = self.get_doctree('plot_and_math')
        assert len(doctree.document) == 1
        tree_str = self.doctree2str(doctree)
        # Sphinx by 1.3 adds "highlight_args={}", Sphinx at 1.1.3 does not
        assert re.compile(
            '<title>Plot directive with mathcode</title>\n'
            '<paragraph>Some text</paragraph>\n'
            r'<literal_block (highlight_args="{}"\s+)?language="python" '
            'linenos="False" xml:space="preserve">a = 101</literal_block>\n'
            '<only expr="html"/>\n'
            '<only expr="latex"/>\n'
            '<only expr="texinfo"/>\n'
            '<paragraph>More text</paragraph>\n'
            '<displaymath docname="plot_and_math" label="None" '
            'latex="101" nowrap="False"( number="None")?/>'
        ).search(tree_str)
