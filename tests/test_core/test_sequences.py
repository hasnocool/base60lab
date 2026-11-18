"""Tests for number sequences with exact rational arithmetic."""

import pytest

from base60lab.core.rational import Rational
from base60lab import sequences


def test_fibonacci_first_10():
    result = sequences.fibonacci(10)
    assert result == [Rational(0), Rational(1), Rational(1), Rational(2), Rational(3), Rational(5), Rational(8), Rational(13), Rational(21), Rational(34)]


def test_fibonacci_count_zero():
    assert sequences.fibonacci(0) == []


def test_fibonacci_count_one():
    assert sequences.fibonacci(1) == [Rational(0)]


def test_fibonacci_negative_raises():
    with pytest.raises(ValueError):
        sequences.fibonacci(-1)


def test_triangular_first_5():
    result = sequences.triangular(5)
    assert result == [Rational(0), Rational(1), Rational(3), Rational(6), Rational(10)]


def test_triangular_formula():
    # T(n) = n * (n + 1) / 2
    result = sequences.triangular(4)
    assert result == [Rational(0), Rational(1), Rational(3), Rational(6)]


def test_square_first_5():
    result = sequences.square(5)
    assert result == [Rational(0), Rational(1), Rational(4), Rational(9), Rational(16)]


def test_cube_first_3():
    result = sequences.cube(3)
    assert result == [Rational(0), Rational(1), Rational(8)]


def test_perfect_first_2():
    result = sequences.perfect(2)
    assert result == [Rational(6), Rational(28)]


def test_prime_first_5():
    result = sequences.prime(5)
    assert result == [Rational(2), Rational(3), Rational(5), Rational(7), Rational(11)]


def test_geometric_default():
    result = sequences.geometric(3)
    assert result == [Rational(1), Rational(2), Rational(4)]


def test_geometric_custom_ratio():
    result = sequences.geometric(3, ratio=3, start=2)
    assert result == [Rational(2), Rational(6), Rational(18)]


def test_harmonic_first_3():
    result = sequences.harmonic(3)
    assert result == [Rational(1), Rational(3, 2), Rational(11, 6)]


def test_all_sequences_return_rational():
    for result in [
        sequences.fibonacci(3),
        sequences.triangular(3),
        sequences.square(3),
        sequences.cube(3),
        sequences.perfect(1),
        sequences.prime(3),
        sequences.geometric(3),
        sequences.harmonic(3),
    ]:
        for item in result:
            assert isinstance(item, Rational)


def test_no_negative_counts_accepted():
    all_funcs = [sequences.fibonacci, sequences.triangular, sequences.square, sequences.cube, sequences.perfect, sequences.prime]
    for func in all_funcs:
        with pytest.raises(ValueError):
            func(-5)


def test_harmonic_zero():
    assert sequences.harmonic(0) == []


def test_prime_two():
    assert sequences.prime(2) == [Rational(2), Rational(3)]
def test_perfect_zero():
    assert sequences.perfect(0) == []


def test_perfect_safety_bound():
    # Test the safety bound p > 31 in perfect() - request more perfect numbers than can be generated
    # This triggers line 131: if p > 31 and len(perfect_numbers) < count: break
    # Only 8 perfect numbers are known within reasonable bounds (p up to 31)
    result = sequences.perfect(10)
    # Should return only the 8 perfect numbers it can generate
    assert len(result) == 8
    # Verify first few are correct
    assert result[0] == Rational(6)
    assert result[1] == Rational(28)
    assert result[2] == Rational(496)
    assert result[3] == Rational(8128)


def test_is_prime_less_than_two():
    # Test _is_prime for n < 2 (line 138)
    # _is_prime is a private function but we can test it via prime() with count=0 which doesn't use it
    # Or test the behavior through the prime function's internal use of _is_prime
    # The _is_prime function is tested implicitly, but let's test the boundary
    from base60lab.sequences import _is_prime
    assert _is_prime(0) is False
    assert _is_prime(1) is False
    assert _is_prime(-1) is False


def test_prime_zero():
    assert sequences.prime(0) == []


def test_geometric_negative_count_raises():
    with pytest.raises(ValueError, match="count must be non-negative"):
        sequences.geometric(-1)


def test_harmonic_negative_count_raises():
    with pytest.raises(ValueError, match="count must be non-negative"):
        sequences.harmonic(-1)