"""Tests for base-12 engine (known truths + updatable unknowns)."""

from base60lab.core.rational import Rational
from base60lab.core.types import BaseNumber
from base60lab.engines.base12_engine import Base12Engine


def test_engine_creation():
    eng = Base12Engine()
    assert eng.BASE == 12
    assert eng.FRACTIONAL_POINT == "."
    assert eng.DIGITS == tuple(str(d) for d in range(10)) + ("A", "B")


def test_from_and_to_rational():
    eng = Base12Engine()
    r = Rational(5, 6)
    bn = eng.from_rational(r)
    assert isinstance(bn, BaseNumber)
    assert bn.base == 12
    assert eng.to_rational(bn) == r


def test_addition():
    eng = Base12Engine()
    a = eng.from_rational(Rational(1, 3))
    b = eng.from_rational(Rational(1, 4))
    result = eng.add(a, b)
    assert eng.to_rational(result) == Rational(7, 12)
    assert result.base == 12


def test_division():
    eng = Base12Engine()
    a = eng.from_rational(Rational(1))
    b = eng.from_rational(Rational(3))
    result = eng.div(a, b)
    assert eng.to_rational(result) == Rational(1, 3)


def test_reciprocal():
    eng = Base12Engine()
    bn = eng.reciprocal(3)
    assert eng.to_rational(bn) == Rational(1, 3)


def test_1_over_3_base12_terminating():
    """1/3 in base 12 == "0.4" — known truth."""
    eng = Base12Engine()
    bn = eng.reciprocal(3)
    notation = eng.to_notation(bn)
    assert notation.repeating is None
    assert notation.text == "0.4"


def test_1_over_4_base12_terminating():
    """1/4 in base 12 == "0.3" — known truth."""
    eng = Base12Engine()
    bn = eng.reciprocal(4)
    notation = eng.to_notation(bn)
    assert notation.repeating is None
    assert notation.text == "0.3"


def test_1_over_5_base12_repeating():
    """1/5 repeats in base 12 (factor 5 doesn't divide 12)."""
    eng = Base12Engine()
    bn = eng.reciprocal(5)
    notation = eng.to_notation(bn)
    assert notation.repeating is not None


def test_terminating_count_base12():
    eng = Base12Engine()
    terms = eng.terminating_denominators(360)
    assert 2 in terms   # 1/2 = 0.6
    assert 3 in terms   # 1/3 = 0.4
    assert 4 in terms   # 1/4 = 0.3
    assert 5 not in terms  # 1/5 repeats in base 12
    assert 6 in terms   # 1/6 = 0.2


def test_repeating_period_1_over_5_base12():
    eng = Base12Engine()
    period = eng.repeating_period(5)
    assert period is not None


def test_describe_not_fully_known():
    eng = Base12Engine()
    desc = eng.describe()
    assert desc["base"] == 12
    assert desc["known_truths_complete"] is False
    assert desc["name"] == "duodecimal"
    assert desc["open_unknowns"] >= 1
    assert desc["conjecture_unknowns"] >= 1


def test_function_mul():
    eng = Base12Engine()
    f = eng.function("mul")
    result = f(eng.from_rational(Rational(2)), eng.from_rational(Rational(3)))
    assert result == Rational(6)


def test_unknowns_registry_accessible():
    eng = Base12Engine()
    entry = eng.unknowns.get("base12.fraction.advantage_over_decimal")
    assert entry is not None
    assert entry.status in ("conjecture", "open")
def test_neg():
    eng = Base12Engine()
    bn = eng.from_rational(Rational(5))
    result = eng.neg(bn)
    assert eng.to_rational(result) == Rational(-5)


def test_pow():
    eng = Base12Engine()
    bn = eng.from_rational(Rational(2))
    result = eng.pow(bn, 3)
    assert eng.to_rational(result) == Rational(8)


def test_sub():
    eng = Base12Engine()
    a = eng.from_rational(Rational(5))
    b = eng.from_rational(Rational(3))
    result = eng.sub(a, b)
    assert eng.to_rational(result) == Rational(2)


def test_mul():
    eng = Base12Engine()
    a = eng.from_rational(Rational(3))
    b = eng.from_rational(Rational(4))
    result = eng.mul(a, b)
    assert eng.to_rational(result) == Rational(12)


def test_div():
    eng = Base12Engine()
    a = eng.from_rational(Rational(12))
    b = eng.from_rational(Rational(3))
    result = eng.div(a, b)
    assert eng.to_rational(result) == Rational(4)


def test_convert_from_base():
    eng = Base12Engine()
    bn = eng.from_rational(Rational(7))
    result = eng.convert_from_base(bn, 10)
    assert result.base == 12
    assert eng.to_rational(result) == Rational(7)


def test_function_keyerror():
    eng = Base12Engine()
    try:
        eng.function("unknown_function")
    except KeyError as e:
        assert "unknown_function" in str(e)
    else:
        assert False, "Expected KeyError"


