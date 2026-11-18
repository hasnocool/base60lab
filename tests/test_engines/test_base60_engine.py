"""Tests for base-60 engine (known truths + updatable unknowns)."""

from base60lab.core.rational import Rational
from base60lab.core.types import BaseNumber
from base60lab.engines.base60_engine import Base60Engine


def test_engine_creation():
    eng = Base60Engine()
    assert eng.BASE == 60
    assert eng.FRACTIONAL_POINT == ";"
    assert eng.DIGITS == tuple(str(d) for d in range(10)) + tuple(
        chr(ord("A") + i) for i in range(26)
    )


def test_from_and_to_rational():
    eng = Base60Engine()
    r = Rational(7, 12)
    bn = eng.from_rational(r)
    assert isinstance(bn, BaseNumber)
    assert bn.base == 60
    assert eng.to_rational(bn) == r


def test_addition():
    eng = Base60Engine()
    a = eng.from_rational(Rational(1, 3))
    b = eng.from_rational(Rational(1, 4))
    result = eng.add(a, b)
    assert eng.to_rational(result) == Rational(7, 12)
    assert result.base == 60


def test_division():
    eng = Base60Engine()
    a = eng.from_rational(Rational(1))
    b = eng.from_rational(Rational(3))
    result = eng.div(a, b)
    assert eng.to_rational(result) == Rational(1, 3)


def test_reciprocal():
    eng = Base60Engine()
    bn = eng.reciprocal(3)
    assert eng.to_rational(bn) == Rational(1, 3)


def test_1_over_3_base60_terminating():
    """1/3 in base 60 == "0;20" — known truth."""
    eng = Base60Engine()
    bn = eng.reciprocal(3)
    notation = eng.to_notation(bn)
    assert notation.repeating is None


def test_1_over_5_base60_terminating():
    """1/5 in base 60 == "0;12" — known truth."""
    eng = Base60Engine()
    bn = eng.reciprocal(5)
    notation = eng.to_notation(bn)
    assert notation.repeating is None


def test_1_over_7_base60_repeating():
    """1/7 repeats in base 60 (factor 7 doesn't divide 60)."""
    eng = Base60Engine()
    bn = eng.reciprocal(7)
    notation = eng.to_notation(bn)
    assert notation.repeating is not None


def test_terminating_count_base60():
    eng = Base60Engine()
    terms = eng.terminating_denominators(360)
    assert 2 in terms   # 1/2 = 0;30
    assert 3 in terms   # 1/3 = 0;20
    assert 4 in terms   # 1/4 = 0;15
    assert 5 in terms   # 1/5 = 0;12
    assert 6 in terms   # 1/6 = 0;10
    assert 7 not in terms  # 1/7 repeats in base 60
    assert 10 in terms  # 1/10 = 0;6
    assert 12 in terms  # 1/12 = 0;5


def test_repeating_period_1_over_7_base60():
    eng = Base60Engine()
    period = eng.repeating_period(7)
    assert period is not None


def test_describe_not_fully_known():
    eng = Base60Engine()
    desc = eng.describe()
    assert desc["base"] == 60
    assert desc["known_truths_complete"] is False
    assert desc["name"] == "sexagesimal"
    assert desc["open_unknowns"] >= 1
    assert desc["conjecture_unknowns"] >= 1


def test_360_equals_6_times_60():
    """Known truth: 360 = 6 × 60 = 30 × 12."""
    assert 6 * 60 == 360
    assert 30 * 12 == 360


def test_function_div():
    eng = Base60Engine()
    f = eng.function("div")
    result = f(eng.from_rational(Rational(1)), eng.from_rational(Rational(3)))
    assert result == Rational(1, 3)


def test_unknowns_registry_accessible():
    eng = Base60Engine()
    entry = eng.unknowns.get("base60.fraction.advantage_over_decimal")
    assert entry is not None
    assert entry.status in ("conjecture", "open")

    entry2 = eng.unknowns.get("base60.circle_subdivision")
    assert entry2 is not None
    assert entry2.status == "proven"
def test_neg():
    eng = Base60Engine()
    bn = eng.from_rational(Rational(5))
    result = eng.neg(bn)
    assert eng.to_rational(result) == Rational(-5)


def test_pow():
    eng = Base60Engine()
    bn = eng.from_rational(Rational(2))
    result = eng.pow(bn, 3)
    assert eng.to_rational(result) == Rational(8)


def test_sub():
    eng = Base60Engine()
    a = eng.from_rational(Rational(5))
    b = eng.from_rational(Rational(3))
    result = eng.sub(a, b)
    assert eng.to_rational(result) == Rational(2)


def test_mul():
    eng = Base60Engine()
    a = eng.from_rational(Rational(3))
    b = eng.from_rational(Rational(4))
    result = eng.mul(a, b)
    assert eng.to_rational(result) == Rational(12)


def test_convert_from_base():
    eng = Base60Engine()
    bn = eng.from_rational(Rational(7))
    result = eng.convert_from_base(bn, 10)
    assert result.base == 60
    assert eng.to_rational(result) == Rational(7)


