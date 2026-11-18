"""Base-60 engine — exact rational arithmetic and representation for sexagesimal.

Known truths encoded here (from PLAN.md mathematical foundations):
  - Base factorisation: 60 = 2² × 3 × 5
  - A rational p/q terminates in base 60 iff q's prime factors are only 2, 3 and/or 5.
  - 360 = 6 × 60 = 30 × 12 (full circle in degrees)
  - Digit symbols: 0-9 then A-Z (or 0-59 as place values); we use 0-9, A-Z for values 10-35
    and two-position sexagesimal places for values 0-59.
  - Fractional point: ";" (sexagesimal fractional separator convention)

Base-60 is NOT treated as fully known: relationships that experiments may
reveal are registered in the core unknowns registry and can be amended in
place as new truths are discovered.
"""

from __future__ import annotations

from typing import Any

from ..core.rational import Rational
from ..core.types import BaseNumber, Expression, Function, Notation, NotationSystem
from ..core.unknowns import UnknownEntry, UnknownsRegistry


class Base60Engine:
    """Engine for base-60 (sexagesimal) representation and arithmetic.

    Known truths:
      - Base factorisation: 60 = 2^2 × 3 × 5
      - Terminating rule: a rational terminates in base 60 iff its reduced
        denominator's prime factors are only 2, 3 and/or 5.
      - 360 degrees = 6 × 60 = 30 × 12 (circular subdivision)
      - Digit symbols: 0-9 then A-Z for place values 10-35 (and 0-59 per place)
      - Fractional point: ";"

    Unknowns (may be proven/refuted by experiments):
      - Whether base-60 notation reveals practical advantages for specific
        frequency ratios, geometry subdivisions, or FFT sizes.
    """

    BASE = 60
    # Digit symbols for sexagesimal places: 0-9 then A-Z (values 10-35)
    DIGITS = tuple(str(d) for d in range(10)) + tuple(chr(ord("A") + i) for i in range(26))
    FRACTIONAL_POINT = ";"
    FACTORISATION = {2: 2, 3: 1, 5: 1}

    def __init__(self, unknowns: UnknownsRegistry | None = None) -> None:
        self.unknowns = unknowns or UnknownsRegistry()
        self._register_known_truths()
        self._register_unknowns()

    # -- known truths -----------------------------------------------------

    def _register_known_truths(self) -> None:
        """Register base-60 known truths as proven entries."""
        truths = [
            UnknownEntry(
                id="base60.factorisation",
                base=60,
                category="arithmetic",
                statement="60 = 2^2 × 3 × 5",
                status="proven",
                version="1.0.0",
            ),
            UnknownEntry(
                id="base60.terminating_rule",
                base=60,
                category="fractions",
                statement="A rational terminates in base 60 iff its reduced denominator's prime factors are only 2, 3 and/or 5.",
                status="proven",
                version="1.0.0",
            ),
            UnknownEntry(
                id="base60.circle_subdivision",
                base=60,
                category="geometry",
                statement="360 degrees = 6 × 60 = 30 × 12; base-60 divides a circle into 60 parts of 6 degrees each.",
                status="proven",
                version="1.0.0",
            ),
            UnknownEntry(
                id="base60.digit_symbols",
                base=60,
                category="notation",
                statement="Base-60 place values range 0-59; digit symbols 0-9 then A-Z for values 10-35.",
                status="proven",
                version="1.0.0",
            ),
        ]
        for t in truths:
            self.unknowns.add(t)

    def _register_unknowns(self) -> None:
        """Register base-60 relationships that experiments may reveal (open/conjecture)."""
        unknowns = [
            UnknownEntry(
                id="base60.fraction.advantage_over_decimal",
                base=60,
                category="fractions",
                statement="Base-60 representation provides a practical advantage over base-10 for the majority of common fractions.",
                status="open",
                version="0.1.0",
            ),
            UnknownEntry(
                id="base60.geometry.circle_subdivision_usefulness",
                base=60,
                category="geometry",
                statement="Sexagesimal circle subdivisions (60, 120, 180, 360 parts) reveal geometric relationships not apparent in decimal degrees.",
                status="conjecture",
                version="0.1.0",
            ),
            UnknownEntry(
                id="base60.frequency.ratio_recognition",
                base=60,
                category="frequency",
                statement="Base-60 notation helps recognise relationships between rational frequency ratios and phase closure.",
                status="open",
                version="0.1.0",
            ),
            UnknownEntry(
                id="base60.fft.size_advantage",
                base=60,
                category="signal_processing",
                statement="FFT sizes constructed from factors 2, 3, 5 (60-smooth) perform measurably better than nearby prime lengths.",
                status="conjecture",
                version="0.1.0",
            ),
        ]
        for u in unknowns:
            self.unknowns.add(u)

    # -- conversion -------------------------------------------------------

    def from_rational(self, value: Rational) -> BaseNumber:
        """Wrap an exact rational value as a base-60 BaseNumber."""
        return BaseNumber(value=value, base=self.BASE)

    def to_rational(self, number: BaseNumber) -> Rational:
        """Extract the exact rational value (base-independent)."""
        return number.value

    def to_notation(self, number: BaseNumber) -> Notation:
        """Render a base-60 BaseNumber as sexagesimal notation."""
        return _render_rational_sexagesimal(number.value)

    def convert_from_base(self, number: BaseNumber, target_base: int) -> BaseNumber:
        """Retag a BaseNumber to base-60 (internal value is base-independent)."""
        return BaseNumber(value=number.value, base=self.BASE)

    # -- arithmetic -------------------------------------------------------

    def add(self, a: BaseNumber, b: BaseNumber) -> BaseNumber:
        return BaseNumber(value=a.value + b.value, base=self.BASE)

    def sub(self, a: BaseNumber, b: BaseNumber) -> BaseNumber:
        return BaseNumber(value=a.value - b.value, base=self.BASE)

    def mul(self, a: BaseNumber, b: BaseNumber) -> BaseNumber:
        return BaseNumber(value=a.value * b.value, base=self.BASE)

    def div(self, a: BaseNumber, b: BaseNumber) -> BaseNumber:
        return BaseNumber(value=a.value / b.value, base=self.BASE)

    def reciprocal(self, denominator: int) -> BaseNumber:
        return self.from_rational(Rational(1, denominator))

    def neg(self, a: BaseNumber) -> BaseNumber:
        return BaseNumber(value=-a.value, base=self.BASE)

    def pow(self, a: BaseNumber, exponent: int) -> BaseNumber:
        return BaseNumber(value=a.value ** exponent, base=self.BASE)

    # -- functions --------------------------------------------------------

    def function(self, name: str) -> Function:
        funcs = {
            "add": Function("add", 2, evaluate=lambda x, y: self.add(x, y).value),
            "sub": Function("sub", 2, evaluate=lambda x, y: self.sub(x, y).value),
            "mul": Function("mul", 2, evaluate=lambda x, y: self.mul(x, y).value),
            "div": Function("div", 2, evaluate=lambda x, y: self.div(x, y).value),
        }
        if name not in funcs:
            raise KeyError(f"function {name!r} not available in base-60 engine")
        return funcs[name]

    # -- introspection ----------------------------------------------------

    def terminating_denominators(self, limit: int = 360) -> list[int]:
        """Return denominators 1..limit whose reciprocals terminate in base 60."""
        return [
            d for d in range(1, limit + 1)
            if Rational(1, d).is_terminating_in_base(self.BASE)
        ]

    def repeating_period(self, denominator: int) -> int | None:
        """Return the repeating period of 1/denominator in base 60, or None if terminating."""
        return Rational(1, denominator).repeating_period_in_base(self.BASE)

    def describe(self) -> dict[str, Any]:
        return {
            "base": self.BASE,
            "name": "sexagesimal",
            "factorisation": self.FACTORISATION,
            "digit_symbols": self.DIGITS,
            "fractional_point": self.FRACTIONAL_POINT,
            "known_truths_complete": False,
            "unknowns_count": len(self.unknowns),
            "open_unknowns": len(self.unknowns.list_by_status("open")),
            "conjecture_unknowns": len(self.unknowns.list_by_status("conjecture")),
        }


