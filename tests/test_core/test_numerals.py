"""Tests for numerals.py — base conversion and arithmetic utilities."""

from base60lab.core.rational import Rational
from base60lab.numerals import (
    DIGITS_10,
    DIGITS_12,
    DIGITS_60,
    DIGIT_VALUE_10,
    DIGIT_VALUE_12,
    DIGIT_VALUE_60,
    digits_for_base,
    digit_value_for_base,
    base_digit_symbol,
    int_to_base,
    int_from_base,
    rational_to_base,
    rational_from_base,
    is_terminating_in_base,
    repeating_period_in_base,
    terminating_denominators,
    convert_base,
    convert_rational_base,
)


# -- Digit symbol tables -------------------------------------------------------

def test_digits_10():
    assert DIGITS_10 == tuple(str(d) for d in range(10))
    assert len(DIGITS_10) == 10


def test_digits_12():
    expected = tuple(str(d) for d in range(10)) + ("A", "B")
    assert DIGITS_12 == expected
    assert len(DIGITS_12) == 12


def test_digits_60():
    expected = tuple(str(d) for d in range(10)) + tuple(chr(ord("A") + i) for i in range(26))
    assert DIGITS_60 == expected
    assert len(DIGITS_60) == 36  # 0-9, A-Z (10-35); 36-59 use angle brackets


def test_digit_value_maps():
    assert DIGIT_VALUE_10 == {d: i for i, d in enumerate(DIGITS_10)}
    assert DIGIT_VALUE_12 == {d: i for i, d in enumerate(DIGITS_12)}
    # 60 includes angle bracket notation
    assert DIGIT_VALUE_60["0"] == 0
    assert DIGIT_VALUE_60["9"] == 9
    assert DIGIT_VALUE_60["A"] == 10
    assert DIGIT_VALUE_60["Z"] == 35
    assert DIGIT_VALUE_60["<36>"] == 36
    assert DIGIT_VALUE_60["<59>"] == 59


def test_digits_for_base():
    assert digits_for_base(10) == DIGITS_10
    assert digits_for_base(12) == DIGITS_12
    assert digits_for_base(60) == DIGITS_60


def test_digits_for_base_invalid():
    try:
        digits_for_base(2)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)
    try:
        digits_for_base(16)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)


def test_digit_value_for_base():
    assert digit_value_for_base(10) == DIGIT_VALUE_10
    assert digit_value_for_base(12) == DIGIT_VALUE_12
    assert digit_value_for_base(60) == DIGIT_VALUE_60


def test_digit_value_for_base_invalid():
    try:
        digit_value_for_base(2)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)


def test_base_digit_symbol_base10():
    for i in range(10):
        assert base_digit_symbol(i, 10) == str(i)
    try:
        base_digit_symbol(-1, 10)
        assert False, "should raise"
    except ValueError:
        pass
    try:
        base_digit_symbol(10, 10)
        assert False, "should raise"
    except ValueError:
        pass


def test_base_digit_symbol_base12():
    for i in range(10):
        assert base_digit_symbol(i, 12) == str(i)
    assert base_digit_symbol(10, 12) == "A"
    assert base_digit_symbol(11, 12) == "B"
    try:
        base_digit_symbol(-1, 12)
        assert False, "should raise"
    except ValueError:
        pass
    try:
        base_digit_symbol(12, 12)
        assert False, "should raise"
    except ValueError:
        pass


def test_base_digit_symbol_base60():
    for i in range(10):
        assert base_digit_symbol(i, 60) == str(i)
    for i in range(10, 36):
        assert base_digit_symbol(i, 60) == chr(ord("A") + i - 10)
    for i in range(36, 60):
        assert base_digit_symbol(i, 60) == f"<{i}>"
    try:
        base_digit_symbol(-1, 60)
        assert False, "should raise"
    except ValueError:
        pass
    try:
        base_digit_symbol(60, 60)
        assert False, "should raise"
    except ValueError:
        pass


def test_base_digit_symbol_invalid_base():
    try:
        base_digit_symbol(0, 2)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)


# -- Integer to base string conversion ----------------------------------------

def test_int_to_base_base10():
    assert int_to_base(0, 10) == "0"
    assert int_to_base(5, 10) == "5"
    assert int_to_base(255, 10) == "255"
    assert int_to_base(1000, 10) == "1000"


