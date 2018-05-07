""" Testing math_dollar module
"""

from ..math_dollar import d2m_source, rst_dollars_to_math


def source_shim(in_str):
    # Shim to return source, so testing a bit more convenient
    source = [in_str]
    d2m_source(source)
    return "\n".join(source)


def test_dollars_to_math():
    # Simple inline math
    d2m = rst_dollars_to_math
    # For a few simple inputs, test list and string versions
    for f in (source_shim, d2m):
        assert f('Here be $a = b$ math') == 'Here be :math:`a = b` math'
        assert f('Here be $a =\nb$ math') == 'Here be :math:`a =\nb` math'
    # Dollars inside backticks don't get replaced
    assert d2m('Here be `$a = b$` math') == 'Here be `$a = b$` math'
    assert d2m('Here be ``$a = b$`` math') == 'Here be ``$a = b$`` math'
    assert d2m('Here `$a = b$` and `$c$`') == 'Here `$a = b$` and `$c$`'
    # In general this is because dollars before or after backticks stay same
    assert d2m('Here be `$a = b` math') == 'Here be `$a = b` math'
    assert d2m('Here be `a = b$` math') == 'Here be `a = b$` math'
    # And in general that's because everything between backticks stays the same
    assert d2m('Such as ``$1 $2 $3`` etc') == 'Such as ``$1 $2 $3`` etc'
    assert d2m('Such as `$1 $2 $3` etc') == 'Such as `$1 $2 $3` etc'
    # Can mix with and without backticks
    assert d2m('Here `$a$` and $c$') == 'Here `$a$` and :math:`c`'
    # Dollars inside curlies don't get replaced
    assert (d2m(r'Now $f(n) = 0 \text{ if $n$ is prime}$ then') ==
                 r'Now :math:`f(n) = 0 \text{ if $n$ is prime}` then')
    # We do now mathize dollars on lines with indents
    assert d2m(' $env$') == ' :math:`env`'
    assert d2m('::\n  $env\n  $var') == '::\n  :math:`env\n  `var'
    assert (d2m('::\n  $env$\n\nHere $b$ there') ==
                '::\n  :math:`env`\n\nHere :math:`b` there')
    assert (d2m('and some `$real dollars`.  More ``$real dollars``.') ==
            'and some `$real dollars`.  More ``$real dollars``.')
    assert (d2m('\n\nSome $math dollars$.  More $math dollars$.\n') ==
            '\n\nSome :math:`math dollars`.  More :math:`math dollars`.\n')
    # Lots of backticks in a heading
    assert (d2m(
        '\nWord\n\nHeading\n```````\nMore ``stuff`` here') ==
        '\nWord\n\nHeading\n```````\nMore ``stuff`` here')
    mysterious_problem="""\
Some text short
```````````````

::

    a
    b
    c
    d

``$H``
"""
    assert d2m(mysterious_problem) == mysterious_problem
    # Test case where text with markers may be substituted with another marker.
    # This depends on dictionary ordering, so will only sometimes catch errors.
    assert (d2m(
        'She `is in ``her own`` new ``world``, always` leaving') ==
        'She `is in ``her own`` new ``world``, always` leaving')
    assert (d2m(
        "* A list item containing\n  $f = 6$ some mathematics.") ==
        "* A list item containing\n  :math:`f = 6` some mathematics.")
    assert (d2m(
        "* A list item containing ``a literal across\n  lines`` and also "
        "$g = 7$ some mathematics.") ==
        "* A list item containing ``a literal across\n  lines`` and also "
        ":math:`g = 7` some mathematics.")
