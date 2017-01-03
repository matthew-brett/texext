""" Sphinx extension to execute sympy code generating LaTeX

Uses code copied from sphinx/ext/mathbase.py.  That file has license:

    :copyright: Copyright 2007-2015 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.

See README file for more information.

The MathCodeDirective accepts a Sympy expression as input.  It returns the
result of that expression as LaTeX included in a ``..math`` block.

This allows you do generate LaTeX dynamically.  For example:

    .. mathcode::

        import sympy
        a, b = sympy.symbols('a, b')
        a * 10 + 2 * b

The directive takes the result of ``sympy.latex(a * 10 + 2 * b)`` and puts it
inside a math directive in the ReST output.

By default the mathcode directives keep context from previous mathcode
directives, so you can use defined variables and functions.

You might want to clear the context for the first mathcode directive in a page,
by adding the ``:newcontext:`` option:

    .. mathcode::
        :newcontext:

        import sympy  # sympy no longer defined
        c, d = sympy.symbols('a, b')
        return c + d

If the last expression in the mathcode block is not an expression, the context
gets updated, but the extension generates no math directive to the output.
This allows you to have blocks that fill in calculations without rendering to
the page.  For example, this generates no output::

    .. mathcode::

        expr = a * 4

If you would like mathcode to share a namespace with the matplotlib ``plot``
directive, set the following in your ``conf.py``::

    # Config of mathcode directive
    mathcode_use_plot_ns = True

If you want to use the plot_directive context from within mathcode directives,
you need to list the plot_directive above the mathcode directive in your sphinx
extension list.  All the plot directives code will get run before all the
mathcode directive code.

Conversely, if you want to use the mathcode directive context from the
plot_directive, list mathcode first in your sphinx extension list.

Remember that, by default, the matplotlib ``plot`` directive will clear the
namespace context for each directive, so you may want to use the ``:context:``
option to the plot directive, most of the time.

If you want to work with a customized version of the plot_directive, you need
to supply the name of the plot context dictionary for the plot directive, as a
string.  For example, if you have a custom plot directive module importable as
``import my_path.plot_directive``, with the plot context in
``my_path.plot_directive.plot_context``, then your ``conf.py`` should have
lines like these::

    # Config of mathcode directive
    mathcode_plot_context = "my_path.plot_directive.plot_context"

The plot context is a string rather than the attribute itself in order to let
sphinx pickle the configuration between runs.  This allows sphinx to avoid
building pages that have not changed between calls to ``sphinx-build``.
"""

import warnings

from ast import parse, Expr, Expression

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info
from sphinx.ext.mathbase import displaymath


def eval_code(code_str, context):
    # Avoid depending on six unless running mathcode directive
    from six import exec_
    mod = parse(code_str, '<string>', 'exec')
    last_line = mod.body.pop() if isinstance(mod.body[-1], Expr) else None
    to_exec = compile(mod, '<string>', 'exec')
    exec_(to_exec, None, context)
    if last_line is None:
        return None
    to_eval = compile(Expression(last_line.value), '<string>', 'eval')
    return eval(to_eval, None, context)


class MathCodeDirective(Directive):
    """ Generate math environment from Sympy math expressions
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'label': directives.unchanged,
        'name': directives.unchanged,
        'nowrap': directives.flag,
        'newcontext': directives.flag,
    }

    def get_plot_directive(self):
        plot_directive = setup.config.mathcode_plot_directive
        if plot_directive is None:
            return None
        warnings.warn("mathcode_plot_directive deprecated; "
                      "please use mathcode_plot_context instead",
                      FutureWarning)
        return plot_directive

    def get_plot_context(self):
        # First try mathcode_plot_context dictionary
        plot_context = setup.config.mathcode_plot_context
        if plot_context is not None:
            # Plot context is a string naming a module attribute
            parts = plot_context.split('.')
            mod_name, el_name = '.'.join(parts[:-1]), parts[-1]
            mod = __import__(mod_name, globals(), locals(), el_name)
            return getattr(mod, el_name)
        # Next try getting dictionary from deprecated mathcode_plot_directive
        plot_directive = self.get_plot_directive()
        if plot_directive is not None:
            return plot_directive.plot_context
        # Default to matplotlib plot_context dictionary
        from matplotlib.sphinxext.plot_directive import plot_context
        return plot_context

    def get_context(self, newcontext=False):
        if setup.config.mathcode_use_plot_ns:
            plot_context = self.get_plot_context()
        else:
            plot_context = setup.code_context
        if newcontext:
            plot_context.clear()
        return plot_context

    def run(self):
        # Avoid depending on sympy unless running mathcode directive
        from sympy import latex
        want_new = True if 'newcontext' in self.options else False
        context = self.get_context(want_new)
        val = eval_code('\n'.join(self.content), context)
        if val is None:
            return []
        node = displaymath()
        node['latex'] = latex(val)
        node['label'] = self.options.get('name', None)
        node['number'] = None
        if node['label'] is None:
            node['label'] = self.options.get('label', None)
        node['nowrap'] = 'nowrap' in self.options
        node['docname'] = self.state.document.settings.env.docname
        ret = [node]
        set_source_info(self, node)
        if hasattr(self, 'src'):
            node.source = self.src
        if node['label']:
            tnode = nodes.target('', '', ids=['equation-' + node['label']])
            self.state.document.note_explicit_target(tnode)
            ret.insert(0, tnode)
        return ret


def setup(app):
    # Global variables
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir
    # Workspace for code run in Mathcode blocks
    setup.code_context = dict()
    app.add_directive('mathcode', MathCodeDirective)
    app.add_config_value('mathcode_use_plot_ns', False, 'env')
    app.add_config_value('mathcode_plot_context', None, 'env')
    # mathcode_plot_directive deprecated; prefer mathcode_plot_context
    app.add_config_value('mathcode_plot_directive', None, 'env')
