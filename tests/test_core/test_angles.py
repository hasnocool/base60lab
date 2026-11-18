"""Tests for angles module: exact rational degrees/turns/radians conversions."""

import pytest

from base60lab.angles import (
    degrees_to_radians,
    degrees_to_turns,
    normalize_degrees,
    normalize_radians,
    normalize_turns,
    radians_to_degrees,
    radians_to_turns,
    subdivide_turn,
    turn_to_degrees,
    turn_to_radians,
)
from base60lab.core.rational import Rational


def test_turn_to_degrees_quarter_turn_is_exact_90():
    assert turn_to_degrees(Rational(1, 4)) == Rational(90)


def test_turn_to_degrees_half_turn():
    assert turn_to_degrees(Rational(1, 2)) == Rational(180)


def test_turn_to_degrees_zero():
    assert turn_to_degrees(Rational(0)) == Rational(0)


def test_turn_to_degrees_negative():
    assert turn_to_degrees(Rational(-1, 4)) == Rational(-90)


def test_degrees_to_turns_round_trip():
    assert degrees_to_turns(turn_to_degrees(Rational(1, 4))) == Rational(1, 4)


def test_turns_to_radians_round_trip():
    assert radians_to_turns(turn_to_radians(Rational(1, 4))) == Rational(1, 4)


def test_full_circle_turn_equals_360_degrees_and_2pi_radians():
    assert turn_to_degrees(Rational(1)) == Rational(360)
    assert degrees_to_turns(Rational(360)) == Rational(1)
    assert turn_to_radians(Rational(1)) == Rational(2)
    assert radians_to_turns(Rational(2)) == Rational(1)


def test_degrees_to_radians_and_back_exact():
    assert radians_to_degrees(degrees_to_radians(Rational(90))) == Rational(90)
    assert degrees_to_radians(radians_to_degrees(Rational(1, 2))) == Rational(1, 2)


def test_conversions_return_rational_not_float():
    result = turn_to_degrees(Rational(1, 4))
    assert isinstance(result, Rational)
    assert not isinstance(result, float)


def test_subdivide_turn_sexagesimal_6x60():
    result = subdivide_turn(6, 60)
    assert result["degrees_per_part"] == Rational(60)
    assert result["degrees_per_subpart"] == Rational(1)
    assert Rational(6) * Rational(60) == Rational(360)


def test_subdivide_turn_duodecimal_30x12():
    result = subdivide_turn(30, 12)
    assert result["degrees_per_part"] == Rational(12)
    assert result["degrees_per_subpart"] == Rational(1)
    assert Rational(30) * Rational(12) == Rational(360)


def test_subdivide_turn_rejects_nonpositive():
    with pytest.raises(ValueError):
        subdivide_turn(0, 60)
    with pytest.raises(ValueError):
        subdivide_turn(6, 0)


def test_normalize_turns_wraps_negative_to_positive():
    assert normalize_turns(Rational(-1, 4)) == Rational(3, 4)


def test_normalize_degrees_wraps_above_full_circle():
    assert normalize_degrees(Rational(400)) == Rational(40)


def test_normalize_radians_wraps_above_full_circle():
    assert normalize_radians(Rational(3)) == Rational(1)
