#########
Some math
#########

Here $a = 1$, except `$b = 2$`.

Here $a = 1$, except ``$b = 2$``.

::

    Here $a = 1$


.. mathcode::

    import sympy
    a, b = sympy.symbols('a, b')
    a * 10 + 2 * b

More text

.. mathcode::
    :label: some-label

    a * 5 + 3 * b
