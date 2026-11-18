"""Tests for core rational arithmetic."""

from fractions import Fraction
from base60lab.core.rational import Rational, rational, zero, one


# -- Construction -------------------------------------------------------------

def test_init_from_int():
    r = Rational(5)
    assert r.numerator == 5
    assert r.denominator == 1


def test_init_from_int_pair():
    r = Rational(3, 6)  # should reduce to 1/2
    assert r.numerator == 1
    assert r.denominator == 2


def test_init_from_negative():
    r = Rational(-3, 6)
    assert r.numerator == -1
    assert r.denominator == 2


def test_init_from_rational():
    r1 = Rational(2, 4)
    r2 = Rational(r1)
    assert r2.numerator == 1
    assert r2.denominator == 2
    assert r2 is not r1


def test_init_from_fraction():
    r = Rational(Fraction(3, 9))
    assert r.numerator == 1
    assert r.denominator == 3


# -- Arithmetic ---------------------------------------------------------------

def test_addition_exact():
    assert Rational(1, 3) + Rational(1, 6) == Rational(1, 2)


def test_addition_with_int():
    assert Rational(1, 2) + 1 == Rational(3, 2)

def test_addition_with_fraction():
    assert Rational(1, 2) + Fraction(1, 3) == Rational(5, 6)


def test_subtraction_exact():
    assert Rational(1, 2) - Rational(1, 3) == Rational(1, 6)


def test_subtraction_with_int():
    assert Rational(3, 2) - 1 == Rational(1, 2)
    assert Rational(1, 2) - 2 == Rational(-3, 2)

def test_subtraction_with_fraction():
    assert Rational(5, 6) - Fraction(1, 3) == Rational(1, 2)


def test_multiplication_exact():
    assert Rational(2, 3) * Rational(3, 4) == Rational(1, 2)


def test_multiplication_with_int():
    assert Rational(1, 3) * 3 == Rational(1)

def test_multiplication_with_fraction():
    assert Rational(1, 2) * Fraction(2, 3) == Rational(1, 3)


def test_division_exact():
    assert Rational(1, 2) / Rational(1, 4) == Rational(2)


def test_division_with_int():
    assert Rational(1, 2) / 2 == Rational(1, 4)
    assert Rational(1) / Rational(2) == Rational(1, 2)

def test_division_with_fraction():
    assert Rational(1, 2) / Fraction(1, 4) == Rational(2)


def test_division_by_zero_raises():
    try:
        Rational(1) / Rational(0)
        assert False, "should have raised ZeroDivisionError"
    except ZeroDivisionError:
        pass

    try:
        Rational(1) / 0
        assert False, "should have raised ZeroDivisionError"
    except ZeroDivisionError:
        pass


def test_power_positive():
    assert Rational(2, 3) ** 2 == Rational(4, 9)
    assert Rational(2) ** 3 == Rational(8)


def test_power_zero():
    assert Rational(5, 7) ** 0 == Rational(1)
    assert Rational(0) ** 0 == Rational(1)  # 0^0 = 1 in Python


def test_power_negative():
    assert Rational(2, 3) ** -1 == Rational(3, 2)
    assert Rational(2) ** -2 == Rational(1, 4)


def test_negation():
    assert -Rational(3, 4) == Rational(-3, 4)
    assert -Rational(-2, 5) == Rational(2, 5)


def test_absolute_value():
    assert abs(Rational(3, 4)) == Rational(3, 4)
    assert abs(Rational(-3, 4)) == Rational(3, 4)
    assert abs(Rational(0)) == Rational(0)


# -- Comparison ---------------------------------------------------------------

def test_equality_base_independent():
    assert Rational(2, 4) == Rational(1, 2)
    assert Rational(-2, 4) == Rational(-1, 2)


def test_equality_with_int():
    assert Rational(5, 1) == 5
    assert 5 == Rational(5, 1)
    assert Rational(1, 2) != 1


def test_equality_with_fraction():
    assert Rational(1, 2) == Fraction(1, 2)
    assert Fraction(1, 2) == Rational(1, 2)
    assert Rational(1, 3) != Fraction(1, 2)


def test_equality_not_implemented():
    r = Rational(1, 2)
    assert r.__eq__("not a number") is NotImplemented
    assert r.__eq__(None) is NotImplemented


def test_less_than():
    assert Rational(1, 3) < Rational(1, 2)
    assert Rational(1, 2) < 1
    assert Rational(1, 2) < Fraction(2, 3)


def test_less_than_or_equal():
    assert Rational(1, 2) <= Rational(1, 2)
    assert Rational(1, 3) <= Rational(1, 2)
    assert Rational(1, 2) <= 1
    assert Rational(1, 2) <= Fraction(1, 2)


