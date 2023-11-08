""" Test building of docstrings into pages with autodoc
"""

import re

from sphinxtesters import SourcesBuilder

# Utilities for debugging
# py.test texext/tests/test_docstrings.py --pdb
# write_file(html)
# IPython: run texext/tests/test_docstrings.py
# check_re('some_regexp_pattern')

def write_file(contents, fname='.html.txt'):
    with open(fname, 'wt') as fobj:
        fobj.write(contents)


def read_file(fname='.html.txt'):
    with open(fname, 'rt') as fobj:
        contents = fobj.read()
    return contents


def check_re(pattern, text=None):
    text = read_file() if text is None else text
    full_pattern = pattern.format(**FRAGMENTS)
    return re.search(full_pattern, text)


# Docstring build regexp
# sphinx 1.1.3 has <tt> for <code>
# sphinx 1.7b0 has "math notranslate" for "math"
FRAGMENTS = dict(
    mod_id=r'id="module-texext.tests.for_docstrings"',
    code=r'(code|tt|span)',
    cclass=r'"(docutils literal( notranslate)?)"',
    math=r'"math( notranslate)?( nohighlight)?"',
)

DOCSTRING_RE = re.compile(
r'<p>Here is the module docstring:</p>\n'
r'(<span class="target" {mod_id}></span><p>|<p {mod_id}>)'  # | for sphinx 7.2
r'A module to test docstring parsing with math such as '
r'<span class={math}'
r'>\\\(\\gamma = \\cos\(\\alpha\)\\\)</span></p>\n'
r'<p>Need to test other markup - so: '
r'<a class="reference external" href="https://github\.com">a link</a>\.</p>\n'
r'<p>Here is the <{code} class={cclass}>'
r'<span class="pre">func</span></{code}> docstring:</p>\n'
r'<dl class="(py )?function">\n'
r'<dt( class=".*")? id="texext.tests.for_docstrings\.func">\n'
r'<{code} class="(sig-prename )?descclassname">'
r'(<span class="pre">)?texext.tests.for_docstrings\.(</span>)?'
r'</{code}>'
r'<{code} class="(sig-name )?descname">(<span class="pre">)?func(</span>)?'
r'</{code}>'
'('  # beginning of regexp group
r'<span class="sig-paren">\(</span><span class="sig-paren">\)</span>'
'|'
r'<big>\(</big><big>\)</big>'  # sphinx 1.1.3
')'  # end of regexp group
r'<a class="headerlink" href="#texext.tests.for_docstrings\.func" '
r'title="(Permalink|Link) to this definition">.+</a></dt>\n'
r'<dd><p>A docstring with math in first line '
r'<span class={math}>\\\(z = \\beta\\\)</span></p>\n'
r'<p>With some more <span class={math}>\\\(a = 1\\\)</span> math\. '
r'Math across lines - <span class={math}>\\\(b\n'
r'= 2\\\)</span>\.</p>\n'
r'<p>Further, there is a <a class="reference external" '
r'href="https://python\.org">link</a> and a substituted\.</p>\n'
'</dd></dl>'.format(**FRAGMENTS))


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

    def test_docstrings(self):
        html = self.get_built_file('a_page.html')
        assert DOCSTRING_RE.search(html)
