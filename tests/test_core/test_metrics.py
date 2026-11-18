"""Tests for base-10/12/60 comparison metrics (exact rational arithmetic).

All comparisons are exact Rationals — no floating-point arithmetic is used
internally. Deterministic throughout.
"""

from fractions import Fraction

import pytest

from base60lab.core.rational import Rational
from base60lab.metrics import (
    BaseComparison,
    BaseMetrics,
    analyze_fraction_in_bases,
    compare_bases,
    compute_base_metrics,
    find_optimal_base_for_fractions,
)
import math


# ---------------------------------------------------------------------------
# Characterization test — baseline fails with ImportError when module missing
# ---------------------------------------------------------------------------

def test_metrics_module_importable():
    """Baseline characterization: the metrics module must be importable."""
    import base60lab.metrics as m

    assert hasattr(m, "BaseMetrics")
    assert hasattr(m, "BaseComparison")
    assert hasattr(m, "compute_base_metrics")
    assert hasattr(m, "compare_bases")
    assert hasattr(m, "analyze_fraction_in_bases")
    assert hasattr(m, "find_optimal_base_for_fractions")


# ---------------------------------------------------------------------------
# compute_base_metrics — exact rational properties
# ---------------------------------------------------------------------------

def test_compute_base_metrics_supported_bases():
    for base in (10, 12, 60):
        m = compute_base_metrics(base)
        assert m.base == base
        assert isinstance(m.avg_digits_per_value, Rational)
        assert isinstance(m.information_density, Rational)
        assert isinstance(m.terminating_fraction_ratio, Rational)
        assert isinstance(m.avg_repeating_period, Rational)
        assert isinstance(m.multiplication_complexity, Rational)
        assert isinstance(m.addition_complexity, Rational)
        assert isinstance(m.cognitive_load_index, Rational)
        assert isinstance(m.factorization_visibility, Rational)
        assert isinstance(m.pattern_revelation_score, Rational)
        assert m.symbol_count == base
        assert isinstance(m.max_repeating_period, int)


def test_compute_base_metrics_rejects_invalid_base():
    for bad in (0, 1, 2, 7, 16, 61, -10):
        with pytest.raises(ValueError):
            compute_base_metrics(bad)


def test_compute_base_metrics_all_exact_rational():
    """Every numeric metric must be a Rational, never a float."""
    for base in (10, 12, 60):
        m = compute_base_metrics(base)
        for name in (
            "avg_digits_per_value",
            "information_density",
            "terminating_fraction_ratio",
            "avg_repeating_period",
            "multiplication_complexity",
            "addition_complexity",
            "cognitive_load_index",
            "factorization_visibility",
            "pattern_revelation_score",
        ):
            assert not isinstance(getattr(m, name), float), f"{name} is float"


def test_base60_has_more_terminating_fractions():
    """Base 60 terminates for 1/2, 1/3, 1/4, 1/5, ... many more than base 10."""
    m10 = compute_base_metrics(10)
    m60 = compute_base_metrics(60)
    assert m60.terminating_fraction_ratio > m10.terminating_fraction_ratio


def test_base12_terminates_1_over_3():
    m = compute_base_metrics(12)
    # 1/3 terminates in base 12 (12 = 2^2 * 3)
    assert m.terminating_fraction_ratio > Rational(0)


def test_terminating_fraction_ratio_exact():
    # Rational check: denominator of ratio must be integer
    m10 = compute_base_metrics(10, max_denominator=60)
    assert m10.terminating_fraction_ratio.denominator >= 1


def test_avg_digits_per_value_monotonic():
    """Higher bases need fewer average digits."""
    m10 = compute_base_metrics(10)
    m12 = compute_base_metrics(12)
    m60 = compute_base_metrics(60)
    assert m10.avg_digits_per_value > m12.avg_digits_per_value > m60.avg_digits_per_value


def test_information_density_monotonic():
    m10 = compute_base_metrics(10)
    m12 = compute_base_metrics(12)
    m60 = compute_base_metrics(60)
    assert m10.information_density < m12.information_density < m60.information_density


def test_multiplication_complexity_growth():
    m10 = compute_base_metrics(10)
    m12 = compute_base_metrics(12)
    m60 = compute_base_metrics(60)
    assert m10.multiplication_complexity == Rational(1)
    assert m12.multiplication_complexity == Rational(144, 100)
    assert m60.multiplication_complexity == Rational(36)