def test_greater_than():
    assert Rational(1, 2) > Rational(1, 3)
    assert Rational(3, 2) > 1
    assert Rational(2, 3) > Fraction(1, 2)


def test_greater_than_or_equal():
    assert Rational(1, 2) >= Rational(1, 2)
    assert Rational(1, 2) >= Rational(1, 3)
    assert Rational(1) >= Rational(1, 2)
    assert Rational(1, 2) >= Fraction(1, 2)


# -- Properties ---------------------------------------------------------------

def test_numerator():
    assert Rational(3, 7).numerator == 3
    assert Rational(-5, 2).numerator == -5
    assert Rational(0).numerator == 0


def test_denominator():
    assert Rational(3, 7).denominator == 7
    assert Rational(-5, 2).denominator == 2
    assert Rational(0).denominator == 1
    assert Rational(5).denominator == 1


def test_is_integer():
    assert Rational(5).is_integer() is True
    assert Rational(10, 2).is_integer() is True
    assert Rational(1, 2).is_integer() is False
    assert Rational(0).is_integer() is True


# -- Base termination / repeating ---------------------------------------------

def test_terminating_base10():
    assert Rational(1, 2).is_terminating_in_base(10) is True
    assert Rational(1, 5).is_terminating_in_base(10) is True
    assert Rational(1, 4).is_terminating_in_base(10) is True
    assert Rational(1, 8).is_terminating_in_base(10) is True
    assert Rational(1, 3).is_terminating_in_base(10) is False
    assert Rational(1, 6).is_terminating_in_base(10) is False
    assert Rational(1, 7).is_terminating_in_base(10) is False


def test_terminating_base12():
    assert Rational(1, 3).is_terminating_in_base(12) is True
    assert Rational(1, 4).is_terminating_in_base(12) is True
    assert Rational(1, 6).is_terminating_in_base(12) is True
    assert Rational(1, 5).is_terminating_in_base(12) is False
    assert Rational(1, 7).is_terminating_in_base(12) is False


def test_terminating_base60():
    assert Rational(1, 3).is_terminating_in_base(60) is True
    assert Rational(1, 5).is_terminating_in_base(60) is True
    assert Rational(1, 2).is_terminating_in_base(60) is True
    assert Rational(1, 7).is_terminating_in_base(60) is False
    assert Rational(1, 11).is_terminating_in_base(60) is False


def test_terminating_invalid_base():
    try:
        Rational(1, 2).is_terminating_in_base(1)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "base must be >= 2" in str(e)

    try:
        Rational(1, 2).is_terminating_in_base(0)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "base must be >= 2" in str(e)


def test_repeating_period_base10():
    assert Rational(1, 3).repeating_period_in_base(10) == 1
    assert Rational(1, 7).repeating_period_in_base(10) == 6
    assert Rational(1, 6).repeating_period_in_base(10) == 1
    assert Rational(1, 9).repeating_period_in_base(10) == 1


def test_repeating_period_base12():
    # 1/5 in base 12: 5 is coprime to 12, period = multiplicative order of 12 mod 5
    # 12 ≡ 2 (mod 5), 2^1=2, 2^2=4, 2^3=3, 2^4=1 => period = 4
    assert Rational(1, 5).repeating_period_in_base(12) == 4
    # 1/7 in base 12: 7 is coprime to 12, period = multiplicative order of 12 mod 7
    # 12 ≡ 5 (mod 7), 5^1=5, 5^2=4, 5^3=6, 5^4=2, 5^5=3, 5^6=1 => period = 6
    assert Rational(1, 7).repeating_period_in_base(12) == 6
    # terminating cases
    assert Rational(1, 3).repeating_period_in_base(12) is None  # terminates
    assert Rational(1, 4).repeating_period_in_base(12) is None  # terminates


def test_repeating_period_base60():
    # 1/7 in base 60: 7 is coprime to 60, period = multiplicative order of 60 mod 7
    # 60 ≡ 4 (mod 7), 4^1=4, 4^2=16≡2, 4^3=8≡1 => period = 3
    assert Rational(1, 7).repeating_period_in_base(60) == 3
    # terminating cases return None
    assert Rational(1, 3).repeating_period_in_base(60) is None
    assert Rational(1, 5).repeating_period_in_base(60) is None
    assert Rational(1, 2).repeating_period_in_base(60) is None


def test_repeating_period_edge_cases():
    # Integer has no repeating period
    assert Rational(5).repeating_period_in_base(10) is None
    assert Rational(0).repeating_period_in_base(10) is None
    # 1/13 in base 10 has period 6
    assert Rational(1, 13).repeating_period_in_base(10) == 6


