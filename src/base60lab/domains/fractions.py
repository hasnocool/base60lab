"""Fractions domain — reciprocals, division, terminating vs repeating per base.

Delegates all base-specific arithmetic to the base engines (base10, base12,
base60) instead of re-implementing per-base logic.
"""

from __future__ import annotations

from ..core.rational import Rational
from ..core.types import BaseNumber
from ..engines import Base10Engine, Base12Engine, Base60Engine


class FractionsDomain:
    """Analyze fractions across all three bases using the engines."""

    def __init__(self, engines: dict[int, Base10Engine | Base12Engine | Base60Engine]) -> None:
        self.engines = engines

    def reciprocal(self, denominator: int, base: int) -> BaseNumber:
        """Return 1/denominator as a BaseNumber in the given base."""
        engine = self.engines[base]
        value = Rational(1, denominator)
        return engine.from_rational(value)

    def divides(self, a: BaseNumber, b: BaseNumber) -> BaseNumber:
        """Return a / b using the engine of a's base."""
        engine = self.engines[a.base]
        return engine.div(a, b)

    def is_terminating(self, denominator: int, base: int) -> bool:
        """True if 1/denominator terminates in the given base."""
        engine = self.engines[base]
        return Rational(1, denominator).is_terminating_in_base(base)

    def repeating_period(self, denominator: int, base: int) -> int | None:
        """Repeating period of 1/denominator in the given base, or None if terminating."""
        engine = self.engines[base]
        return engine.repeating_period(denominator)

    def terminating_count(self, limit: int = 360) -> dict[int, list[int]]:
        """Return denominators whose reciprocals terminate, per base."""
        return {
            base: self.engines[base].terminating_denominators(limit)
            for base in (10, 12, 60)
        }

    def compare_reciprocal(self, denominator: int) -> dict[int, str]:
        """Render 1/denominator in all three bases as notation strings."""
        result = {}
        for base in (10, 12, 60):
            engine = self.engines[base]
            number = self.reciprocal(denominator, base)
            notation = engine.to_notation(number)
            result[base] = notation.text
        return result


__all__ = ["FractionsDomain"]