def test_int_to_base_base12():
    assert int_to_base(0, 12) == "0"
    assert int_to_base(5, 12) == "5"
    assert int_to_base(10, 12) == "A"
    assert int_to_base(11, 12) == "B"
    assert int_to_base(12, 12) == "10"
    assert int_to_base(13, 12) == "11"
    assert int_to_base(143, 12) == "BB"  # 11*12 + 11 = 143
    assert int_to_base(144, 12) == "100"  # 12^2 = 144


def test_int_to_base_base60():
    assert int_to_base(0, 60) == "0"
    assert int_to_base(5, 60) == "5"
    assert int_to_base(10, 60) == "A"
    assert int_to_base(35, 60) == "Z"
    assert int_to_base(36, 60) == "<36>"
    assert int_to_base(59, 60) == "<59>"
    assert int_to_base(60, 60) == "1,0"
    assert int_to_base(3600, 60) == "1,0,0"  # 60^2 = 3600


def test_int_to_base_negative_raises():
    try:
        int_to_base(-1, 10)
        assert False, "should raise"
    except ValueError as e:
        assert "negative integers not supported" in str(e)


def test_int_to_base_invalid_base():
    try:
        int_to_base(10, 2)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)
    try:
        int_to_base(10, 16)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)


# -- Base string to integer conversion ----------------------------------------

def test_int_from_base_base10():
    assert int_from_base("0", 10) == 0
    assert int_from_base("5", 10) == 5
    assert int_from_base("255", 10) == 255
    assert int_from_base("1000", 10) == 1000


def test_int_from_base_base12():
    assert int_from_base("0", 12) == 0
    assert int_from_base("5", 12) == 5
    assert int_from_base("A", 12) == 10
    assert int_from_base("B", 12) == 11
    assert int_from_base("10", 12) == 12
    assert int_from_base("11", 12) == 13
    assert int_from_base("BB", 12) == 143
    assert int_from_base("100", 12) == 144


def test_int_from_base_base60():
    assert int_from_base("0", 60) == 0
    assert int_from_base("5", 60) == 5
    assert int_from_base("A", 60) == 10
    assert int_from_base("Z", 60) == 35
    assert int_from_base("<36>", 60) == 36
    assert int_from_base("<59>", 60) == 59
    assert int_from_base("10", 60) == 60
    assert int_from_base("1,0", 60) == 60  # Comma separated
    assert int_from_base("100", 60) == 3600


def test_int_from_base_multi_digit_base60():
    # Multi-digit base-60 numbers use comma or just concatenation
    assert int_from_base("1,0", 60) == 60
    assert int_from_base("1,U", 60) == 90  # 1*60 + 30 (U = 30)
    assert int_from_base("2,0,0", 60) == 7200  # 2*60^2


def test_int_from_base_empty_raises():
    try:
        int_from_base("", 10)
        assert False, "should raise"
    except ValueError as e:
        assert "empty string" in str(e)


def test_int_from_base_invalid_digit_raises():
    try:
        int_from_base("G", 12)
        assert False, "should raise"
    except ValueError as e:
        assert "invalid digit" in str(e)
    try:
        int_from_base("2", 2)
        assert False, "should raise"
    except ValueError as e:
        # Base 2 is not supported at all, so we get "unsupported base" error
        assert "unsupported base" in str(e)
    try:
        int_from_base("<60>", 60)
        assert False, "should raise"
    except ValueError as e:
        assert "invalid digit" in str(e)


def test_int_from_base_unclosed_bracket_raises():
    try:
        int_from_base("<36", 60)
        assert False, "should raise"
    except ValueError as e:
        assert "unclosed angle bracket" in str(e)


def test_int_from_base_invalid_base():
    try:
        int_from_base("10", 2)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)


# -- Round-trip integer conversion --------------------------------------------

def test_round_trip_integers():
    for base in (10, 12, 60):
        for n in range(0, 1000):
            s = int_to_base(n, base)
            m = int_from_base(s, base)
            assert m == n, f"round-trip failed for {n} in base {base}: {s} -> {m}"


def test_round_trip_large_integers():
    for base in (10, 12, 60):
        for n in [3600, 10000, 36000, 216000, 1000000]:
            s = int_to_base(n, base)
            m = int_from_base(s, base)
            assert m == n, f"round-trip failed for {n} in base {base}"


# -- Rational to base string conversion ---------------------------------------