# -- Conversion ---------------------------------------------------------------

def test_to_fraction():
    r = Rational(3, 7)
    f = r.to_fraction()
    assert isinstance(f, Fraction)
    assert f == Fraction(3, 7)


def test_to_float():
    assert Rational(1, 2).to_float() == 0.5
    assert Rational(1, 3).to_float() == 1 / 3
    assert Rational(-3, 4).to_float() == -0.75
    assert Rational(0).to_float() == 0.0


# -- Representation -----------------------------------------------------------

def test_repr_integer():
    assert repr(Rational(5)) == "Rational(5)"
    assert repr(Rational(-3)) == "Rational(-3)"
    assert repr(Rational(0)) == "Rational(0)"


def test_repr_fraction():
    assert repr(Rational(3, 7)) == "Rational(3/7)"
    assert repr(Rational(-3, 7)) == "Rational(-3/7)"
    assert repr(Rational(1, 2)) == "Rational(1/2)"


def test_str():
    assert str(Rational(5)) == "Rational(5)"
    assert str(Rational(3, 7)) == "Rational(3/7)"


# -- Hash ---------------------------------------------------------------------

def test_hash():
    assert hash(Rational(1, 2)) == hash(Rational(2, 4))
    assert hash(Rational(3, 7)) == hash(Fraction(3, 7))
    # Hashable in sets/dicts
    s = {Rational(1, 2), Rational(1, 3), Rational(2, 4)}
    assert len(s) == 2  # 1/2 and 2/4 are same
    d = {Rational(1, 2): "half"}
    assert d[Rational(2, 4)] == "half"


# -- Convenience constructors -------------------------------------------------

def test_rational_constructor():
    assert rational(5) == Rational(5)
    assert rational(3, 7) == Rational(3, 7)
    assert rational(Rational(2, 3)) == Rational(2, 3)
    assert rational(Fraction(4, 6)) == Rational(2, 3)


def test_zero():
    assert zero() == Rational(0)
    assert zero().numerator == 0
    assert zero().denominator == 1


def test_one():
    assert one() == Rational(1)
    assert one().numerator == 1
    assert one().denominator == 1


# -- Round-trip / integration -------------------------------------------------

def test_round_trip_integers():
    for n in range(-50, 51):
        for base in (10, 12, 60):
            r = Rational(n)
            assert r.is_terminating_in_base(base) is True


def test_round_trip_fractions():
    # Test various fractions across bases
    test_cases = [
        (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
        (2, 3), (3, 4), (5, 6), (7, 8), (2, 5), (3, 5), (4, 5),
    ]
    for num, den in test_cases:
        for base in (10, 12, 60):
            r = Rational(num, den)
            term = r.is_terminating_in_base(base)
            period = r.repeating_period_in_base(base)
            if term:
                assert period is None
            else:
                assert period is not None
                assert period > 0


def test_arithmetic_chain():
    # Chain operations: 1/2 + 1/3 * 3/4 - 1/6 = 1/2 + 1/4 - 1/6 = 6/12 + 3/12 - 2/12 = 7/12
    r = Rational(1, 2) + Rational(1, 3) * Rational(3, 4) - Rational(1, 6)
    assert r == Rational(7, 12)


def test_comparison_chain():
    assert Rational(1, 3) < Rational(1, 2) < Rational(2, 3)
    assert Rational(1) <= Rational(1) <= Rational(2)
    assert Rational(3) > Rational(2) > Rational(1)
    assert Rational(3) >= Rational(3) >= Rational(2)


def test_negative_denominator():
    # Negative denominator should be normalized
    r = Rational(1, -2)
    assert r.numerator == -1
    assert r.denominator == 2
    assert r == Rational(-1, 2)

    r2 = Rational(-1, -2)
    assert r2.numerator == 1
    assert r2.denominator == 2


def test_large_numbers():
    # Test with large integers
    r = Rational(10**10 + 7, 10**10 + 9)
    assert r.numerator == 10**10 + 7
    assert r.denominator == 10**10 + 9
    assert r.to_float() == (10**10 + 7) / (10**10 + 9)


def test_gcd_edge_cases():
    # Test that fractions are always in lowest terms
    assert Rational(100, 200) == Rational(1, 2)
    assert Rational(999999, 333333) == Rational(3, 1)
    assert Rational(123456, 789012).denominator == 65751  # 789012/123456 = 65751/10288


def test_equality_with_other_types():
    r = Rational(1, 2)
    assert not (r == "1/2")
    assert not (r == [1, 2])
    assert not (r == {"num": 1, "den": 2})
    assert not (r == None)