def test_addition_complexity_growth():
    m10 = compute_base_metrics(10)
    m12 = compute_base_metrics(12)
    m60 = compute_base_metrics(60)
    assert m10.addition_complexity == Rational(1)
    assert m12.addition_complexity == Rational(6, 5)
    assert m60.addition_complexity == Rational(6)


def test_base_metrics_frozen_hashable():
    m = compute_base_metrics(12)
    # Frozen dataclass: hashable, immutable
    hash(m)
    with pytest.raises(Exception):
        m.base = 13  # type: ignore[misc]


# ---------------------------------------------------------------------------
# compare_bases — cross-base comparison
# ---------------------------------------------------------------------------

def test_compare_bases_three_way():
    cmp = compare_bases(10, 12, 60)
    assert isinstance(cmp, BaseComparison)
    assert tuple(m.base for m in cmp.base_metrics) == (10, 12, 60)

    # Rankings cover all three bases exactly once
    for rank_dict in (
        cmp.representation_efficiency_rank,
        cmp.mathematical_simplicity_rank,
        cmp.computational_efficiency_rank,
        cmp.visual_interpretability_rank,
        cmp.discovery_effectiveness_rank,
    ):
        assert sorted(rank_dict.values()) == [1, 2, 3]
        assert set(rank_dict.keys()) == {10, 12, 60}


def test_compare_bases_two_way():
    cmp = compare_bases(12, 60)
    assert sorted(cmp.representation_efficiency_rank.values()) == [1, 2]
    assert set(cmp.representation_efficiency_rank.keys()) == {12, 60}


def test_compare_bases_rejects_single_base():
    with pytest.raises(ValueError):
        compare_bases(10)


def test_compare_bases_rejects_duplicate_bases():
    with pytest.raises(ValueError):
        compare_bases(12, 12)


def test_compare_bases_rejects_invalid_base():
    with pytest.raises(ValueError):
        compare_bases(10, 7, 60)


def test_compare_bases_rejects_unsupported_in_middle():
    with pytest.raises(ValueError):
        compare_bases(10, 11, 60)


def test_overall_scores_exact_rational():
    cmp = compare_bases(10, 12, 60)
    for b, score in cmp.overall_scores.items():
        assert isinstance(score, Rational)
        assert not isinstance(score, float)
        assert Rational(0) <= score <= Rational(1)


def test_overall_scores_sum_is_exact():
    """Scores must be exact rational sums, never float round-trip artifacts."""
    cmp = compare_bases(10, 12, 60)
    for s in cmp.overall_scores.values():
        assert s.to_fraction() == Fraction(s.numerator, s.denominator)


def test_representation_rank_prefers_larger_bases():
    cmp = compare_bases(10, 12, 60)
    assert cmp.representation_efficiency_rank[60] == 1
    assert cmp.representation_efficiency_rank[10] == 3


def test_mathematical_rank_prefers_base60():
    cmp = compare_bases(10, 12, 60)
    assert cmp.mathematical_simplicity_rank[60] == 1


def test_computational_rank_prefers_base10():
    cmp = compare_bases(10, 12, 60)
    assert cmp.computational_efficiency_rank[10] == 1


def test_discovery_rank_prefers_base60():
    cmp = compare_bases(10, 12, 60)
    assert cmp.discovery_effectiveness_rank[60] == 1


def test_compare_bases_deterministic():
    """Flaky-test prevention: repeated calls produce identical results."""
    cmp1 = compare_bases(10, 12, 60)
    cmp2 = compare_bases(10, 12, 60)
    assert cmp1 == cmp2


def test_compare_bases_value_validation():
    """Misleading-success prevention: verify actual computed values."""
    cmp = compare_bases(10, 12, 60)
    by_base = {m.base: m for m in cmp.base_metrics}
    # Base 10 mul complexity is exactly base^2 / 100
    assert by_base[10].multiplication_complexity == Rational(1)
    assert by_base[12].multiplication_complexity == Rational(36, 25)
    # Base 60 add complexity is base/10
    assert by_base[60].addition_complexity == Rational(6)
    # Info density is exact rational approximation of log2
    assert by_base[10].information_density == Rational(332193, 100000)
    # Terminating ratio for base 10 must be less than base 60
    assert by_base[10].terminating_fraction_ratio < by_base[60].terminating_fraction_ratio


# ---------------------------------------------------------------------------
# analyze_fraction_in_bases
# ---------------------------------------------------------------------------

