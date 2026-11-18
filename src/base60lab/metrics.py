"""Comparison and evaluation of representations across bases.

This module provides metrics for comparing base-10, base-12, and base-60
representations using exact rational arithmetic. No floating-point is used
internally for any comparisons.

Metrics categories:
    - Representation efficiency: digit count, information density
    - Mathematical simplicity: terminating fractions, period lengths
    - Computational efficiency: operation complexity
    - Visual interpretability: symbol diversity, cognitive load
    - Discovery effectiveness: pattern revelation, factorization visibility
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .core.rational import Rational


@dataclass(frozen=True, order=True)
class BaseMetrics:
    """Metrics for a single base.

    All values are exact Rational numbers where applicable.
    """

    base: int
    # Representation efficiency
    avg_digits_per_value: Rational  # Average digits to represent values in range
    information_density: Rational  # log2(base) bits per digit
    # Mathematical simplicity
    terminating_fraction_ratio: Rational  # Fraction of unit fractions that terminate
    avg_repeating_period: Rational  # Average period length for non-terminating
    max_repeating_period: int  # Maximum period for unit fractions up to denominator limit
    # Computational efficiency
    multiplication_complexity: Rational  # Relative complexity of multiplication
    addition_complexity: Rational  # Relative complexity of addition
    # Visual interpretability
    symbol_count: int  # Number of distinct digit symbols
    cognitive_load_index: Rational  # Composite measure of visual complexity
    # Discovery effectiveness
    factorization_visibility: Rational  # How well base reveals number structure
    pattern_revelation_score: Rational  # Score for revealing mathematical patterns

    def __post_init__(self) -> None:
        if self.base not in (10, 12, 60):
            raise ValueError(f"unsupported base {self.base}; must be 10, 12, or 60")


def _prime_factors(n: int) -> set[int]:
    """Return the set of prime factors of n."""
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def _terminating_fraction_ratio(base: int, max_denominator: int = 100) -> Rational:
    """Compute the fraction of unit fractions 1/d (d <= max_denominator) that terminate in base."""
    base_factors = _prime_factors(base)
    terminating = 0
    total = 0
    for d in range(1, max_denominator + 1):
        total += 1
        if _prime_factors(d).issubset(base_factors):
            terminating += 1
    return Rational(terminating, total) if total > 0 else Rational(0)


def _avg_repeating_period(base: int, max_denominator: int = 100) -> Rational:
    """Compute average repeating period for non-terminating unit fractions."""
    base_factors = _prime_factors(base)
    periods = []
    for d in range(1, max_denominator + 1):
        if not _prime_factors(d).issubset(base_factors):
            r = Rational(1, d)
            period = r.repeating_period_in_base(base)
            if period is not None:
                periods.append(period)
    if not periods:
        return Rational(0)
    total_period = Rational(0)
    for p in periods:
        total_period += Rational(p)
    return Rational(total_period.numerator, total_period.denominator * len(periods))


def _max_repeating_period(base: int, max_denominator: int = 100) -> int:
    """Maximum repeating period for unit fractions up to max_denominator."""
    base_factors = _prime_factors(base)
    max_period = 0
    for d in range(1, max_denominator + 1):
        if not _prime_factors(d).issubset(base_factors):
            r = Rational(1, d)
            period = r.repeating_period_in_base(base)
            if period is not None and period > max_period:
                max_period = period
    return max_period


def _avg_digits_per_value(base: int, max_value: int = 1000) -> Rational:
    """Average number of digits to represent integers 0..max_value in base."""
    total_digits = 0
    for n in range(max_value + 1):
        if n == 0:
            total_digits += 1
        else:
            digits = 0
            temp = n
            while temp > 0:
                temp //= base
                digits += 1
            total_digits += digits
    return Rational(total_digits, max_value + 1)


def _multiplication_complexity(base: int) -> Rational:
    """Relative complexity of multiplication in this base.

    Complexity grows with base^2 for naive multiplication table size.
    Normalized to base-10 = 1.
    """
    return Rational(base * base, 10 * 10)


def _addition_complexity(base: int) -> Rational:
    """Relative complexity of addition in this base.

    Complexity grows with base for addition table size.
    Normalized to base-10 = 1.
    """
    return Rational(base, 10)


def _cognitive_load_index(base: int, max_value: int = 1000) -> Rational:
    """Composite measure of visual/cognitive complexity.

    Factors: symbol count (distinct digit symbols to learn) and positional
    load (average digit count for values up to ``max_value``).  All arithmetic
    is exact Rational; lower is better.
    """
    avg_digits = _avg_digits_per_value(base, max_value)
    # Exact monotonic combination: symbol load times positional load.
    symbol_load = Rational(base)
    return symbol_load * avg_digits


def _information_density(base: int) -> Rational:
    """Information density: bits per digit for the base."""
    # log2(base) approximated as exact rational
    if base == 10:
        return Rational(332193, 100000)
    if base == 12:
        return Rational(358496, 100000)
    if base == 60:
        return Rational(590689, 100000)
    return Rational(base, 10)


def _factorization_visibility(base: int) -> Rational:
    """How well the base reveals factorization structure of numbers.

    A base with more small prime factors reveals more structure.
    Score based on sum of reciprocals of prime factors.
    """
    factors = _prime_factors(base)
    if not factors:
        return Rational(0)
    total = Rational(0)
    for p in factors:
        total += Rational(1, p)
    return total


def _pattern_revelation_score(base: int) -> Rational:
    """Score for revealing mathematical patterns (divisibility, fractions, etc.).

    Combines terminating fraction ratio with factorization visibility.
    """
    term_ratio = _terminating_fraction_ratio(base, 100)
    fact_vis = _factorization_visibility(base)
    return term_ratio * Rational(2) + fact_vis * Rational(3)


def _information_density(base: int) -> Rational:
    """Information density: log2(base) bits per digit, approximated as exact rational."""
    # log2(base) = ln(base)/ln(2). For exact rational, use rational approximations.
    # We can compute log2 via integer powers: find k such that 2^k ≈ base.
    # For bases 10, 12, 60:
    # log2(10) ≈ 3.32193 = 332193/100000
    # log2(12) ≈ 3.58496 = 358496/100000
    # log2(60) ≈ 5.90689 = 590689/100000
    if base == 10:
        return Rational(332193, 100000)
    if base == 12:
        return Rational(358496, 100000)
    if base == 60:
        return Rational(590689, 100000)
    # Fallback: compute via integer logarithm approximation
    k = 0
    pow2 = 1
    while pow2 < base:
        pow2 *= 2
        k += 1
    return Rational(k)


def compute_base_metrics(
    base: int,
    max_denominator: int = 100,
    max_value: int = 1000,
) -> BaseMetrics:
    """Compute comprehensive metrics for a single base.

    Args:
        base: The base to analyze (10, 12, or 60)
        max_denominator: Maximum denominator for fraction analysis
        max_value: Maximum integer value for digit count analysis

    Returns:
        BaseMetrics with all computed metrics as exact Rationals.
    """
    if base not in (10, 12, 60):
        raise ValueError(f"unsupported base {base}; must be 10, 12, or 60")

    return BaseMetrics(
        base=base,
        # Representation efficiency
        avg_digits_per_value=_avg_digits_per_value(base, max_value),
        information_density=_information_density(base),
        # Mathematical simplicity
        terminating_fraction_ratio=_terminating_fraction_ratio(base, max_denominator),
        avg_repeating_period=_avg_repeating_period(base, max_denominator),
        max_repeating_period=_max_repeating_period(base, max_denominator),
        # Computational efficiency
        multiplication_complexity=_multiplication_complexity(base),
        addition_complexity=_addition_complexity(base),
        # Visual interpretability
        symbol_count=base,
        cognitive_load_index=_cognitive_load_index(base),
        # Discovery effectiveness
        factorization_visibility=_factorization_visibility(base),
        pattern_revelation_score=_pattern_revelation_score(base),
    )


@dataclass(frozen=True)
class BaseComparison:
    """Comparison result between two or three bases."""

    base_metrics: tuple[BaseMetrics, ...]

    # Relative rankings (1 = best)
    representation_efficiency_rank: dict[int, int]
    mathematical_simplicity_rank: dict[int, int]
    computational_efficiency_rank: dict[int, int]
    visual_interpretability_rank: dict[int, int]
    discovery_effectiveness_rank: dict[int, int]

    # Overall composite score (higher = better)
    overall_scores: dict[int, Rational]


def _rank_by_exact(values: dict[int, Rational], reverse: bool = False) -> dict[int, int]:
    """Rank bases by exact Rational values (no floats)."""
    sorted_items = sorted(values.items(), key=lambda kv: kv[1], reverse=reverse)
    return {b: i + 1 for i, (b, _) in enumerate(sorted_items)}


def _rank_by_tuple(values: dict[int, tuple[Rational, Rational]], reverse: bool = False) -> dict[int, int]:
    """Rank by tuple of Rationals (e.g., (terminating_ratio, -avg_period))."""
    def sort_key(item):
        b, (primary, secondary) = item
        # We'll use Rational arithmetic for comparison
        return (primary, -secondary if secondary else Rational(0))
    sorted_items = sorted(values.items(), key=sort_key, reverse=reverse)
    return {b: i + 1 for i, (b, _) in enumerate(sorted_items)}


def _normalize_rational(values: dict[int, Rational], reverse: bool = False) -> dict[int, Rational]:
    """Normalize Rational values to 0-1 range using exact rational arithmetic."""
    vals = list(values.values())
    min_v = min(vals)
    max_v = max(vals)
    if max_v == min_v:
        return {k: Rational(1) for k in values}
    if reverse:
        return {k: (max_v - v) / (max_v - min_v) for k, v in values.items()}
    return {k: (v - min_v) / (max_v - min_v) for k, v in values.items()}


def compare_bases(
    *bases: int,
    max_denominator: int = 100,
    max_value: int = 1000,
) -> BaseComparison:
    """Compare metrics across multiple bases.

    Args:
        *bases: Bases to compare (each must be 10, 12, or 60)
        max_denominator: Maximum denominator for fraction analysis
        max_value: Maximum integer value for digit count analysis

    Returns:
        BaseComparison with metrics and rankings for each base.

    Raises:
        ValueError: If any base is not supported or if fewer than 2 bases given.
    """
    if len(bases) < 2:
        raise ValueError("at least two bases required for comparison")
    if len(set(bases)) != len(bases):
        raise ValueError("duplicate bases not allowed in comparison")
    for b in bases:
        if b not in (10, 12, 60):
            raise ValueError(f"unsupported base {b}; must be 10, 12, or 60")

    metrics = tuple(compute_base_metrics(b, max_denominator, max_value) for b in bases)

    # Build metric dictionaries by base
    avg_digits = {m.base: m.avg_digits_per_value for m in metrics}
    term_ratio = {m.base: m.terminating_fraction_ratio for m in metrics}
    avg_period = {m.base: m.avg_repeating_period for m in metrics}
    mul_complex = {m.base: m.multiplication_complexity for m in metrics}
    add_complex = {m.base: m.addition_complexity for m in metrics}
    cog_load = {m.base: m.cognitive_load_index for m in metrics}
    pattern_score = {m.base: m.pattern_revelation_score for m in metrics}

    # Rankings (1 = best)
    # Representation efficiency: fewer digits = better
    rep_rank = _rank_by_exact(avg_digits, reverse=False)

    # Mathematical simplicity: higher terminating ratio = better, lower avg period = better
    math_rank_values = {b: (term_ratio[b], avg_period[b]) for b in bases}
    math_rank = _rank_by_tuple(math_rank_values, reverse=True)

    # Computational efficiency: lower complexity = better
    comp_rank = _rank_by_exact({b: mul_complex[b] + add_complex[b] for b in bases}, reverse=False)

    # Visual interpretability: lower cognitive load = better
    visual_rank = _rank_by_exact(cog_load, reverse=False)

    # Discovery effectiveness: higher score = better
    disc_rank = _rank_by_exact(pattern_score, reverse=True)

    # Overall composite score using exact rational normalization
    norm_rep = _normalize_rational(avg_digits, reverse=True)  # fewer digits = better
    norm_math = {}
    for b in bases:
        t = term_ratio[b]
        p = avg_period[b]
        # Combine: (t + (1 - min(p, 1))/2)
        max_period_val = max(avg_period.values())
        norm_p = Rational(1) - (p / max_period_val) if max_period_val > 0 else Rational(1)
        norm_math[b] = (t + norm_p) / Rational(2)
    norm_comp = _normalize_rational({b: mul_complex[b] + add_complex[b] for b in bases}, reverse=True)
    norm_vis = _normalize_rational(cog_load, reverse=True)
    norm_disc = _normalize_rational(pattern_score, reverse=False)

    overall = {}
    for b in bases:
        overall[b] = (
            norm_rep[b] + norm_math[b] + norm_comp[b] + norm_vis[b] + norm_disc[b]
        ) / Rational(5)

    return BaseComparison(
        base_metrics=metrics,
        representation_efficiency_rank=rep_rank,
        mathematical_simplicity_rank=math_rank,
        computational_efficiency_rank=comp_rank,
        visual_interpretability_rank=visual_rank,
        discovery_effectiveness_rank=disc_rank,
        overall_scores=overall,
    )


def analyze_fraction_in_bases(
    numerator: int,
    denominator: int,
    bases: tuple[int, ...] = (10, 12, 60),
) -> dict[int, dict[str, Any]]:
    """Analyze a specific fraction across multiple bases.

    Returns exact representations and properties for each base.
    """
    r = Rational(numerator, denominator)
    results = {}
    for base in bases:
        if base not in (10, 12, 60):
            continue
        results[base] = {
            "value": r,
            "terminating": r.is_terminating_in_base(base),
            "repeating_period": r.repeating_period_in_base(base),
            "factors_of_denominator": _prime_factors(denominator),
            "factors_of_base": _prime_factors(base),
        }
    return results


def find_optimal_base_for_fractions(
    denominators: list[int],
    candidate_bases: tuple[int, ...] = (10, 12, 60),
) -> dict[int, list[int]]:
    """Find which base(s) give terminating representation for each denominator.

    Returns mapping from denominator to list of bases where it terminates.
    """
    result = {}
    for d in denominators:
        terminating_in = []
        for base in candidate_bases:
            r = Rational(1, d)
            if r.is_terminating_in_base(base):
                terminating_in.append(base)
        result[d] = terminating_in
    return result


__all__ = [
    "BaseMetrics",
    "BaseComparison",
    "compute_base_metrics",
    "compare_bases",
    "analyze_fraction_in_bases",
    "find_optimal_base_for_fractions",
]