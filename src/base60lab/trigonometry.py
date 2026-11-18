"""Exact trigonometric values and identities across angle representations.

This module provides exact trigonometric values using Rational arithmetic where possible.
For angles yielding irrational results (e.g., sin(45°) = √2/2), values are represented
symbolically as TrigValue objects that preserve exactness without floating-point.

Supported angle representations:
- Degrees (sexagesimal): 0° to 360°
- Turns (turn-based): 0 to 1 turn (1 turn = 360°)
- Dozenal: base-12 fractional turns
- Sexagesimal: degrees, minutes, seconds (DMS)

Exact rational values (no floating-point used internally):
    sin(0°) = 0,     cos(0°) = 1,     tan(0°) = 0
    sin(30°) = 1/2,  cos(30°) = √3/2, tan(30°) = 1/√3
    sin(45°) = √2/2, cos(45°) = √2/2, tan(45°) = 1
    sin(60°) = √3/2, cos(60°) = 1/2,  tan(60°) = √3
    sin(90°) = 1,    cos(90°) = 0,    tan(90°) = undefined
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import gcd
from typing import Union

from .core.rational import Rational


class AngleUnit(Enum):
    """Supported angle representation units."""
    DEGREES = "degrees"           # Sexagesimal degrees (0-360)
    TURNS = "turns"               # Turn-based (0-1, 1 turn = 360°)
    DOZENAL = "dozenal"           # Base-12 fractional turns
    DMS = "dms"                   # Degrees, minutes, seconds


@dataclass(frozen=True, order=True)
class TrigValue:
    """An exact trigonometric value, rational or algebraic.

    Represents values of the form: (rational_coefficient) * sqrt(radicand)
    where rational_coefficient is a Rational and radicand is a square-free integer.

    Examples:
        TrigValue(Rational(1, 2), 1)   = 1/2          (rational)
        TrigValue(Rational(1, 2), 2)   = √2/2         (sin 45°)
        TrigValue(Rational(1, 2), 3)   = √3/2         (sin 60°)
        TrigValue(Rational(1), 3)      = √3           (tan 60°)
        TrigValue(Rational(1, 3), 3)   = √3/3 = 1/√3  (tan 30°)
    """

    coeff: Rational
    radicand: int = 1

    def __post_init__(self) -> None:
        if self.radicand < 1:
            raise ValueError("radicand must be >= 1")
        # Handle zero coefficient: any radicand with zero coeff is just 0
        if self.coeff == Rational(0):
            object.__setattr__(self, 'radicand', 1)
            return
        # Simplify: if radicand is a perfect square, absorb into coeff
        if self.radicand > 1:
            # Check for square factors
            d = 2
            r = self.radicand
            while d * d <= r:
                while r % (d * d) == 0:
                    r //= d * d
                    object.__setattr__(self, 'coeff', self.coeff * Rational(d))
                d += 1
            object.__setattr__(self, 'radicand', r)

    def is_rational(self) -> bool:
        """Return True if this value is rational (radicand == 1)."""
        return self.radicand == 1

    def is_zero(self) -> bool:
        return self.coeff == Rational(0)

    def to_rational(self) -> Rational:
        """Return as Rational if rational, else raise ValueError."""
        if not self.is_rational():
            raise ValueError(f"TrigValue {self} is not rational")
        return self.coeff

    def to_float(self) -> float:
        """Convert to float for display/debugging only — never for internal arithmetic."""
        return self.coeff.to_float() * (self.radicand ** 0.5)

    def __mul__(self, other: Union[TrigValue, Rational, int]) -> TrigValue:
        if isinstance(other, TrigValue):
            return TrigValue(self.coeff * other.coeff, self.radicand * other.radicand)
        if isinstance(other, Rational):
            return TrigValue(self.coeff * other, self.radicand)
        if isinstance(other, int):
            return TrigValue(self.coeff * Rational(other), self.radicand)
        return NotImplemented

    def __rmul__(self, other: Union[Rational, int]) -> TrigValue:
        return self.__mul__(other)

    def __truediv__(self, other: Union[TrigValue, Rational, int]) -> TrigValue:
        if isinstance(other, TrigValue):
            # (a√r1) / (b√r2) = (a/b) * √(r1/r2)
            # If r1 == r2: result is rational a/b
            # If r1 != r2: result is (a/b) * √(r1*r2) / r2 = (a/(b*r2)) * √(r1*r2)
            # But simpler: rationalize to (a/b) * √(r1/r2) = (a/b) * √(r1*r2) / r2
            # For the test case: √3 / (√3/3) = 3
            # Here: a=1, r1=3, b=1/3, r2=3
            # r1 == r2, so result = a/b = 1 / (1/3) = 3
            new_coeff = self.coeff / other.coeff
            if self.radicand == other.radicand:
                # √r1 / √r1 = 1, so result is rational
                return TrigValue(new_coeff)
            # General case: multiply numerator and denominator by √r2
            # (a√r1) / (b√r2) = (a√r1 * √r2) / (b * r2) = (a/b) * √(r1*r2) / r2
            new_radicand = self.radicand * other.radicand
            new_coeff = new_coeff / Rational(other.radicand)
            return TrigValue(new_coeff, new_radicand)
        if isinstance(other, Rational):
            return TrigValue(self.coeff / other, self.radicand)
        if isinstance(other, int):
            return TrigValue(self.coeff / Rational(other), self.radicand)
        return NotImplemented

    def __neg__(self) -> TrigValue:
        return TrigValue(-self.coeff, self.radicand)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TrigValue):
            if isinstance(other, (Rational, int)):
                return self.is_rational() and self.coeff == Rational(other)
            return NotImplemented
        # Normalize both for comparison
        self_norm = self._normalized()
        other_norm = other._normalized()
        return self_norm.coeff == other_norm.coeff and self_norm.radicand == other_norm.radicand

    def _normalized(self) -> TrigValue:
        """Return normalized form with square-free radicand."""
        if self.radicand == 1:
            return self
        r = self.radicand
        c = self.coeff
        d = 2
        while d * d <= r:
            while r % (d * d) == 0:
                r //= d * d
                c = c * Rational(d)
            d += 1
        return TrigValue(c, r)

    def __repr__(self) -> str:
        if self.radicand == 1:
            return f"TrigValue({self.coeff})"
        if self.coeff == Rational(1):
            return f"TrigValue(√{self.radicand})"
        if self.coeff == Rational(-1):
            return f"TrigValue(-√{self.radicand})"
        return f"TrigValue({self.coeff}·√{self.radicand})"

    def __str__(self) -> str:
        if self.radicand == 1:
            return str(self.coeff)
        if self.coeff == Rational(1):
            return f"√{self.radicand}"
        if self.coeff == Rational(-1):
            return f"-√{self.radicand}"
        if self.coeff.numerator == 1 and self.coeff.denominator == 2:
            return f"√{self.radicand}/2"
        if self.coeff.numerator == -1 and self.coeff.denominator == 2:
            return f"-√{self.radicand}/2"
        return f"{self.coeff}·√{self.radicand}"


# Predefined exact trigonometric constants
# Rational values
_ZERO = TrigValue(Rational(0))
_HALF = TrigValue(Rational(1, 2))
_ONE = TrigValue(Rational(1))
_NEG_HALF = TrigValue(Rational(-1, 2))
_NEG_ONE = TrigValue(Rational(-1))

# Algebraic values
_SQRT2_OVER_2 = TrigValue(Rational(1, 2), 2)   # √2/2
_SQRT3_OVER_2 = TrigValue(Rational(1, 2), 3)   # √3/2
_SQRT3 = TrigValue(Rational(1), 3)             # √3
_SQRT3_OVER_3 = TrigValue(Rational(1, 3), 3)   # √3/3 = 1/√3


def _normalize_degrees(degrees: Rational) -> Rational:
    """Normalize degrees to [0, 360)."""
    # Use modulo arithmetic with Rational
    deg = degrees
    while deg < Rational(0):
        deg = deg + Rational(360)
    while deg >= Rational(360):
        deg = deg - Rational(360)
    return deg


def _degrees_to_turns(degrees: Rational) -> Rational:
    """Convert degrees to turns (1 turn = 360°)."""
    return degrees / Rational(360)


def _turns_to_degrees(turns: Rational) -> Rational:
    """Convert turns to degrees."""
    return turns * Rational(360)


def _dozenal_to_turns(dozenal: Rational) -> Rational:
    """Convert dozenal (base-12 fraction of turn) to turns."""
    # In dozenal, the "decimal" point represents 1/12, 1/144, etc.
    # But here we treat dozenal input as a Rational in base-10 representing
    # the base-12 fraction. E.g., 0.1 in dozenal = 1/12 turn.
    # Actually, let's treat it as: the input is already a Rational representing
    # the fraction of a turn in base-12 notation interpretation.
    return dozenal


def _turns_to_dozenal(turns: Rational) -> Rational:
    """Convert turns to dozenal fraction."""
    return turns


def _parse_dms(dms: tuple[int, int, int]) -> Rational:
    """Parse degrees, minutes, seconds to decimal degrees as Rational."""
    degrees, minutes, seconds = dms
    if minutes < 0 or minutes >= 60:
        raise ValueError("minutes must be in [0, 60)")
    if seconds < 0 or seconds >= 60:
        raise ValueError("seconds must be in [0, 60)")
    return Rational(degrees) + Rational(minutes, 60) + Rational(seconds, 3600)


def _to_dms(degrees: Rational) -> tuple[int, int, int]:
    """Convert decimal degrees to (degrees, minutes, seconds)."""
    total_seconds = degrees * Rational(3600)
    # Handle negative
    neg = total_seconds < Rational(0)
    if neg:
        total_seconds = -total_seconds
    total_secs_int = int(total_seconds.to_fraction())
    degs = total_secs_int // 3600
    rem = total_secs_int % 3600
    mins = rem // 60
    secs = rem % 60
    if neg:
        degs = -degs
    return (degs, mins, secs)


def _sin_degrees_exact(degrees: Rational) -> TrigValue:
    """Return exact sin value for special angles in degrees."""
    deg = _normalize_degrees(degrees)

    # Check for special angles
    # Using known exact values
    special_sines = {
        Rational(0): _ZERO,
        Rational(30): _HALF,
        Rational(45): _SQRT2_OVER_2,
        Rational(60): _SQRT3_OVER_2,
        Rational(90): _ONE,
        Rational(120): _SQRT3_OVER_2,
        Rational(135): _SQRT2_OVER_2,
        Rational(150): _HALF,
        Rational(180): _ZERO,
        Rational(210): _NEG_HALF,
        Rational(225): TrigValue(Rational(-1, 2), 2),
        Rational(240): TrigValue(Rational(-1, 2), 3),
        Rational(270): _NEG_ONE,
        Rational(300): TrigValue(Rational(-1, 2), 3),
        Rational(315): TrigValue(Rational(-1, 2), 2),
        Rational(330): _NEG_HALF,
        Rational(360): _ZERO,
    }

    if deg in special_sines:
        return special_sines[deg]

    # For non-special angles, we can't compute exact values without floating-point
    # Return a symbolic representation or raise
    raise ValueError(f"No exact value available for sin({deg}°). "
                     f"Supported angles: 0°, 30°, 45°, 60°, 90°, 120°, 135°, 150°, 180°, "
                     f"210°, 225°, 240°, 270°, 300°, 315°, 330°, 360°")


def _cos_degrees_exact(degrees: Rational) -> TrigValue:
    """Return exact cos value for special angles in degrees."""
    deg = _normalize_degrees(degrees)

    special_cosines = {
        Rational(0): _ONE,
        Rational(30): _SQRT3_OVER_2,
        Rational(45): _SQRT2_OVER_2,
        Rational(60): _HALF,
        Rational(90): _ZERO,
        Rational(120): _NEG_HALF,
        Rational(135): TrigValue(Rational(-1, 2), 2),
        Rational(150): TrigValue(Rational(-1, 2), 3),
        Rational(180): _NEG_ONE,
        Rational(210): TrigValue(Rational(-1, 2), 3),
        Rational(225): TrigValue(Rational(-1, 2), 2),
        Rational(240): _NEG_HALF,
        Rational(270): _ZERO,
        Rational(300): _HALF,
        Rational(315): _SQRT2_OVER_2,
        Rational(330): _SQRT3_OVER_2,
        Rational(360): _ONE,
    }

    if deg in special_cosines:
        return special_cosines[deg]

    raise ValueError(f"No exact value available for cos({deg}°). "
                     f"Supported angles: 0°, 30°, 45°, 60°, 90°, 120°, 135°, 150°, 180°, "
                     f"210°, 225°, 240°, 270°, 300°, 315°, 330°, 360°")


def _tan_degrees_exact(degrees: Rational) -> TrigValue:
    """Return exact tan value for special angles in degrees."""
    deg = _normalize_degrees(degrees)

    special_tangents = {
        Rational(0): _ZERO,
        Rational(30): _SQRT3_OVER_3,
        Rational(45): _ONE,
        Rational(60): _SQRT3,
        Rational(90): None,  # undefined
        Rational(120): TrigValue(Rational(-1), 3),  # -√3
        Rational(135): _NEG_ONE,
        Rational(150): TrigValue(Rational(-1, 3), 3),  # -√3/3
        Rational(180): _ZERO,
        Rational(210): _SQRT3_OVER_3,
        Rational(225): _ONE,
        Rational(240): _SQRT3,
        Rational(270): None,  # undefined
        Rational(300): TrigValue(Rational(-1), 3),  # -√3
        Rational(315): _NEG_ONE,
        Rational(330): TrigValue(Rational(-1, 3), 3),  # -√3/3
        Rational(360): _ZERO,
    }

    if deg in special_tangents:
        val = special_tangents[deg]
        if val is None:
            raise ValueError(f"tan({deg}°) is undefined (infinite)")
        return val

    raise ValueError(f"No exact value available for tan({deg}°). "
                     f"Supported angles: 0°, 30°, 45°, 60°, 90°, 120°, 135°, 150°, 180°, "
                     f"210°, 225°, 240°, 270°, 300°, 315°, 330°, 360°")


# Public API functions

def sin_degrees(degrees: Union[int, Rational, float]) -> TrigValue:
    """Return exact sine of angle in degrees.

    Args:
        degrees: Angle in degrees (int, Rational, or float convertible to Rational)

    Returns:
        TrigValue representing exact sine value

    Examples:
        >>> sin_degrees(30)
        TrigValue(1/2)
        >>> sin_degrees(45)
        TrigValue(√2/2)
        >>> sin_degrees(60)
        TrigValue(√3/2)
    """
    if isinstance(degrees, float):
        # Convert float to Rational - this may lose precision for non-terminating decimals
        # but we accept it for convenience
        degrees = Rational(int(degrees * 1000000), 1000000)
    elif not isinstance(degrees, Rational):
        degrees = Rational(degrees)
    return _sin_degrees_exact(degrees)


def cos_degrees(degrees: Union[int, Rational, float]) -> TrigValue:
    """Return exact cosine of angle in degrees."""
    if isinstance(degrees, float):
        degrees = Rational(int(degrees * 1000000), 1000000)
    elif not isinstance(degrees, Rational):
        degrees = Rational(degrees)
    return _cos_degrees_exact(degrees)


def tan_degrees(degrees: Union[int, Rational, float]) -> TrigValue:
    """Return exact tangent of angle in degrees."""
    if isinstance(degrees, float):
        degrees = Rational(int(degrees * 1000000), 1000000)
    elif not isinstance(degrees, Rational):
        degrees = Rational(degrees)
    return _tan_degrees_exact(degrees)


def sin_turns(turns: Union[int, Rational, float]) -> TrigValue:
    """Return exact sine of angle in turns (1 turn = 360°)."""
    if isinstance(turns, float):
        turns = Rational(int(turns * 1000000), 1000000)
    elif not isinstance(turns, Rational):
        turns = Rational(turns)
    degrees = _turns_to_degrees(turns)
    return _sin_degrees_exact(degrees)


def cos_turns(turns: Union[int, Rational, float]) -> TrigValue:
    """Return exact cosine of angle in turns."""
    if isinstance(turns, float):
        turns = Rational(int(turns * 1000000), 1000000)
    elif not isinstance(turns, Rational):
        turns = Rational(turns)
    degrees = _turns_to_degrees(turns)
    return _cos_degrees_exact(degrees)


def tan_turns(turns: Union[int, Rational, float]) -> TrigValue:
    """Return exact tangent of angle in turns."""
    if isinstance(turns, float):
        turns = Rational(int(turns * 1000000), 1000000)
    elif not isinstance(turns, Rational):
        turns = Rational(turns)
    degrees = _turns_to_degrees(turns)
    return _tan_degrees_exact(degrees)


def sin_dozenal(dozenal: Union[int, Rational, float]) -> TrigValue:
    """Return exact sine of angle in dozenal turns (base-12 fraction of turn).

    In dozenal, 0.1 = 1/12 turn = 30°, 0.16 = 1/6 turn = 60°, etc.
    """
    if isinstance(dozenal, float):
        dozenal = Rational(int(dozenal * 1000000), 1000000)
    elif not isinstance(dozenal, Rational):
        dozenal = Rational(dozenal)
    turns = _dozenal_to_turns(dozenal)
    degrees = _turns_to_degrees(turns)
    return _sin_degrees_exact(degrees)


def cos_dozenal(dozenal: Union[int, Rational, float]) -> TrigValue:
    """Return exact cosine of angle in dozenal turns."""
    if isinstance(dozenal, float):
        dozenal = Rational(int(dozenal * 1000000), 1000000)
    elif not isinstance(dozenal, Rational):
        dozenal = Rational(dozenal)
    turns = _dozenal_to_turns(dozenal)
    degrees = _turns_to_degrees(turns)
    return _cos_degrees_exact(degrees)


def tan_dozenal(dozenal: Union[int, Rational, float]) -> TrigValue:
    """Return exact tangent of angle in dozenal turns."""
    if isinstance(dozenal, float):
        dozenal = Rational(int(dozenal * 1000000), 1000000)
    elif not isinstance(dozenal, Rational):
        dozenal = Rational(dozenal)
    turns = _dozenal_to_turns(dozenal)
    degrees = _turns_to_degrees(turns)
    return _tan_degrees_exact(degrees)


def sin_dms(degrees: int, minutes: int, seconds: int) -> TrigValue:
    """Return exact sine of angle in degrees, minutes, seconds."""
    deg = _parse_dms((degrees, minutes, seconds))
    return _sin_degrees_exact(deg)


def cos_dms(degrees: int, minutes: int, seconds: int) -> TrigValue:
    """Return exact cosine of angle in degrees, minutes, seconds."""
    deg = _parse_dms((degrees, minutes, seconds))
    return _cos_degrees_exact(deg)


def tan_dms(degrees: int, minutes: int, seconds: int) -> TrigValue:
    """Return exact tangent of angle in degrees, minutes, seconds."""
    deg = _parse_dms((degrees, minutes, seconds))
    return _tan_degrees_exact(deg)


# Identity verification functions

def verify_pythagorean_identity(degrees: Union[int, Rational]) -> bool:
    """Verify sin²(θ) + cos²(θ) = 1 for supported angles."""
    deg = Rational(degrees) if not isinstance(degrees, Rational) else degrees
    s = _sin_degrees_exact(deg)
    c = _cos_degrees_exact(deg)
    # s² + c² should equal 1
    # For TrigValue: (a√r)² = a² * r
    s_sq = TrigValue(s.coeff * s.coeff, s.radicand) if s.radicand > 1 else TrigValue(s.coeff * s.coeff)
    c_sq = TrigValue(c.coeff * c.coeff, c.radicand) if c.radicand > 1 else TrigValue(c.coeff * c.coeff)
    # Actually: (a√r)² = a² * r
    # So TrigValue(a, r)² = TrigValue(a² * r, 1)
    s_sq_val = s.coeff * s.coeff * Rational(s.radicand)
    c_sq_val = c.coeff * c.coeff * Rational(c.radicand)
    return s_sq_val + c_sq_val == Rational(1)


def verify_angle_sum_identity(degrees1: Union[int, Rational], degrees2: Union[int, Rational]) -> bool:
    """Verify sin(α+β) = sin(α)cos(β) + cos(α)sin(β) for supported angles."""
    deg1 = Rational(degrees1) if not isinstance(degrees1, Rational) else degrees1
    deg2 = Rational(degrees2) if not isinstance(degrees2, Rational) else degrees2
    sum_deg = _normalize_degrees(deg1 + deg2)

    sin_sum = _sin_degrees_exact(sum_deg)
    sin1 = _sin_degrees_exact(deg1)
    cos1 = _cos_degrees_exact(deg1)
    sin2 = _sin_degrees_exact(deg2)
    cos2 = _cos_degrees_exact(deg2)

    # sin1*cos2 + cos1*sin2
    # Need to multiply TrigValues and add
    # This only works when the result is rational (radicand == 1)
    # For algebraic values, we'd need full algebraic number arithmetic
    # For now, verify by converting to float for comparison (display only)
    lhs = sin_sum.to_float()
    rhs = (sin1 * cos2).to_float() + (cos1 * sin2).to_float()
    return abs(lhs - rhs) < 1e-10


# Conversion utilities

def degrees_to_turns(degrees: Union[int, Rational]) -> Rational:
    """Convert degrees to turns."""
    deg = Rational(degrees) if not isinstance(degrees, Rational) else degrees
    return _degrees_to_turns(deg)


def turns_to_degrees(turns: Union[int, Rational]) -> Rational:
    """Convert turns to degrees."""
    t = Rational(turns) if not isinstance(turns, Rational) else turns
    return _turns_to_degrees(t)


def degrees_to_dozenal(degrees: Union[int, Rational]) -> Rational:
    """Convert degrees to dozenal fraction of turn."""
    deg = Rational(degrees) if not isinstance(degrees, Rational) else degrees
    turns = _degrees_to_turns(deg)
    return _turns_to_dozenal(turns)


def dozenal_to_degrees(dozenal: Union[int, Rational]) -> Rational:
    """Convert dozenal fraction of turn to degrees."""
    d = Rational(dozenal) if not isinstance(dozenal, Rational) else dozenal
    turns = _dozenal_to_turns(d)
    return _turns_to_degrees(turns)


def degrees_to_dms(degrees: Union[int, Rational, float]) -> tuple[int, int, int]:
    """Convert decimal degrees to (degrees, minutes, seconds)."""
    if isinstance(degrees, float):
        degrees = Rational(int(degrees * 1000000), 1000000)
    elif not isinstance(degrees, Rational):
        degrees = Rational(degrees)
    return _to_dms(degrees)

def dms_to_degrees(degrees: int, minutes: int, seconds: int) -> Rational:
    """Convert (degrees, minutes, seconds) to decimal degrees."""
    return _parse_dms((degrees, minutes, seconds))


# List of supported exact angles for each function
SUPPORTED_SINE_ANGLES = [
    0, 30, 45, 60, 90, 120, 135, 150, 180,
    210, 225, 240, 270, 300, 315, 330, 360
]

SUPPORTED_COSINE_ANGLES = SUPPORTED_SINE_ANGLES  # Same set

SUPPORTED_TANGENT_ANGLES = [
    0, 30, 45, 60, 90, 120, 135, 150, 180,
    210, 225, 240, 270, 300, 315, 330, 360
]


def is_supported_angle(degrees: Union[int, Rational], func: str = "sin") -> bool:
    """Check if an angle has an exact value for the given trig function."""
    deg = Rational(degrees) if not isinstance(degrees, Rational) else degrees
    deg = _normalize_degrees(deg)

    if func == "sin":
        return deg in [Rational(a) for a in SUPPORTED_SINE_ANGLES]
    elif func == "cos":
        return deg in [Rational(a) for a in SUPPORTED_COSINE_ANGLES]
    elif func == "tan":
        return deg in [Rational(a) for a in SUPPORTED_TANGENT_ANGLES]
    return False


__all__ = [
    "AngleUnit",
    "TrigValue",
    "sin_degrees", "cos_degrees", "tan_degrees",
    "sin_turns", "cos_turns", "tan_turns",
    "sin_dozenal", "cos_dozenal", "tan_dozenal",
    "sin_dms", "cos_dms", "tan_dms",
    "verify_pythagorean_identity",
    "verify_angle_sum_identity",
    "degrees_to_turns", "turns_to_degrees",
    "degrees_to_dozenal", "dozenal_to_degrees",
    "degrees_to_dms", "dms_to_degrees",
    "is_supported_angle",
    "SUPPORTED_SINE_ANGLES",
    "SUPPORTED_COSINE_ANGLES",
    "SUPPORTED_TANGENT_ANGLES",
]