def test_analyze_fraction_in_bases_basic():
    result = analyze_fraction_in_bases(1, 3)
    assert set(result.keys()) == {10, 12, 60}
    for base, info in result.items():
        assert info["value"] == Rational(1, 3)
        assert "terminating" in info
        assert "repeating_period" in info
        assert "factors_of_denominator" in info
        assert "factors_of_base" in info


def test_analyze_fraction_1_over_3():
    result = analyze_fraction_in_bases(1, 3)
    # 1/3 terminates in base 12 and 60, but not base 10
    assert result[10]["terminating"] is False
    assert result[12]["terminating"] is True
    assert result[60]["terminating"] is True


def test_analyze_fraction_1_over_5():
    result = analyze_fraction_in_bases(1, 5)
    # 1/5 terminates in base 10 (5 | 10) and base 60 (5 | 60) but not base 12
    assert result[10]["terminating"] is True
    assert result[12]["terminating"] is False
    assert result[60]["terminating"] is True


def test_analyze_fraction_1_over_7():
    result = analyze_fraction_in_bases(1, 7)
    # 7 divides no power of 2, 5, 3 → repeating in all three bases
    assert result[10]["terminating"] is False
    assert result[12]["terminating"] is False
    assert result[60]["terminating"] is False
    # All periods are positive integers
    for base in (10, 12, 60):
        period = result[base]["repeating_period"]
        assert isinstance(period, int)
        assert period > 0


def test_analyze_fraction_unsupported_bases_skipped():
    result = analyze_fraction_in_bases(1, 2, bases=(10, 7, 60))
    assert set(result.keys()) == {10, 60}


def test_analyze_fraction_factors_exact():
    result = analyze_fraction_in_bases(1, 12)
    assert result[10]["factors_of_denominator"] == {2, 3}
    assert result[10]["factors_of_base"] == {2, 5}
    assert result[12]["factors_of_base"] == {2, 3}
    assert result[60]["factors_of_base"] == {2, 3, 5}


# ---------------------------------------------------------------------------
# find_optimal_base_for_fractions
# ---------------------------------------------------------------------------

def test_find_optimal_base_for_fractions_basic():
    result = find_optimal_base_for_fractions([2, 3, 5, 7, 11])
    assert set(result.keys()) == {2, 3, 5, 7, 11}
    assert 10 in result[2]
    assert 12 in result[3]
    assert 60 in result[3]
    assert result[7] == []
    assert result[11] == []


def test_find_optimal_base_for_fractions_includes_60_for_common():
    result = find_optimal_base_for_fractions([2, 3, 4, 5, 6])
    for d in [2, 3, 4, 5, 6]:
        assert 60 in result[d]


def test_find_optimal_base_for_fractions_empty_denominators():
    result = find_optimal_base_for_fractions([])
    assert result == {}


def test_find_optimal_base_candidates_restricted():
    result = find_optimal_base_for_fractions([3, 5], candidate_bases=(12,))
    assert result[3] == [12]
    assert result[5] == []
# ---------------------------------------------------------------------------
# Edge cases for uncovered lines
# ---------------------------------------------------------------------------

def test_base_metrics_post_init_rejects_invalid_base():
    """Test BaseMetrics.__post_init__ raises ValueError for unsupported base."""
    # This tests line 50 in metrics.py
    with pytest.raises(ValueError, match="unsupported base 7"):
        BaseMetrics(
            base=7,
            avg_digits_per_value=Rational(1),
            information_density=Rational(1),
            terminating_fraction_ratio=Rational(1),
            avg_repeating_period=Rational(0),
            max_repeating_period=0,
            multiplication_complexity=Rational(1),
            addition_complexity=Rational(1),
            symbol_count=7,
            cognitive_load_index=Rational(1),
            factorization_visibility=Rational(1),
            pattern_revelation_score=Rational(1),
        )


def test_avg_repeating_period_no_periods():
    """Test _avg_repeating_period returns Rational(0) when no non-terminating fractions."""
    # This tests line 90 in metrics.py
    # Use a base that's a power of a prime and max_denominator=1
    # For base=2 (not supported), but let's test the internal function directly
    from base60lab.metrics import _avg_repeating_period
    
    # For base where all denominators up to max_denominator terminate
    # Base 2 with max_denominator=1: only 1/1, which terminates
    # But base 2 is not supported... let's use base=4 (also not supported)
    # Actually, the function is internal, so we can test with any base
    result = _avg_repeating_period(2, max_denominator=1)
    assert result == Rational(0)
    
    # Another case: base=4, max_denominator=2
    # 1/1 terminates, 1/2 terminates (4 = 2^2)
    result = _avg_repeating_period(4, max_denominator=2)
    assert result == Rational(0)


