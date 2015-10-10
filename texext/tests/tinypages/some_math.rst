#########
Some math
#########

Here $a = 1$, except `$b = 2$`.

Here $a = 1$, except ``$b = 2$``.

::

    Here $a = 1$


.. mathcode::

    import sympy
    a, b, foo = sympy.symbols('a, b, q')
    a * 10 + 2 * b + foo

More text

.. mathcode::
    :label: some-label

    a * 5 + 3 * b

Yet more text

.. mathcode::
    :newcontext:

    import sympy
    foo, b = sympy.symbols('w, x')
    foo * 5 + 3 * b