def test_rational_to_base_integers():
    for base in (10, 12, 60):
        for n in [0, 1, 5, 10, 100]:
            r = Rational(n)
            s = rational_to_base(r, base)
            assert s == int_to_base(n, base)


def test_rational_to_base_negative():
    r = Rational(-5)
    assert rational_to_base(r, 10) == "-5"
    assert rational_to_base(r, 12) == "-5"
    assert rational_to_base(r, 60) == "-5"

    r = Rational(-1, 2)
    s10 = rational_to_base(r, 10)
    s12 = rational_to_base(r, 12)
    s60 = rational_to_base(r, 60)
    assert s10 == "-0.5"
    assert s12 == "-0.6"
    # In base 60, 30 is represented as 'U' (A=10, B=11, ..., U=30)
    assert s60 == "-0;U"


def test_rational_to_base_terminating_base10():
    # 1/2 = 0.5
    assert rational_to_base(Rational(1, 2), 10) == "0.5"
    # 1/4 = 0.25
    assert rational_to_base(Rational(1, 4), 10) == "0.25"
    # 1/5 = 0.2
    assert rational_to_base(Rational(1, 5), 10) == "0.2"
    # 1/8 = 0.125
    assert rational_to_base(Rational(1, 8), 10) == "0.125"
    # 3/2 = 1.5
    assert rational_to_base(Rational(3, 2), 10) == "1.5"


def test_rational_to_base_terminating_base12():
    # 1/2 = 0.6 (base 12)
    assert rational_to_base(Rational(1, 2), 12) == "0.6"
    # 1/3 = 0.4 (base 12) - terminates because 3 divides 12
    assert rational_to_base(Rational(1, 3), 12) == "0.4"
    # 1/4 = 0.3 (base 12)
    assert rational_to_base(Rational(1, 4), 12) == "0.3"
    # 1/6 = 0.2 (base 12)
    assert rational_to_base(Rational(1, 6), 12) == "0.2"
    # 1/8 = 0.16 (base 12) - 8 = 2^3, divides 12^2
    assert rational_to_base(Rational(1, 8), 12) == "0.16"
    # 1/9 = 0.14 (base 12) - 9 = 3^2, divides 12^2
    assert rational_to_base(Rational(1, 9), 12) == "0.14"


def test_rational_to_base_terminating_base60():
    # 1/2 = 0;U (base 60) - 30 = U
    assert rational_to_base(Rational(1, 2), 60) == "0;U"
    # 1/3 = 0;K (base 60) - 20 = K
    assert rational_to_base(Rational(1, 3), 60) == "0;K"
    # 1/4 = 0;F (base 60) - 15 = F
    assert rational_to_base(Rational(1, 4), 60) == "0;F"
    # 1/5 = 0;C (base 60) - 12 = C
    assert rational_to_base(Rational(1, 5), 60) == "0;C"
    # 1/6 = 0;A (base 60) - 10 = A
    assert rational_to_base(Rational(1, 6), 60) == "0;A"
    # 1/8 = 0;7,U (base 60) = 7/60 + 30/3600 = 450/3600 = 1/8
    assert rational_to_base(Rational(1, 8), 60) == "0;7,U"
    # 1/9 = 0;6,<40> (base 60) - 6/60 + 40/3600 = 400/3600 = 1/9
    assert rational_to_base(Rational(1, 9), 60) == "0;6,<40>"
    # 1/10 = 0;6 (base 60)
    assert rational_to_base(Rational(1, 10), 60) == "0;6"


def test_rational_to_base_repeating_base10():
    # 1/3 = 0.(3)
    s = rational_to_base(Rational(1, 3), 10)
    assert s == "0.(3)"
    # 1/7 = 0.(142857)
    s = rational_to_base(Rational(1, 7), 10)
    assert s == "0.(142857)"
    # 1/6 = 0.1(6)
    s = rational_to_base(Rational(1, 6), 10)
    assert s == "0.1(6)"
    # 1/9 = 0.(1)
    s = rational_to_base(Rational(1, 9), 10)
    assert s == "0.(1)"


def test_rational_to_base_repeating_base12():
    # 1/5 in base 12: period 4 (12 ≡ 2 mod 5, 2^4 ≡ 1 mod 5)
    s = rational_to_base(Rational(1, 5), 12)
    assert s == "0.(2497)"
    # 1/7 in base 12: period 6
    s = rational_to_base(Rational(1, 7), 12)
    assert s == "0.(186A35)"
    # 1/10 = 0.1(2497) (non-repeating 1/2 then repeating 1/5)
    s = rational_to_base(Rational(1, 10), 12)
    assert s == "0.1(2497)"


