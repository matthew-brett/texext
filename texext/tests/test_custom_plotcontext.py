""" Tests for plotcontext build using sphinx extensions

Test ability to combine plot_context with mathcode
"""

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
