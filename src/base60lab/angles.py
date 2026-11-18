"""Angles module: degrees, turns and radians with exact rational arithmetic.

All internal arithmetic uses exact rational numbers. The display base is a
presentation choice only; it never affects the underlying value and can never
introduce rounding errors.

Circle subdivisions:
- 1 turn = 360 degrees = 6*60 = 30*12 degrees = 2*pi radians
"""

from __future__ import annotations

from .core.rational import Rational


DEGREES_PER_TURN = Rational(360)
TURNS_PER_CIRCLE = Rational(1)
RADIANS_PER_TURN = Rational(2)  # exact coefficient of pi: 1 turn == 2*pi


def _as_rational(value: Rational) -> Rational:
    if isinstance(value, Rational):
        return value
    return Rational(value)


def turn_to_degrees(turns: Rational) -> Rational:
    turns = _as_rational(turns)
    return turns * DEGREES_PER_TURN


def degrees_to_turns(degrees: Rational) -> Rational:
    degrees = _as_rational(degrees)
    return degrees / DEGREES_PER_TURN


def turn_to_radians(turns: Rational) -> Rational:
    turns = _as_rational(turns)
    return turns * RADIANS_PER_TURN


def radians_to_turns(radians: Rational) -> Rational:
    radians = _as_rational(radians)
    return radians / RADIANS_PER_TURN


def degrees_to_radians(degrees: Rational) -> Rational:
    degrees = _as_rational(degrees)
    return degrees * (RADIANS_PER_TURN / DEGREES_PER_TURN)


def radians_to_degrees(radians: Rational) -> Rational:
    radians = _as_rational(radians)
    return radians * (DEGREES_PER_TURN / RADIANS_PER_TURN)


def subdivide_turn(parts: int, subparts: int = 1) -> dict:
    if parts < 1 or subparts < 1:
        raise ValueError("parts and subparts must be positive")
    total = parts * subparts
    return {
        "parts": Rational(parts),
        "subparts": Rational(subparts),
        "turn_per_part": Rational(1, parts),
        "turn_per_subpart": Rational(1, total),
        "degrees_per_part": DEGREES_PER_TURN / parts,
        "degrees_per_subpart": DEGREES_PER_TURN / total,
    }


def normalize_turns(turns: Rational) -> Rational:
    turns = _as_rational(turns)
    f = turns.to_fraction()
    n = f.numerator
    d = f.denominator
    whole = n // d
    rem_num = n - whole * d
    return Rational(rem_num, d)


def normalize_degrees(degrees: Rational) -> Rational:
    degrees = _as_rational(degrees)
    turns = normalize_turns(degrees_to_turns(degrees))
    return turn_to_degrees(turns)


def normalize_radians(radians: Rational) -> Rational:
    radians = _as_rational(radians)
    turns = normalize_turns(radians_to_turns(radians))
    return turn_to_radians(turns)


__all__ = [
    "Rational",
    "DEGREES_PER_TURN",
    "TURNS_PER_CIRCLE",
    "RADIANS_PER_TURN",
    "turn_to_degrees",
    "degrees_to_turns",
    "turn_to_radians",
    "radians_to_turns",
    "degrees_to_radians",
    "radians_to_degrees",
    "subdivide_turn",
    "normalize_turns",
    "normalize_degrees",
    "normalize_radians",
]