def test_rational_to_base_repeating_base60():
    # 1/7 in base 60: period 3 (60 ≡ 4 mod 7, 4^3 ≡ 1 mod 7)
    s = rational_to_base(Rational(1, 7), 60)
    # 8 = 8, 34 = Y, 17 = H (A=10, B=11, ..., H=17, ..., Y=34)
    assert s == "0;(8,Y,H)"


def test_rational_to_base_max_digits():
    # Very long repeating period - should truncate with ...
    s = rational_to_base(Rational(1, 97), 10, max_digits=50)
    assert s.endswith("...")


def test_rational_to_base_invalid_base():
    try:
        rational_to_base(Rational(1, 2), 2)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)


# -- Rational from base string conversion -------------------------------------

def test_rational_from_base_integers():
    for base in (10, 12, 60):
        for n in [0, 1, 5, 10, 100]:
            s = int_to_base(n, base)
            r = rational_from_base(s, base)
            assert r == Rational(n)


def test_rational_from_base_negative():
    r = rational_from_base("-5", 10)
    assert r == Rational(-5)
    r = rational_from_base("-0.5", 10)
    assert r == Rational(-1, 2)
    r = rational_from_base("-0;U", 60)
    assert r == Rational(-1, 2)


def test_rational_from_base_terminating_base10():
    assert rational_from_base("0.5", 10) == Rational(1, 2)
    assert rational_from_base("0.25", 10) == Rational(1, 4)
    assert rational_from_base("0.2", 10) == Rational(1, 5)
    assert rational_from_base("1.5", 10) == Rational(3, 2)


def test_rational_from_base_terminating_base12():
    assert rational_from_base("0.6", 12) == Rational(1, 2)
    assert rational_from_base("0.4", 12) == Rational(1, 3)
    assert rational_from_base("0.3", 12) == Rational(1, 4)
    assert rational_from_base("0.2", 12) == Rational(1, 6)


def test_rational_from_base_terminating_base60():
    assert rational_from_base("0;U", 60) == Rational(1, 2)    # U = 30
    assert rational_from_base("0;K", 60) == Rational(1, 3)    # K = 20
    assert rational_from_base("0;F", 60) == Rational(1, 4)    # F = 15
    assert rational_from_base("0;C", 60) == Rational(1, 5)    # C = 12
    assert rational_from_base("0;A", 60) == Rational(1, 6)    # A = 10
    assert rational_from_base("0;7,U", 60) == Rational(1, 8)  # 7/60 + 30/3600

def test_rational_from_base_repeating_base10():
    assert rational_from_base("0.(3)", 10) == Rational(1, 3)
    assert rational_from_base("0.1(6)", 10) == Rational(1, 6)
    assert rational_from_base("0.(142857)", 10) == Rational(1, 7)
    assert rational_from_base("1.(3)", 10) == Rational(4, 3)


def test_rational_from_base_repeating_base12():
    assert rational_from_base("0.(2497)", 12) == Rational(1, 5)
    assert rational_from_base("0.1(2497)", 12) == Rational(1, 10)


def test_rational_from_base_repeating_base60():
    assert rational_from_base("0;(8,Y,H)", 60) == Rational(1, 7)


def test_rational_from_base_invalid_format():
    try:
        rational_from_base("0.(3", 10)
        assert False, "should raise"
    except ValueError as e:
        assert "unclosed parenthesis" in str(e)
    try:
        rational_from_base("0.()", 10)
        assert False, "should raise"
    except ValueError as e:
        assert "empty repeating part" in str(e)
    try:
        rational_from_base("", 10)
        assert False, "should raise"
    except ValueError as e:
        assert "empty string" in str(e)


def test_rational_from_base_invalid_digit():
    try:
        rational_from_base("G", 12)
        assert False, "should raise"
    except ValueError as e:
        assert "invalid digit" in str(e)


def test_rational_from_base_invalid_base():
    try:
        rational_from_base("0.5", 2)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)


# -- Round-trip rational conversion -------------------------------------------