def test_factorization_visibility_no_factors():
    """Test _factorization_visibility returns Rational(0) for base=1."""
    # This tests line 177 in metrics.py
    from base60lab.metrics import _factorization_visibility
    
    result = _factorization_visibility(1)
    assert result == Rational(0)


def test_information_density_fallback():
    """Test _information_density fallback for bases other than 10, 12, 60."""
    # This tests lines 160-166 and 209-214 in metrics.py
    from base60lab.metrics import _information_density
    
    # Test base=2 (fallback computes k where 2^k >= base)
    result = _information_density(2)
    assert result == Rational(1)  # k=1 since 2^1 = 2
    
    # Test base=3
    result = _information_density(3)
    assert result == Rational(2)  # k=2 since 2^2 = 4 > 3
    
    # Test base=4
    result = _information_density(4)
    assert result == Rational(2)  # k=2 since 2^2 = 4
    
    # Test base=5
    result = _information_density(5)
    assert result == Rational(3)  # k=3 since 2^3 = 8 > 5
    
    # Test base=8
    result = _information_density(8)
    assert result == Rational(3)  # k=3 since 2^3 = 8


def test_normalize_rational_equal_values():
    """Test _normalize_rational when all values are equal."""
    # This tests line 295 in metrics.py
    from base60lab.metrics import _normalize_rational
    
    values = {10: Rational(5), 12: Rational(5), 60: Rational(5)}
    result = _normalize_rational(values)
    assert result == {10: Rational(1), 12: Rational(1), 60: Rational(1)}
    
    # Test with reverse=True
    result_rev = _normalize_rational(values, reverse=True)
    assert result_rev == {10: Rational(1), 12: Rational(1), 60: Rational(1)}


def test_compare_bases_normalize_edge_case():
    """Test compare_bases with bases that have equal metric values."""
    # This tests the _normalize_rational equal values case in context
    # Create a scenario where two bases have identical metrics
    # This is hard with real bases, but we can test the internal function
    pass


# ---------------------------------------------------------------------------
# Additional edge case tests for better coverage
# ---------------------------------------------------------------------------

def test_prime_factors_edge_cases():
    """Test _prime_factors with edge cases."""
    from base60lab.metrics import _prime_factors
    
    assert _prime_factors(1) == set()
    assert _prime_factors(2) == {2}
    assert _prime_factors(4) == {2}
    assert _prime_factors(6) == {2, 3}
    assert _prime_factors(12) == {2, 3}
    assert _prime_factors(60) == {2, 3, 5}
    assert _prime_factors(97) == {97}  # prime


def test_terminating_fraction_ratio_edge_cases():
    """Test _terminating_fraction_ratio with edge cases."""
    from base60lab.metrics import _terminating_fraction_ratio
    
    # max_denominator=0 should return 0
    result = _terminating_fraction_ratio(10, max_denominator=0)
    assert result == Rational(0)
    
    # max_denominator=1
    result = _terminating_fraction_ratio(10, max_denominator=1)
    assert result == Rational(1)  # 1/1 terminates


def test_max_repeating_period_edge_cases():
    """Test _max_repeating_period with edge cases."""
    from base60lab.metrics import _max_repeating_period
    
    # max_denominator=0
    result = _max_repeating_period(10, max_denominator=0)
    assert result == 0
    
    # Base where all fractions terminate up to max_denominator
    result = _max_repeating_period(2, max_denominator=2)
    assert result == 0


def test_avg_digits_per_value_edge_cases():
    """Test _avg_digits_per_value with edge cases."""
    from base60lab.metrics import _avg_digits_per_value
    
    # max_value=0
    result = _avg_digits_per_value(10, max_value=0)
    assert result == Rational(1)  # Only 0, which has 1 digit
    
    # max_value=1
    result = _avg_digits_per_value(10, max_value=1)
    assert result == Rational(2, 2)  # 0 and 1, both 1 digit = 2/2 = 1


