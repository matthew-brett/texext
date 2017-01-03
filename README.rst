######################################################
Texext - sphinx extensions for working with LaTeX math
######################################################

``texext`` contains a couple of Sphinx_ extensions for working with LaTeX math.

***********
math_dollar
***********

``math_dollar`` replaces math expressions between dollars in ReST_ with
equivalent inline math.

For example::

    Here is some math: $a = 2$

will be replaced by::

    Here is some math: :math:`a = 2`

The extension makes some effort not to replace dollars that aren't meant as
math, but please check your output carefully, and submit an issue on the
`texext issue tracker`_ if we have messed up.

To enable math_dollar, make sure that the ``texext`` package is on your
Python path, and add ``textext.math_dollar`` to your list of extensions in the
Sphinx ``conf.py``.  If you want math_dollar to process docstrings, you
should add ``sphinx.ext.autodoc`` higher up your extensions list than
``math_dollar``.

******************
mathcode directive
******************

Users of `sympy <http://www.sympy.org>`_ may want to generate LaTeX
expressions dynamically in Sympy, and then render them in LaTeX in the built
pages.  You can do this with the ``mathcode`` directive::

    .. mathcode::

        import sympy
        a, b = sympy.symbols('a, b')
        a * 10 + 2 * b

The directive runs ``sympy.latex()`` on the return result of the final
expression, and embeds it in a ``.. math::`` directive, resulting in
equivalent output to sphinx of::

    .. math::

        10 a + 2 b

Context (namespace) is preserved by default, so you can use context in
subsequent directives, e.g.::

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

To reset the context (namespace), use the ``newcontext`` option::

    .. mathcode::
        :newcontext:

        import sympy  # again

If you would like mathcode to share a namespace with the `matplotlib
plot_directive`_, set the following in your ``conf.py``::

    # Config of mathcode directive
    mathcode_use_plot_ns = True

.. note::

    If you want to use the plot_directive context from within mathcode
    directives, you need to list the plot_directive above the mathcode
    directive in your sphinx extension list.  All the plot directives code
    will get run before all the mathcode directive code.

    Conversely, if you want to use the mathcode directive context from the
    plot_directive, list mathcode first in your sphinx extension list.

Remember that, by default, the ``plot_directive`` will clear the namespace
context for each directive, so you may want to use the ``:context:`` option to
the plot directive, most of the time.

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

To enable the mathcode directive, make sure that the ``texext`` package is on
your Python path, and add ``textext.mathcode`` to your list of extensions in
the Sphinx ``conf.py``.

****
Code
****

See https://github.com/matthew-brett/texext

Released under the BSD two-clause license - see the file ``LICENSE`` in the
source distribution.

`travis-ci <https://travis-ci.org/matthew-brett/texext>`_ kindly tests the
code automatically under Python versions 2.7, and 3.3 through 3.6.

The latest released version is at https://pypi.python.org/pypi/texext

*******
Support
*******

Please put up issues on the `texext issue tracker`_.

.. _sphinx: http://sphinx-doc.org
.. _rest: http://docutils.sourceforge.net/rst.html
.. _texext issue tracker: https://github.com/matthew-brett/texext/issues
.. _matplotlib plot_directive: http://matplotlib.org/sampledoc/extensions.html