def test_round_trip_rationals_terminating():
    for base in (10, 12, 60):
        test_cases = [
            Rational(1, 2),
            Rational(1, 3),
            Rational(1, 4),
            Rational(1, 5),
            Rational(1, 6),
            Rational(1, 8),
            Rational(1, 9),
            Rational(1, 10),
            Rational(1, 12),
            Rational(1, 15),
            Rational(1, 16),
            Rational(1, 20),
            Rational(1, 24),
            Rational(1, 25),
            Rational(1, 30),
            Rational(1, 36),
            Rational(1, 40),
            Rational(1, 45),
            Rational(1, 48),
            Rational(1, 50),
            Rational(1, 60),
            Rational(3, 2),
            Rational(5, 4),
            Rational(7, 3),
            Rational(11, 6),
        ]
        for r in test_cases:
            if r.is_terminating_in_base(base):
                s = rational_to_base(r, base)
                r2 = rational_from_base(s, base)
                assert r2 == r, f"round-trip failed for {r} in base {base}: {s}"


def test_round_trip_rationals_repeating():
    for base in (10, 12, 60):
        test_cases = [
            Rational(1, 7),
            Rational(1, 11),
            Rational(1, 13),
            Rational(1, 14),
            Rational(1, 17),
            Rational(1, 19),
            Rational(1, 21),
            Rational(1, 22),
            Rational(1, 23),
            Rational(1, 26),
            Rational(1, 27),
            Rational(1, 28),
            Rational(1, 29),
            Rational(1, 31),
        ]
        for r in test_cases:
            if not r.is_terminating_in_base(base):
                s = rational_to_base(r, base)
                r2 = rational_from_base(s, base)
                assert r2 == r, f"round-trip failed for {r} in base {base}: {s}"


# -- Terminating detection ----------------------------------------------------

def test_is_terminating_in_base_base10():
    assert is_terminating_in_base(1, 10) is True
    assert is_terminating_in_base(2, 10) is True
    assert is_terminating_in_base(4, 10) is True
    assert is_terminating_in_base(5, 10) is True
    assert is_terminating_in_base(8, 10) is True
    assert is_terminating_in_base(10, 10) is True
    assert is_terminating_in_base(16, 10) is True
    assert is_terminating_in_base(20, 10) is True
    assert is_terminating_in_base(25, 10) is True
    assert is_terminating_in_base(3, 10) is False
    assert is_terminating_in_base(6, 10) is False
    assert is_terminating_in_base(7, 10) is False
    assert is_terminating_in_base(9, 10) is False
    assert is_terminating_in_base(11, 10) is False


def test_is_terminating_in_base_base12():
    assert is_terminating_in_base(1, 12) is True
    assert is_terminating_in_base(2, 12) is True
    assert is_terminating_in_base(3, 12) is True
    assert is_terminating_in_base(4, 12) is True
    assert is_terminating_in_base(6, 12) is True
    assert is_terminating_in_base(8, 12) is True
    assert is_terminating_in_base(9, 12) is True
    assert is_terminating_in_base(12, 12) is True
    assert is_terminating_in_base(16, 12) is True
    assert is_terminating_in_base(18, 12) is True
    assert is_terminating_in_base(5, 12) is False
    assert is_terminating_in_base(7, 12) is False
    assert is_terminating_in_base(10, 12) is False  # 10 = 2*5, 5 doesn't divide 12
    assert is_terminating_in_base(11, 12) is False


def test_is_terminating_in_base_base60():
    # 60 = 2^2 * 3 * 5, so any denominator with only factors 2, 3, 5 terminates
    assert is_terminating_in_base(1, 60) is True
    assert is_terminating_in_base(2, 60) is True
    assert is_terminating_in_base(3, 60) is True
    assert is_terminating_in_base(4, 60) is True
    assert is_terminating_in_base(5, 60) is True
    assert is_terminating_in_base(6, 60) is True
    assert is_terminating_in_base(8, 60) is True
    assert is_terminating_in_base(9, 60) is True
    assert is_terminating_in_base(10, 60) is True
    assert is_terminating_in_base(12, 60) is True
    assert is_terminating_in_base(15, 60) is True
    assert is_terminating_in_base(16, 60) is True
    assert is_terminating_in_base(18, 60) is True
    assert is_terminating_in_base(20, 60) is True
    assert is_terminating_in_base(24, 60) is True
    assert is_terminating_in_base(25, 60) is True
    assert is_terminating_in_base(27, 60) is True
    assert is_terminating_in_base(30, 60) is True
    assert is_terminating_in_base(36, 60) is True
    assert is_terminating_in_base(40, 60) is True
    assert is_terminating_in_base(45, 60) is True
    assert is_terminating_in_base(48, 60) is True
    assert is_terminating_in_base(50, 60) is True
    assert is_terminating_in_base(60, 60) is True
    assert is_terminating_in_base(7, 60) is False
    assert is_terminating_in_base(11, 60) is False
    assert is_terminating_in_base(13, 60) is False
    assert is_terminating_in_base(14, 60) is False  # 14 = 2*7
    assert is_terminating_in_base(17, 60) is False


