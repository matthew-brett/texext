#####################################################
Texext - sphinx extension for working with LaTeX math
#####################################################

A couple of sphinx extensions for working with LaTeX math.

***************
``math_dollar``
***************

By Ondřej Čertík, refactored.

Replaces math expressions between dollars in ReST with equivalent inline math.

For example::

    Here is some math: $a = 2$

will be replaced by::

    Here is some math: :math:`a = 2`

The extension makes some effort not to replace dollars that aren't meant as
math, but please check your output carefull, and submit an issue if we mess
up.

******************
mathcode directive
******************

Users of `sympy <http://www.sympy.org>`_ may want to generate LaTeX
expressions dynamically in sympy, and then render them in LaTeX in the built
pages.  You can do this with the ``mathcode`` directive::

    .. mathcode::

        import sympy
        a, b = sympy.symbols('a, b')
        a * 10 + 2 * b

The directive runs ``sympy.latex()`` on the return result of the final
expression, and embeds it in a ``.. math::`` directive, resulting in
equivalent output to sphinx of:

    .. math::

        10 a + 2 b

Context is preserved by default, so you can use context in subsequent
directives, e.g.::

    .. mathcode::

        a * 5 + 3 * b

If the last expression in the mathcode block is not an expression, the context
gets updated, but the extension generates no math directive to the output.
This allows you to have blocks that fill in calculations without rendering to
the page.  For example, this generates no output::

    .. mathcode::

        expr = a * 4

You can use the generated context in a later directive::

    .. mathcode::

        expr

To reset the context (namespaces), use the ``newcontext`` option::

    .. mathcode::
        :newcontext:

        import sympy  # again

If you would like mathcode to share a namespace with the matplotlib
``plot_directive``, set::

    # Config of mathcode directive
    mathcode_use_plot_ns = True

Remember that, by default, the ``plot_directive`` will clear the namespace
context for each directive, so you may want to use the ``:context:`` option to
the plot directive, most of the time.