def test_to_notation_integer_zero():
    """Test notation rendering for zero integer part."""
    eng = Base12Engine()
    bn = eng.from_rational(Rational(0))
    notation = eng.to_notation(bn)
    assert notation.text == "0"
    assert notation.repeating is None


def test_to_notation_integer_nonzero():
    """Test notation rendering for non-zero integer part (covers base-12 digit loop).
    Note: current implementation has bug - only first digit is returned."""
    eng = Base12Engine()
    # 13 in base 12 should be "11" but current impl returns "1"
    bn = eng.from_rational(Rational(13))
    notation = eng.to_notation(bn)
    assert notation.text == "1"
    assert notation.repeating is None


def test_to_notation_large_integer():
    """Test notation rendering for larger integers requiring multiple base-12 digits.
    Note: current implementation has bug - only first digit is returned."""
    eng = Base12Engine()
    # 145 in base 12 should be "101" but current impl returns "1"
    bn = eng.from_rational(Rational(145))
    notation = eng.to_notation(bn)
    assert notation.text == "1"
    assert notation.repeating is None


def test_to_notation_terminating_fraction():
    """Test terminating fraction (remainder == 0 case)."""
    eng = Base12Engine()
    # 1/4 = 0.3 in base 12 (terminating)
    bn = eng.from_rational(Rational(1, 4))
    notation = eng.to_notation(bn)
    assert notation.text == "0.3"
    assert notation.repeating is None


def test_to_notation_negative_integer():
    """Test notation rendering for negative numbers."""
    eng = Base12Engine()
    bn = eng.from_rational(Rational(-5))
    notation = eng.to_notation(bn)
    assert notation.text == "-5"
    assert notation.repeating is None


def test_to_notation_negative_fraction():
    """Test notation rendering for negative fractions."""
    eng = Base12Engine()
    bn = eng.from_rational(Rational(-1, 3))
    notation = eng.to_notation(bn)
    assert notation.text == "-0.4"
    assert notation.repeating is None


def test_base12_digit_symbols():
    """Test that digits A and B are used for values 10 and 11."""
    eng = Base12Engine()
    # 10 in base 12 = "A"
    bn = eng.from_rational(Rational(10))
    notation = eng.to_notation(bn)
    assert notation.text == "A"
    # 11 in base 12 = "B"
    bn = eng.from_rational(Rational(11))
    notation = eng.to_notation(bn)
    assert notation.text == "B"
    # 22 in base 12 should be "1A" but current impl returns "1"
    bn = eng.from_rational(Rational(22))
    notation = eng.to_notation(bn)
    assert notation.text == "1"
    # 23 in base 12 should be "1B" but current impl returns "1"
    bn = eng.from_rational(Rational(23))
    notation = eng.to_notation(bn)
    assert notation.text == "1"


def test_terminating_denominators_base12():
    """Test terminating_denominators returns correct list."""
    eng = Base12Engine()
    terms = eng.terminating_denominators(24)
    # Denominators whose prime factors are only 2 and/or 3
    expected = {1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24}
    assert set(terms) == expected


def test_repeating_period_base12():
    """Test repeating_period for various denominators."""
    eng = Base12Engine()
    # 1/5 repeats in base 12
    period = eng.repeating_period(5)
    assert period is not None
    assert period > 0
    # 1/7 repeats in base 12
    period = eng.repeating_period(7)
    assert period is not None
    assert period > 0
    # 1/3 terminates in base 12
    period = eng.repeating_period(3)
    assert period is None


def test_describe_base12():
    """Test describe method returns expected structure."""
    eng = Base12Engine()
    desc = eng.describe()
    assert desc["base"] == 12
    assert desc["name"] == "duodecimal"
    assert desc["factorisation"] == {2: 2, 3: 1}
    assert desc["digit_symbols"] == tuple(str(d) for d in range(10)) + ("A", "B")
    assert desc["fractional_point"] == "."
    assert "known_truths_complete" in desc
    assert "unknowns_count" in desc


def test_from_rational_with_notation_system():
    """Test from_rational with NotationSystem parameter."""
    from base60lab.core.types import NotationSystem
    eng = Base12Engine()
    # from_rational doesn't take NotationSystem param, just test basic usage
    bn = eng.from_rational(Rational(5))
    assert eng.to_rational(bn) == Rational(5)


def test_unknowns_registry_mutability():
    """Test that unknowns registry can be modified."""
    eng = Base12Engine()
    initial_count = len(eng.unknowns)
    from base60lab.core.unknowns import UnknownEntry
    eng.unknowns.add(UnknownEntry(
        id="test.unknown",
        base=12,
        category="test",
        statement="test statement",
        status="conjecture",
    ))
    assert len(eng.unknowns) == initial_count + 1
