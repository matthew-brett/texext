#########
Some math
#########

Here $a = 1$, except `$b = 2$`.

Here $c = 3$, except ``$d = 4$``.

::

    Here $e = 5$

* A list item containing
  $f = 6$ some mathematics.
* A list item containing ``a literal across
  lines`` and also $g = 7$ some mathematics.

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

Math with $\beta$ a backslash.

A protected white\ space with $dollars$.

Some \* asterisks \*.  $dollars$. A line \
break.  Protected \\ backslash.  Protected \n in $a$ line.