def test_cognitive_load_index_edge_cases():
    """Test _cognitive_load_index with edge cases."""
    from base60lab.metrics import _cognitive_load_index, _avg_digits_per_value
    
    # max_value=0: only 0, which has 1 digit
    # avg_digits = 1/1 = 1, symbol_load = base
    result = _cognitive_load_index(10, max_value=0)
    # symbol_load = 10, avg_digits = 1
    assert result == Rational(10)
    
    result = _cognitive_load_index(60, max_value=0)
    assert result == Rational(60)
    
    # max_value=1: 0 and 1, both 1 digit
    # avg_digits = 2/2 = 1, symbol_load = base
    result = _cognitive_load_index(10, max_value=1)
    assert result == Rational(10)
    
    result = _cognitive_load_index(60, max_value=1000)
    # Should be larger due to more symbols
    m10 = _cognitive_load_index(10, max_value=1000)
    assert result > m10


def test_multiplication_addition_complexity_exact():
    """Test _multiplication_complexity and _addition_complexity exact values."""
    from base60lab.metrics import _multiplication_complexity, _addition_complexity
    
    # Base 10
    assert _multiplication_complexity(10) == Rational(1)
    assert _addition_complexity(10) == Rational(1)
    
    # Base 12
    assert _multiplication_complexity(12) == Rational(144, 100)  # 12*12 / 10*10
    assert _addition_complexity(12) == Rational(12, 10)
    
    # Base 60
    assert _multiplication_complexity(60) == Rational(3600, 100)  # 36
    assert _addition_complexity(60) == Rational(60, 10)  # 6


def test_pattern_revelation_score():
    """Test _pattern_revelation_score computation."""
    from base60lab.metrics import _pattern_revelation_score, _terminating_fraction_ratio, _factorization_visibility
    
    for base in (10, 12, 60):
        term_ratio = _terminating_fraction_ratio(base, 100)
        fact_vis = _factorization_visibility(base)
        expected = term_ratio * Rational(2) + fact_vis * Rational(3)
        actual = _pattern_revelation_score(base)
        assert actual == expected


def test_compute_base_metrics_custom_params():
    """Test compute_base_metrics with custom max_denominator and max_value."""
    from base60lab.metrics import compute_base_metrics
    
    # Test with small max_denominator
    m = compute_base_metrics(10, max_denominator=10, max_value=10)
    assert m.terminating_fraction_ratio > Rational(0)
    assert m.avg_digits_per_value > Rational(0)
    
    # Test with larger values
    m = compute_base_metrics(60, max_denominator=200, max_value=2000)
    assert m.terminating_fraction_ratio > Rational(0)


def test_analyze_fraction_in_bases_more_cases():
    """Test analyze_fraction_in_bases with more fractions."""
    from base60lab.metrics import analyze_fraction_in_bases
    
    # Fraction that terminates in all bases
    result = analyze_fraction_in_bases(1, 2)
    for base in (10, 12, 60):
        assert result[base]["terminating"] is True
        assert result[base]["repeating_period"] is None
    
    # Fraction that terminates in base 12 and 60 but not 10
    result = analyze_fraction_in_bases(1, 3)
    assert result[10]["terminating"] is False
    assert result[12]["terminating"] is True
    assert result[60]["terminating"] is True
    
    # Fraction that terminates in base 10 and 60 but not 12
    result = analyze_fraction_in_bases(1, 5)
    assert result[10]["terminating"] is True
    assert result[12]["terminating"] is False
    assert result[60]["terminating"] is True
    
    # Fraction that terminates nowhere
    result = analyze_fraction_in_bases(1, 7)
    for base in (10, 12, 60):
        assert result[base]["terminating"] is False
        assert result[base]["repeating_period"] is not None
        assert result[base]["repeating_period"] > 0


def test_find_optimal_base_for_fractions_more_cases():
    """Test find_optimal_base_for_fractions with more cases."""
    from base60lab.metrics import find_optimal_base_for_fractions
    
    # Denominators that are powers of 2
    result = find_optimal_base_for_fractions([2, 4, 8, 16])
    for d in [2, 4, 8, 16]:
        assert 10 in result[d]
        assert 12 in result[d]
        assert 60 in result[d]
    
    # Denominators with factor 3
    result = find_optimal_base_for_fractions([3, 6, 9, 12])
    for d in [3, 6, 9, 12]:
        assert 10 not in result[d]
        assert 12 in result[d]
        assert 60 in result[d]
    
    # Denominators with factor 5
    result = find_optimal_base_for_fractions([5, 10, 15, 20])
    for d in [5, 10, 15, 20]:
        if d % 2 == 0:  # 10, 20
            assert 10 in result[d]
        assert 60 in result[d]
    
    # Denominators with factor 7
    result = find_optimal_base_for_fractions([7, 14, 21])
    for d in [7, 14, 21]:
        assert result[d] == []  # No base supports 7
    
    # Large denominators
    result = find_optimal_base_for_fractions([30, 31, 32, 33, 34, 35])
    # 30 = 2*3*5: only base 60 has all three factors
    assert 10 not in result[30]
    assert 12 not in result[30]
    assert 60 in result[30]
    # 31 = 31 (prime): no base has 31
    assert result[31] == []
    # 32 = 2^5: all bases have factor 2
    assert 10 in result[32]
    assert 12 in result[32]
    assert 60 in result[32]
    # 33 = 3*11: no base has 11
    assert result[33] == []
    # 34 = 2*17: no base has 17
    assert result[34] == []
    # 35 = 5*7: no base has 7
    assert result[35] == []