def test_is_terminating_in_base_invalid_base():
    try:
        is_terminating_in_base(1, 1)
        assert False, "should raise"
    except ValueError as e:
        assert "base must be >= 2" in str(e)


def test_is_terminating_in_base_invalid_denominator():
    try:
        is_terminating_in_base(0, 10)
        assert False, "should raise"
    except ValueError as e:
        assert "denominator must be positive" in str(e)
    try:
        is_terminating_in_base(-1, 10)
        assert False, "should raise"
    except ValueError as e:
        assert "denominator must be positive" in str(e)


# -- Repeating period ---------------------------------------------------------

def test_repeating_period_in_base_base10():
    assert repeating_period_in_base(1, 10) is None
    assert repeating_period_in_base(2, 10) is None
    assert repeating_period_in_base(3, 10) == 1
    assert repeating_period_in_base(6, 10) == 1
    assert repeating_period_in_base(7, 10) == 6
    assert repeating_period_in_base(9, 10) == 1
    assert repeating_period_in_base(11, 10) == 2
    assert repeating_period_in_base(13, 10) == 6
    assert repeating_period_in_base(17, 10) == 16
    assert repeating_period_in_base(19, 10) == 18


def test_repeating_period_in_base_base12():
    assert repeating_period_in_base(1, 12) is None
    assert repeating_period_in_base(2, 12) is None
    assert repeating_period_in_base(3, 12) is None
    assert repeating_period_in_base(4, 12) is None
    assert repeating_period_in_base(5, 12) == 4  # 12^4 ≡ 1 (mod 5)
    assert repeating_period_in_base(7, 12) == 6
    assert repeating_period_in_base(10, 12) == 4  # 10 = 2*5, period from 5


def test_repeating_period_in_base_base60():
    assert repeating_period_in_base(1, 60) is None
    assert repeating_period_in_base(2, 60) is None
    assert repeating_period_in_base(3, 60) is None
    assert repeating_period_in_base(5, 60) is None
    assert repeating_period_in_base(7, 60) == 3  # 60^3 ≡ 1 (mod 7)
    # 60 ≡ 5 (mod 11), 5^1=5, 5^2=3, 5^3=4, 5^4=9, 5^5=1 => period = 5
    assert repeating_period_in_base(11, 60) == 5
    # 60 ≡ 8 (mod 13), 8^1=8, 8^2=12, 8^3=5, 8^4=1 => period = 4
    assert repeating_period_in_base(13, 60) == 4
    assert repeating_period_in_base(14, 60) == 3  # 14 = 2*7, period from 7


def test_repeating_period_in_base_invalid():
    try:
        repeating_period_in_base(1, 1)
        assert False, "should raise"
    except ValueError as e:
        assert "base must be >= 2" in str(e)
    try:
        repeating_period_in_base(0, 10)
        assert False, "should raise"
    except ValueError as e:
        assert "denominator must be positive" in str(e)


# -- Terminating denominators -------------------------------------------------

def test_terminating_denominators_base10():
    terms = terminating_denominators(10, 100)
    assert 1 in terms
    assert 2 in terms
    assert 4 in terms
    assert 5 in terms
    assert 8 in terms
    assert 10 in terms
    assert 3 not in terms
    assert 7 not in terms
    assert 9 not in terms
    assert 11 not in terms


def test_terminating_denominators_base12():
    terms = terminating_denominators(12, 100)
    assert 1 in terms
    assert 2 in terms
    assert 3 in terms
    assert 4 in terms
    assert 6 in terms
    assert 8 in terms
    assert 9 in terms
    assert 12 in terms
    assert 5 not in terms
    assert 7 not in terms
    assert 10 not in terms
    assert 11 not in terms


