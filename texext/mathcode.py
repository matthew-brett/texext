""" Sphinx extension to execute sympy code generating LaTeX

Uses code copied from sphinx/ext/mathbase.py.  That file has license:

    :copyright: Copyright 2007-2015 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
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