def _render_rational_sexagesimal(value: Rational) -> Notation:
    """Render an exact rational as sexagesimal (base-60) notation.

    Integer part in base 60, fractional part as successive sexagesimal places
    (each 0-59).  Repeating periods are detected via long division remainders.
    """
    num = value.numerator
    den = value.denominator
    sign = "-" if num < 0 else ""
    num = abs(num)

    integer_part = num // den
    remainder = num % den

    # ---- integer part in base 60 ----
    if integer_part == 0:
        int_digits = ["0"]
    else:
        parts: list[str] = []
        n = integer_part
        while n > 0:
            n, rem = divmod(n, 60)
            parts.append(_sexagesimal_digit(rem))
        int_digits = list(reversed(parts))
    int_text = ",".join(int_digits) if len(int_digits) > 1 else int_digits[0]
    if remainder == 0:
        text = f"{sign}{int_text}"
        return Notation(
            base=60,
            digits=tuple(_sexagesimal_digit(i) for i in range(60)),
            fractional_point=";",
            text=text,
            repeating=None,
        )

    # ---- fractional part: long division in base 60 ----
    frac_digits: list[str] = []
    seen: dict[int, int] = {}
    r = remainder
    repeating_start: int | None = None

    while r != 0 and r not in seen:
        seen[r] = len(frac_digits)
        r *= 60
        digit = r // den
        frac_digits.append(_sexagesimal_digit(digit))
        r = r % den

    if r in seen:
        repeating_start = seen[r]
        non_rep = "".join(frac_digits[:repeating_start])
        rep = "".join(frac_digits[repeating_start:])
        text = f"{sign}{int_text};{non_rep}({rep})"
    else:
        text = f"{sign}{int_text};" + "".join(frac_digits)

    return Notation(
        base=60,
        digits=tuple(_sexagesimal_digit(i) for i in range(60)),
        fractional_point=";",
        text=text,
        repeating=repeating_start,
    )


def _sexagesimal_digit(value: int) -> str:
    """Return the symbol for a single sexagesimal place value (0-59)."""
    if not 0 <= value <= 59:
        raise ValueError(f"sexagesimal digit must be 0-59, got {value}")
    if value < 10:
        return str(value)
    # Values 10-35 -> A-Z; 36-59 -> two-symbol fallback
    if value < 36:
        return chr(ord("A") + value - 10)
    # For 36-59, use a compact representation
    return f"<{value}>"


__all__ = ["Base60Engine"]
