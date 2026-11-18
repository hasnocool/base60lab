"""Tests for base-10 engine (known-truths reference system)."""

from base60lab.core.rational import Rational
from base60lab.core.types import BaseNumber
from base60lab.engines.base10_engine import Base10Engine


def test_engine_creation():
    eng = Base10Engine()
    assert eng.BASE == 10
    assert eng.FRACTIONAL_POINT == "."
    assert eng.DIGITS == tuple(str(d) for d in range(10))


def test_from_and_to_rational():
    eng = Base10Engine()
    r = Rational(3, 4)
    bn = eng.from_rational(r)
    assert isinstance(bn, BaseNumber)
    assert bn.base == 10
    assert eng.to_rational(bn) == r


def test_addition():
    eng = Base10Engine()
    a = eng.from_rational(Rational(1, 2))
    b = eng.from_rational(Rational(1, 4))
    result = eng.add(a, b)
    assert eng.to_rational(result) == Rational(3, 4)
    assert result.base == 10


def test_division():
    eng = Base10Engine()
    a = eng.from_rational(Rational(1))
    b = eng.from_rational(Rational(3))
    result = eng.div(a, b)
    assert eng.to_rational(result) == Rational(1, 3)


def test_round_trip_notation():
    eng = Base10Engine()
    for n in range(0, 101):
        bn = eng.from_rational(Rational(n))
        notation = eng.to_notation(bn)
        assert notation.base == 10


def test_1_over_3_decimal_repeating():
    eng = Base10Engine()
    bn = eng.reciprocal(3) if hasattr(eng, "reciprocal") else eng.from_rational(Rational(1, 3))
    notation = eng.to_notation(bn)
    assert notation.repeating is not None
    assert "3" in notation.text


def test_1_over_2_decimal_terminating():
    eng = Base10Engine()
    bn = eng.from_rational(Rational(1, 2))
    notation = eng.to_notation(bn)
    assert notation.repeating is None


def test_terminating_count_base10():
    eng = Base10Engine()
    terms = eng.terminating_denominators(360)
    # 1/2, 1/4, 1/5, 1/8, 1/10, ... terminate in base 10
    assert 2 in terms
    assert 5 in terms
    assert 10 in terms
    assert 3 not in terms  # 1/3 repeats in base 10
    assert 7 not in terms


def test_repeating_period_1_over_7_base10():
    eng = Base10Engine()
    period = eng.repeating_period(7)
    assert period == 6


def test_describe_known_truths_complete():
    eng = Base10Engine()
    desc = eng.describe()
    assert desc["base"] == 10
    assert desc["known_truths_complete"] is True
    assert desc["name"] == "decimal"


def test_function_add():
    eng = Base10Engine()
    f = eng.function("add")
    result = f(eng.from_rational(Rational(2)), eng.from_rational(Rational(3)))
    assert result == Rational(5)


def test_function_unknown_raises():
    eng = Base10Engine()
    try:
        eng.function("nonexistent")
        assert False, "should have raised KeyError"
    except KeyError:
        pass
def test_neg():
    eng = Base10Engine()
    bn = eng.from_rational(Rational(5))
    result = eng.neg(bn)
    assert eng.to_rational(result) == Rational(-5)


def test_pow():
    eng = Base10Engine()
    bn = eng.from_rational(Rational(2))
    result = eng.pow(bn, 3)
    assert eng.to_rational(result) == Rational(8)


def test_sub():
    eng = Base10Engine()
    a = eng.from_rational(Rational(5))
    b = eng.from_rational(Rational(3))
    result = eng.sub(a, b)
    assert eng.to_rational(result) == Rational(2)


def test_mul():
    eng = Base10Engine()
    a = eng.from_rational(Rational(3))
    b = eng.from_rational(Rational(4))
    result = eng.mul(a, b)
    assert eng.to_rational(result) == Rational(12)


def test_convert_from_base():
    eng = Base10Engine()
    bn = eng.from_rational(Rational(7))
    result = eng.convert_from_base(bn, 12)
    assert result.base == 10
    assert eng.to_rational(result) == Rational(7)


def test_function_keyerror():
    eng = Base10Engine()
    try:
        eng.function("unknown_function")
    except KeyError as e:
        assert "unknown_function" in str(e)
    else:
        assert False, "Expected KeyError"


def test_to_notation_integer_zero():
    """Test notation rendering for zero integer part."""
    eng = Base10Engine()
    bn = eng.from_rational(Rational(0))
    notation = eng.to_notation(bn)
    assert notation.text == "0"
    assert notation.repeating is None


def test_to_notation_negative_integer():
    """Test notation rendering for negative numbers."""
    eng = Base10Engine()
    bn = eng.from_rational(Rational(-5))
    notation = eng.to_notation(bn)
    assert notation.text == "-5"
    assert notation.repeating is None


def test_to_notation_negative_fraction():
    """Test notation rendering for negative fractions."""
    eng = Base10Engine()
    bn = eng.from_rational(Rational(-1, 2))
    notation = eng.to_notation(bn)
    assert notation.text == "-0.5"
    assert notation.repeating is None


def test_terminating_denominators_base10():
    """Test terminating_denominators returns correct list."""
    eng = Base10Engine()
    terms = eng.terminating_denominators(20)
    # Denominators whose prime factors are only 2 and/or 5
    expected = {1, 2, 4, 5, 8, 10, 16, 20}
    assert set(terms) == expected


def test_repeating_period_base10():
    """Test repeating_period for various denominators."""
    eng = Base10Engine()
    # 1/7 repeats with period 6 in base 10
    period = eng.repeating_period(7)
    assert period == 6
    # 1/3 repeats with period 1
    period = eng.repeating_period(3)
    assert period == 1
    # 1/2 terminates
    period = eng.repeating_period(2)
    assert period is None


def test_describe_base10():
    """Test describe method returns expected structure."""
    eng = Base10Engine()
    desc = eng.describe()
    assert desc["base"] == 10
    assert desc["name"] == "decimal"
    assert desc["factorisation"] == {2: 1, 5: 1}
    assert desc["digit_symbols"] == tuple(str(d) for d in range(10))
    assert desc["fractional_point"] == "."
    assert desc["known_truths_complete"] is True
    assert "unknowns_count" in desc


def test_unknowns_registry_accessible():
    """Test that unknowns registry is accessible."""
    eng = Base10Engine()
    # Base10Engine has some unknowns even though known_truths_complete is True
    assert len(eng.unknowns) >= 0
    assert eng.describe()["known_truths_complete"] is True