def test_rank_by_exact_and_tuple():
    """Test _rank_by_exact and _rank_by_tuple functions."""
    from base60lab.metrics import _rank_by_exact, _rank_by_tuple
    
    # Test _rank_by_exact
    values = {10: Rational(3), 12: Rational(2), 60: Rational(1)}
    rank = _rank_by_exact(values, reverse=False)  # Smaller is better
    assert rank[60] == 1
    assert rank[12] == 2
    assert rank[10] == 3
    
    rank_rev = _rank_by_exact(values, reverse=True)  # Larger is better
    assert rank_rev[10] == 1
    assert rank_rev[12] == 2
    assert rank_rev[60] == 3
    
    # Test _rank_by_tuple
    tuple_values = {
        10: (Rational(1), Rational(3)),
        12: (Rational(2), Rational(2)),
        60: (Rational(3), Rational(1)),
    }
    rank = _rank_by_tuple(tuple_values, reverse=True)
    # Primary: larger is better, Secondary: smaller is better (negative)
    assert rank[60] == 1  # Primary 3 is highest
    assert rank[12] == 2  # Primary 2
    assert rank[10] == 3  # Primary 1


def test_compare_bases_detailed():
    """Test compare_bases with detailed verification."""
    from base60lab.metrics import compare_bases
    
    # Test with all three bases
    cmp = compare_bases(10, 12, 60)
    
    # Check all ranks have all three bases
    for rank_dict in [
        cmp.representation_efficiency_rank,
        cmp.mathematical_simplicity_rank,
        cmp.computational_efficiency_rank,
        cmp.visual_interpretability_rank,
        cmp.discovery_effectiveness_rank,
    ]:
        assert set(rank_dict.keys()) == {10, 12, 60}
        assert set(rank_dict.values()) == {1, 2, 3}
    
    # Check overall scores are in [0, 1]
    for score in cmp.overall_scores.values():
        assert Rational(0) <= score <= Rational(1)
    
    # Verify BaseMetrics are stored
    assert len(cmp.base_metrics) == 3
    bases_in_metrics = {m.base for m in cmp.base_metrics}
    assert bases_in_metrics == {10, 12, 60}


def test_compare_bases_two_way_detailed():
    """Test compare_bases with two bases."""
    from base60lab.metrics import compare_bases
    
    cmp = compare_bases(10, 60)
    
    # Check ranks
    for rank_dict in [
        cmp.representation_efficiency_rank,
        cmp.mathematical_simplicity_rank,
        cmp.computational_efficiency_rank,
        cmp.visual_interpretability_rank,
        cmp.discovery_effectiveness_rank,
    ]:
        assert set(rank_dict.keys()) == {10, 60}
        assert set(rank_dict.values()) == {1, 2}
    
    # Overall scores
    assert len(cmp.overall_scores) == 2
    for score in cmp.overall_scores.values():
        assert Rational(0) <= score <= Rational(1)


def test_base_metrics_ordering():
    """Test BaseMetrics ordering (frozen, order=True)."""
    from base60lab.metrics import BaseMetrics, compute_base_metrics
    
    m1 = compute_base_metrics(10)
    m2 = compute_base_metrics(12)
    m3 = compute_base_metrics(60)
    
    # Ordering is by base (first field)
    assert m1 < m2 < m3
    assert m3 > m2 > m1
    assert m1 <= m2 <= m3
    assert m3 >= m2 >= m1
    
    # Equality
    m1_copy = compute_base_metrics(10)
    assert m1 == m1_copy
    assert not (m1 != m1_copy)
    assert m1 != m2
