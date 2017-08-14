""" Test building of docstrings into pages with autodoc
"""

import re

from sphinxtesters import SourcesBuilder

from nose.tools import assert_regexp_matches


class TestDocstrings(SourcesBuilder):

    rst_sources = dict(a_page="""\
Here is the module docstring:

.. automodule:: texext.tests.for_docstrings

Here is the ``func`` docstring:

.. autofunction:: texext.tests.for_docstrings.func
""")

    conf_source = """\
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'texext.math_dollar']
"""

    # sphinx 1.1.3 has <tt> for <code>
    expected_re = re.compile(
r'<p>Here is the module docstring:</p>\n'
r'<span class="target" id="module-texext.tests.for_docstrings"></span>'
r'<p>A module to test docstring parsing with math such as '
r'<span class="math">\\\(\\gamma = \\cos\(\\alpha\)\\\)</span></p>\n'
r'<p>Need to test other markup - so: '
r'<a class="reference external" href="https://github\.com">a link</a>\.</p>\n'
r'<p>Here is the <(code|tt) class="docutils literal">'
r'<span class="pre">func</span></(code|tt)> docstring:</p>\n'
r'<dl class="function">\n'
r'<dt id="texext.tests.for_docstrings\.func">\n'
r'<(code|tt) class="descclassname">texext.tests.for_docstrings\.</(code|tt)>'
r'<(code|tt) class="descname">func</(code|tt)>'
'('
r'<span class="sig-paren">\(</span><span class="sig-paren">\)</span>'
'|'
r'<big>\(</big><big>\)</big>'  # sphinx 1.1.3
')'
r'<a class="headerlink" href="#texext.tests.for_docstrings\.func" '
r'title="Permalink to this definition">.+</a></dt>\n'
r'<dd><p>A docstring with math in first line '
r'<span class="math">\\\(z = \\beta\\\)</span></p>\n'
r'<p>With some more <span class="math">\\\(a = 1\\\)</span> math\. '
r'Math across lines - <span class="math">\\\(b\n'
r'= 2\\\)</span>\.</p>\n'
r'<p>Further, there is a <a class="reference external" '
r'href="https://python\.org">link</a> and a substituted\.</p>\n'
'</dd></dl>')

    def test_docstrings(self):
        html = self.get_built_file('a_page.html')
        assert_regexp_matches(html, self.expected_re)
