""" Testing math_dollar module
"""

from ..math_dollar import dollars_to_math

from nose.tools import (assert_true, assert_false, assert_raises,
                        assert_equal, assert_not_equal)


def d2m(source):
    # Shim to return source, so testing a bit more convenient
    dollars_to_math(source)
    return source


def test_dollars_to_math():
    # Simple inline math
    assert_equal(d2m(['Here be $a = b$ math']), ['Here be :math:`a = b` math'])
    assert_equal(d2m(['Here be $a =\nb$ math']), ['Here be :math:`a =\nb` math'])
    # Dollars inside backticks don't get replaced
    assert_equal(d2m(['Here be `$a = b$` math']), ['Here be `$a = b$` math'])
    assert_equal(d2m(['Here be ``$a = b$`` math']), ['Here be ``$a = b$`` math'])
    assert_equal(d2m(['Here `$a = b$` and `$c$`']), ['Here `$a = b$` and `$c$`'])
    # In general this is because dollars before or after backticks stay same
    assert_equal(d2m(['Here be `$a = b` math']), ['Here be `$a = b` math'])
    assert_equal(d2m(['Here be `a = b$` math']), ['Here be `a = b$` math'])
    # And in general that's because everything between backticks stays the same
    assert_equal(d2m(['Such as ``$1 $2 $3`` etc']), ['Such as ``$1 $2 $3`` etc'])
    assert_equal(d2m(['Such as `$1 $2 $3` etc']), ['Such as `$1 $2 $3` etc'])
    # Can mix with and without backticks
    assert_equal(d2m(['Here `$a$` and $c$']), ['Here `$a$` and :math:`c`'])
    # Dollars inside curlies don't get replaced
    assert_equal(d2m([r'Now $f(n) = 0 \text{ if $n$ is prime}$ then']),
                 [r'Now :math:`f(n) = 0 \text{ if $n$ is prime}` then'])
    # Don't mathize dollars on lines with indents
    assert_equal(d2m([' $env']), [' $env'])
    assert_equal(d2m(['::\n  $env\n  $var']), ['::\n  $env\n  $var'])
    assert_equal(d2m(['::\n  $env\n\nHere $b$ there']),
                 ['::\n  $env\n\nHere :math:`b` there'])
    assert_equal(d2m(['and some `$real dollars`.  More ``$real dollars``.']),
                 ['and some `$real dollars`.  More ``$real dollars``.'])
    assert_equal(d2m(
        ['\n\nSome $math dollars$.  More $math dollars$.\n']),
        ['\n\nSome :math:`math dollars`.  More :math:`math dollars`.\n']),