def test_function_keyerror():
    eng = Base60Engine()
    try:
        eng.function("unknown_function")
    except KeyError as e:
        assert "unknown_function" in str(e)
    else:
        assert False, "Expected KeyError"


def test_to_notation_integer_zero():
    """Test notation rendering for zero integer part."""
    eng = Base60Engine()
    bn = eng.from_rational(Rational(0))
    notation = eng.to_notation(bn)
    assert notation.text == "0"
    assert notation.repeating is None


def test_to_notation_integer_single_digit():
    """Test notation rendering for single sexagesimal digit (values 0-35 use 0-9,A-Z)."""
    eng = Base60Engine()
    # 30 in base 60 = "U" (since digits are 0-9,A-Z for 0-35)
    bn = eng.from_rational(Rational(30))
    notation = eng.to_notation(bn)
    assert notation.text == "U"
    assert notation.repeating is None


def test_to_notation_integer_multi_digit():
    """Test notation rendering for multiple sexagesimal digits (covers line 231-236)."""
    eng = Base60Engine()
    # 61 = 1*60 + 1 -> "1,1"
    bn = eng.from_rational(Rational(61))
    notation = eng.to_notation(bn)
    assert notation.text == "1,1"
    assert notation.repeating is None
    # 3600 = 1*60^2 + 0*60 + 0 -> "1,0,0"
    bn = eng.from_rational(Rational(3600))
    notation = eng.to_notation(bn)
    assert notation.text == "1,0,0"
    assert notation.repeating is None


def test_to_notation_terminating_fraction():
    """Test terminating fraction (remainder == 0 case, lines 239-240)."""
    eng = Base60Engine()
    # 1/3 = 20/60 = "K" in base-60 digits (since 20 = K)
    bn = eng.from_rational(Rational(1, 3))
    notation = eng.to_notation(bn)
    assert notation.text == "0;K"
    assert notation.repeating is None


def test_to_notation_negative_integer():
    """Test notation rendering for negative numbers."""
    eng = Base60Engine()
    bn = eng.from_rational(Rational(-5))
    notation = eng.to_notation(bn)
    assert notation.text == "-5"
    assert notation.repeating is None


def test_to_notation_negative_fraction():
    """Test notation rendering for negative fractions."""
    eng = Base60Engine()
    bn = eng.from_rational(Rational(-1, 3))
    notation = eng.to_notation(bn)
    assert notation.text == "-0;K"
    assert notation.repeating is None


def test_sexagesimal_digit_symbols():
    """Test that sexagesimal digits work correctly."""
    eng = Base60Engine()
    # Values 0-9 use plain digits
    from base60lab.engines.base60_engine import _sexagesimal_digit
    for i in range(10):
        assert _sexagesimal_digit(i) == str(i)
    # Values 10-35 use A-Z
    for i in range(10, 36):
        expected = chr(ord("A") + i - 10)
        assert _sexagesimal_digit(i) == expected
    # Values 36-59 use <value> format
    for i in range(36, 60):
        assert _sexagesimal_digit(i) == f"<{i}>"


def test_sexagesimal_digit_valueerror():
    """Test _sexagesimal_digit raises ValueError for out-of-range values."""
    from base60lab.engines.base60_engine import _sexagesimal_digit
    try:
        _sexagesimal_digit(-1)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for -1"
    try:
        _sexagesimal_digit(60)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for 60"


def test_terminating_denominators_base60():
    """Test terminating_denominators returns correct list."""
    eng = Base60Engine()
    terms = eng.terminating_denominators(30)
    # Denominators whose prime factors are only 2, 3, and/or 5
    expected = {1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30}
    assert set(terms) == expected


def test_repeating_period_base60():
    """Test repeating_period for various denominators."""
    eng = Base60Engine()
    # 1/7 repeats in base 60
    period = eng.repeating_period(7)
    assert period is not None
    assert period > 0
    # 1/11 repeats in base 60
    period = eng.repeating_period(11)
    assert period is not None
    assert period > 0
    # 1/3 terminates in base 60
    period = eng.repeating_period(3)
    assert period is None


def test_describe_base60():
    """Test describe method returns expected structure."""
    eng = Base60Engine()
    desc = eng.describe()
    assert desc["base"] == 60
    assert desc["name"] == "sexagesimal"
    assert desc["factorisation"] == {2: 2, 3: 1, 5: 1}
    assert "digit_symbols" in desc
    assert desc["fractional_point"] == ";"
    assert "known_truths_complete" in desc
    assert "unknowns_count" in desc


def test_from_rational_with_notation_system():
    """Test from_rational with NotationSystem parameter."""
    from base60lab.core.types import NotationSystem
    eng = Base60Engine()
    # Just test it doesn't crash with the extra parameter
    bn = eng.from_rational(Rational(5))
    assert eng.to_rational(bn) == Rational(5)


def test_unknowns_registry_mutability():
    """Test that unknowns registry can be modified."""
    eng = Base60Engine()
    initial_count = len(eng.unknowns)
    from base60lab.core.unknowns import UnknownEntry
    eng.unknowns.add(UnknownEntry(
        id="test.unknown",
        base=60,
        category="test",
        statement="test statement",
        status="conjecture",
    ))
    assert len(eng.unknowns) == initial_count + 1
