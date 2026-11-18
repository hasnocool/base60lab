"""Tests for Lissajous figures module."""

from base60lab.core.rational import Rational
from base60lab.lissajous import (
    LissajousParameters,
    ClosureInfo,
    is_closed,
    closure_info,
    generate_lissajous_points,
    plot_lissajous,
    compare_frequency_ratios,
    analyze_prime_factor_effects,
    prime_factors,
    classify_denominator,
)


# --- Baseline characterization test (module doesn't exist → ImportError) ---
# This test will fail initially if the module doesn't exist, then pass after implementation


def test_module_imports():
    """Baseline: module can be imported."""
    from base60lab import lissajous
    assert lissajous is not None


# --- Core functionality tests ---


def test_is_closed_true_for_rational_ratio():
    """A rational frequency ratio yields a closed Lissajous figure."""
    assert is_closed(3, 2) is True
    assert is_closed(5, 3) is True
    assert is_closed(1, 1) is True
    assert is_closed(Rational(7), Rational(5)) is True


def test_is_closed_with_rational_objects():
    """is_closed works with Rational objects."""
    assert is_closed(Rational(3), Rational(2)) is True
    assert is_closed(Rational(2, 3), Rational(1, 2)) is True


def test_is_closed_zero_frequency_raises():
    """Zero frequency in y direction raises ValueError."""
    try:
        is_closed(1, 0)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "cannot be zero" in str(e)


def test_closure_info_basic():
    """closure_info returns correct closure information."""
    info = closure_info(3, 2)
    assert info.is_closed is True
    assert info.closure_period == 2
    assert info.numerator == 3
    assert info.denominator == 2
    assert info.factorization == {2: 1}
    assert info.prime_class == "2_3_5_smooth"


def test_closure_info_reduced_fraction():
    """closure_info reduces the fraction."""
    info = closure_info(6, 4)  # 6/4 = 3/2
    assert info.numerator == 3
    assert info.denominator == 2
    assert info.closure_period == 2


def test_closure_info_prime_factors():
    """closure_info correctly computes prime factorization."""
    info = closure_info(1, 60)  # denominator 60 = 2^2 * 3 * 5
    assert info.factorization == {2: 2, 3: 1, 5: 1}
    assert info.prime_class == "2_3_5_smooth"

    info = closure_info(1, 7)  # prime 7
    assert info.factorization == {7: 1}
    assert info.prime_class == "prime_7_11_13"

    info = closure_info(1, 14)  # 2 * 7 = mixed
    assert info.factorization == {2: 1, 7: 1}
    assert info.prime_class == "mixed"


def test_classify_denominator():
    """Denominator classification by prime factors."""
    assert classify_denominator(1) == "2_3_5_smooth"
    assert classify_denominator(2) == "2_3_5_smooth"
    assert classify_denominator(3) == "2_3_5_smooth"
    assert classify_denominator(5) == "2_3_5_smooth"
    assert classify_denominator(6) == "2_3_5_smooth"  # 2*3
    assert classify_denominator(60) == "2_3_5_smooth"  # 2^2*3*5

    assert classify_denominator(7) == "prime_7_11_13"
    assert classify_denominator(11) == "prime_7_11_13"
    assert classify_denominator(13) == "prime_7_11_13"
    assert classify_denominator(77) == "prime_7_11_13"  # 7*11

    assert classify_denominator(14) == "mixed"  # 2*7
    assert classify_denominator(21) == "mixed"  # 3*7
    assert classify_denominator(30) == "2_3_5_smooth"  # 2*3*5 -> smooth


def test_prime_factors():
    """Prime factorization correctness."""
    assert prime_factors(1) == {}
    assert prime_factors(2) == {2: 1}
    assert prime_factors(4) == {2: 2}
    assert prime_factors(12) == {2: 2, 3: 1}
    assert prime_factors(60) == {2: 2, 3: 1, 5: 1}
    assert prime_factors(7) == {7: 1}
    assert prime_factors(14) == {2: 1, 7: 1}


def test_lissajous_parameters():
    """LissajousParameters construction and methods."""
    params = LissajousParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        phase=Rational(1, 2),
    )
    assert params.freq_x == Rational(3)
    assert params.freq_y == Rational(2)
    assert params.phase == Rational(1, 2)

    ratio = params.frequency_ratio()
    assert ratio == Rational(3, 2)

    num, den = params.reduced_ratio()
    assert num == 3
    assert den == 2