def test_terminating_denominators_base60():
    terms = terminating_denominators(60, 100)
    assert 1 in terms
    assert 2 in terms
    assert 3 in terms
    assert 4 in terms
    assert 5 in terms
    assert 6 in terms
    assert 8 in terms
    assert 9 in terms
    assert 10 in terms
    assert 12 in terms
    assert 15 in terms
    assert 16 in terms
    assert 18 in terms
    assert 20 in terms
    assert 24 in terms
    assert 25 in terms
    assert 27 in terms
    assert 30 in terms
    assert 7 not in terms
    assert 11 not in terms
    assert 13 not in terms
    assert 14 not in terms


def test_terminating_denominators_invalid_base():
    try:
        terminating_denominators(2, 100)
        assert False, "should raise"
    except ValueError as e:
        assert "unsupported base" in str(e)


# -- Base conversion ----------------------------------------------------------

def test_convert_base_integer():
    # 255 in base 10 -> base 12
    assert convert_base("255", 10, 12) == "193"  # 1*144 + 9*12 + 3 = 255
    # 255 in base 12 -> base 10
    assert convert_base("193", 12, 10) == "255"
    # 255 in base 10 -> base 60 (4*60 + 15 = 255, 15 = F)
    assert convert_base("255", 10, 60) == "4,F"
    # 255 in base 60 -> base 10
    assert convert_base("4,F", 60, 10) == "255"
    # 3600 in base 10 -> base 60
    assert convert_base("3600", 10, 60) == "1,0,0"
    # Same base returns same
    assert convert_base("255", 10, 10) == "255"


def test_convert_base_rational():
    # 1/2 in base 10 -> base 12
    assert convert_rational_base("0.5", 10, 12) == "0.6"
    # 1/3 in base 10 -> base 12 (terminates in base 12!)
    assert convert_rational_base("0.(3)", 10, 12) == "0.4"
    # 1/2 in base 12 -> base 10
    assert convert_rational_base("0.6", 12, 10) == "0.5"
    # 1/3 in base 12 -> base 10 (repeating in base 10)
    assert convert_rational_base("0.4", 12, 10) == "0.(3)"
    # 1/2 in base 60 -> base 10 (U = 30)
    assert convert_rational_base("0;U", 60, 10) == "0.5"
    # Same base returns same
    assert convert_rational_base("0.5", 10, 10) == "0.5"


# -- Rational integration -----------------------------------------------------

def test_rational_methods_consistency():
    # Verify Rational.is_terminating_in_base matches our function
    for base in (10, 12, 60):
        for d in range(1, 100):
            r = Rational(1, d)
            assert r.is_terminating_in_base(base) == is_terminating_in_base(d, base)

    # Verify Rational.repeating_period_in_base matches our function
    for base in (10, 12, 60):
        for d in range(1, 100):
            r = Rational(1, d)
            assert r.repeating_period_in_base(base) == repeating_period_in_base(d, base)


# -- Edge cases ---------------------------------------------------------------

def test_large_numbers():
    # Test with large integers
    n = 10**10
    for base in (10, 12, 60):
        s = int_to_base(n, base)
        m = int_from_base(s, base)
        assert m == n


def test_zero_handling():
    for base in (10, 12, 60):
        assert int_to_base(0, base) == "0"
        assert int_from_base("0", base) == 0
        assert rational_to_base(Rational(0), base) == "0"
        assert rational_from_base("0", base) == Rational(0)


def test_negative_zero():
    # Negative zero should be handled as zero
    r = Rational(0)
    for base in (10, 12, 60):
        assert rational_to_base(r, base) == "0"
    r = Rational(-0)
    for base in (10, 12, 60):
        assert rational_to_base(r, base) == "0"


def test_fractional_point_conventions():
    # Base 10 and 12 use '.'
    assert "." in rational_to_base(Rational(1, 2), 10)
    assert "." in rational_to_base(Rational(1, 2), 12)
    # Base 60 uses ';'
    assert ";" in rational_to_base(Rational(1, 2), 60)
    assert "." not in rational_to_base(Rational(1, 2), 60)


def test_repeating_parentheses():
    for base in (10, 12, 60):
        r = Rational(1, 7)
        s = rational_to_base(r, base)
        if not r.is_terminating_in_base(base):
            assert "(" in s
            assert ")" in s
            # Opening paren before closing
            assert s.index("(") < s.index(")")
            # Non-empty repeating part
            assert s.index(")") > s.index("(") + 1