"""Base-12 engine — exact rational arithmetic and representation for duodecimal.

Known truths encoded here:
  - Base factorisation: 12 = 2² × 3
  - A rational p/q terminates in base 12 iff q's prime factors are only 2 and/or 3.
  - Digit symbols: 0-9 then A, B (values 10, 11)
  - Fractional point: "."

Base-12 is NOT treated as fully known: relationships that experiments may
reveal are registered in the core unknowns registry and can be amended in
place as new truths are discovered.
"""

from __future__ import annotations

from typing import Any

from ..core.rational import Rational
from ..core.types import BaseNumber, Function, Notation
from ..core.unknowns import UnknownEntry, UnknownsRegistry


class Base12Engine:
    """Engine for base-12 (duodecimal) representation and arithmetic.

    Known truths:
      - Base factorisation: 12 = 2^2 × 3
      - Terminating rule: a rational terminates in base 12 iff its reduced
        denominator's prime factors are only 2 and/or 3.
      - Digit symbols: 0-9 then A, B for values 10 and 11
      - Fractional point: "."

    Unknowns (may be proven/refuted by experiments):
      - Whether base-12 notation reveals practical advantages for fractions,
        geometry, or frequency relationships vs base-10/base-60.
    """

    BASE = 12
    DIGITS = tuple(str(d) for d in range(10)) + ("A", "B")
    FRACTIONAL_POINT = "."
    FACTORISATION = {2: 2, 3: 1}

    def __init__(self, unknowns=None) -> None:
        self.unknowns = unknowns or UnknownsRegistry()
        self._register_known_truths()
        self._register_unknowns()

    # -- known truths -----------------------------------------------------

    def _register_known_truths(self):
        truths = [
            UnknownEntry(
                id="base12.factorisation",
                base=12,
                category="arithmetic",
                statement="12 = 2^2 × 3",
                status="proven",
                version="1.0.0",
            ),
            UnknownEntry(
                id="base12.terminating_rule",
                base=12,
                category="fractions",
                statement="A rational terminates in base 12 iff its reduced denominator's prime factors are only 2 and/or 3.",
                status="proven",
                version="1.0.0",
            ),
            UnknownEntry(
                id="base12.digit_symbols",
                base=12,
                category="notation",
                statement="Base-12 digit symbols are 0-9 then A (10) and B (11).",
                status="proven",
                version="1.0.0",
            ),
        ]
        for t in truths:
            self.unknowns.add(t)

    def _register_unknowns(self):
        unknowns = [
            UnknownEntry(
                id="base12.fraction.advantage_over_decimal",
                base=12,
                category="fractions",
                statement="Base-12 representation provides a practical advantage over base-10 for fractions with denominators having factors 2 and 3.",
                status="conjecture",
                version="0.1.0",
            ),
            UnknownEntry(
                id="base12.versus_base60.fraction_termination",
                base=12,
                category="fractions",
                statement="Base-60 terminates more fractions than base-12 because it adds factor 5.",
                status="proven",
                version="1.0.0",
            ),
            UnknownEntry(
                id="base12.frequency.ratio_recognition",
                base=12,
                category="frequency",
                statement="Base-12 notation helps recognise relationships between rational frequency ratios and phase closure.",
                status="open",
                version="0.1.0",
            ),
        ]
        for u in unknowns:
            self.unknowns.add(u)

    # -- conversion -------------------------------------------------------

    def from_rational(self, value):
        return BaseNumber(value=value, base=self.BASE)

    def to_rational(self, number):
        return number.value

    def to_notation(self, number):
        return _render_rational_duodecimal(number.value)

    def convert_from_base(self, number, target_base):
        return BaseNumber(value=number.value, base=self.BASE)

    # -- arithmetic -------------------------------------------------------

    def add(self, a, b):
        return BaseNumber(value=a.value + b.value, base=self.BASE)

    def sub(self, a, b):
        return BaseNumber(value=a.value - b.value, base=self.BASE)

    def mul(self, a, b):
        return BaseNumber(value=a.value * b.value, base=self.BASE)

    def div(self, a, b):
        return BaseNumber(value=a.value / b.value, base=self.BASE)

    def reciprocal(self, denominator):
        return self.from_rational(Rational(1, denominator))

    def neg(self, a):
        return BaseNumber(value=-a.value, base=self.BASE)

    def pow(self, a, exponent):
        return BaseNumber(value=a.value ** exponent, base=self.BASE)

    # -- functions --------------------------------------------------------

    def function(self, name):
        funcs = {
            "add": lambda x, y: self.add(x, y).value,
            "sub": lambda x, y: self.sub(x, y).value,
            "mul": lambda x, y: self.mul(x, y).value,
            "div": lambda x, y: self.div(x, y).value,
        }
        if name not in funcs:
            raise KeyError(f"function {name!r} not available in base-12 engine")
        return funcs[name]

    # -- introspection ----------------------------------------------------

    def terminating_denominators(self, limit=360):
        return [
            d for d in range(1, limit + 1)
            if Rational(1, d).is_terminating_in_base(self.BASE)
        ]

    def repeating_period(self, denominator):
        return Rational(1, denominator).repeating_period_in_base(self.BASE)

    def describe(self):
        return {
            "base": self.BASE,
            "name": "duodecimal",
            "factorisation": self.FACTORISATION,
            "digit_symbols": self.DIGITS,
            "fractional_point": self.FRACTIONAL_POINT,
            "known_truths_complete": False,
            "unknowns_count": len(self.unknowns),
            "open_unknowns": len(self.unknowns.list_by_status("open")),
            "conjecture_unknowns": len(self.unknowns.list_by_status("conjecture")),
        }


def _render_rational_duodecimal(value):
    """Render an exact rational as duodecimal (base-12) notation."""
    num = value.numerator
    den = value.denominator
    sign = "-" if num < 0 else ""
    num = abs(num)

    integer_part = num // den
    remainder = num % den

    if integer_part == 0:
        int_digits = ["0"]
    else:
        parts = []
        n = integer_part
        while n > 0:
            n, rem = divmod(n, 12)
            parts.append(str(rem) if rem < 10 else ("A" if rem == 10 else "B"))
        int_digits = list(reversed(parts))
    int_text = int_digits[0]
    if remainder == 0:
        text = f"{sign}{int_text}"
        return Notation(
            base=12,
            digits=tuple(str(d) for d in range(10)) + ("A", "B"),
            fractional_point=".",
            text=text,
            repeating=None,
        )

    frac_digits = []
    seen = {}
    r = remainder
    repeating_start = None

    while r != 0 and r not in seen:
        seen[r] = len(frac_digits)
        r *= 12
        digit = r // den
        frac_digits.append(str(digit) if digit < 10 else ("A" if digit == 10 else "B"))
        r = r % den

    if r in seen:
        repeating_start = seen[r]
        non_rep = "".join(frac_digits[:repeating_start])
        rep = "".join(frac_digits[repeating_start:])
        text = f"{sign}{int_text}.{non_rep}({rep})"
    else:
        text = f"{sign}{int_text}." + "".join(frac_digits)

    return Notation(
        base=12,
        digits=tuple(str(d) for d in range(10)) + ("A", "B"),
        fractional_point=".",
        text=text,
        repeating=repeating_start,
    )


__all__ = ["Base12Engine"]