def test_generate_lissajous_points():
    """Point generation returns correct shape arrays."""
    params = LissajousParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        phase=Rational(0),
    )
    x, y = generate_lissajous_points(params, num_points=100)
    assert x.shape == (100,)
    assert y.shape == (100,)
    # Values should be in [-1, 1] for unit amplitude
    assert all(-1.0 <= v <= 1.0 for v in x)
    assert all(-1.0 <= v <= 1.0 for v in y)


def test_plot_lissajous_creates_figure(tmp_path):
    """plot_lissajous creates and saves a figure."""
    params = LissajousParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        phase=Rational(0),
    )
    output_path = tmp_path / "test_lissajous.svg"
    fig = plot_lissajous(params, output_path=str(output_path))
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_compare_frequency_ratios():
    """compare_frequency_ratios returns list of ClosureInfo."""
    ratios = [(1, 1), (3, 2), (5, 3), (7, 5)]
    results = compare_frequency_ratios(ratios)
    assert len(results) == 4
    assert all(isinstance(r, ClosureInfo) for r in results)
    assert results[0].closure_period == 1
    assert results[1].closure_period == 2
    assert results[2].closure_period == 3
    assert results[3].closure_period == 5


def test_analyze_prime_factor_effects():
    """analyze_prime_factor_effects categorizes by prime class."""
    classes = analyze_prime_factor_effects(max_denominator=20)
    assert "2_3_5_smooth" in classes
    assert "prime_7_11_13" in classes
    assert "mixed" in classes

    # Check that we have entries in each
    assert len(classes["2_3_5_smooth"]) > 0
    assert len(classes["prime_7_11_13"]) > 0
    assert len(classes["mixed"]) > 0


def test_closure_period_equals_denominator():
    """Closure period equals the denominator of reduced ratio."""
    # For ratio a/b in lowest terms, period = b
    test_cases = [
        (1, 1, 1),
        (3, 2, 2),
        (5, 3, 3),
        (7, 5, 5),
        (2, 7, 7),
        (11, 13, 13),
    ]
    for num, den, expected_period in test_cases:
        info = closure_info(num, den)
        assert info.closure_period == expected_period, f"Failed for {num}/{den}"


def test_deterministic_results():
    """All computations are deterministic (no floating-point randomness)."""
    for _ in range(10):
        info1 = closure_info(7, 5)
        info2 = closure_info(7, 5)
        assert info1.closure_period == info2.closure_period
        assert info1.factorization == info2.factorization
        assert info1.prime_class == info2.prime_class


def test_phase_parameter():
    """Phase parameter is stored and used correctly."""
    params = LissajousParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        phase=Rational(1, 4),  # π/4
    )
    assert params.phase == Rational(1, 4)
    x, y = generate_lissajous_points(params, num_points=10)
    assert x.shape == (10,)


def test_amplitude_parameters():
    """Amplitude parameters affect output range."""
    params = LissajousParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        phase=Rational(0),
        amplitude_x=Rational(2),
        amplitude_y=Rational(3),
    )
    x, y = generate_lissajous_points(params, num_points=100)
    assert all(-2.0 <= v <= 2.0 for v in x)
    assert all(-3.0 <= v <= 3.0 for v in y)


# --- Adversarial / edge case tests ---


def test_negative_frequencies():
    """Negative frequencies work (ratio sign doesn't affect closure)."""
    info = closure_info(-3, 2)
    assert info.is_closed is True
    assert info.closure_period == 2
    assert info.numerator == -3
    assert info.denominator == 2


def test_large_frequencies():
    """Large frequencies still compute correctly."""
    info = closure_info(1009, 1013)  # large primes
    assert info.is_closed is True
    assert info.closure_period == 1013
    assert info.factorization == {1013: 1}
    assert info.prime_class == "mixed"  # 1013 is prime, but not in {7,11,13} group


def test_zero_phase():
    """Zero phase is valid."""
    params = LissajousParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        phase=Rational(0),
    )
    assert params.phase == Rational(0)


def test_closure_info_str():
    """ClosureInfo string representation is informative."""
    info = closure_info(3, 2)
    s = str(info)
    assert "Closed" in s
    assert "period=2" in s
    assert "3/2" in s
    assert "2_3_5_smooth" in s


def test_save_closure_analysis(tmp_path):
    """save_closure_analysis creates markdown and plots."""
    from base60lab.lissajous import save_closure_analysis
    save_closure_analysis(str(tmp_path), max_denominator=10)

    md_path = tmp_path / "lissajous-phase-closure.md"
    assert md_path.exists()
    content = md_path.read_text()
    assert "Lissajous Phase Closure Analysis" in content
    assert "2_3_5_smooth" in content

    # Check at least one SVG was created
    svgs = list(tmp_path.glob("*.svg"))
    assert len(svgs) > 0


# Ensure pytest can find tests
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])