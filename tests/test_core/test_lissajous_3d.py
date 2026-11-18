"""Tests for 3D Lissajous figures module."""

from base60lab.core.rational import Rational
from base60lab.lissajous import (
    Lissajous3DParameters,
    ClosureInfo3D,
    is_closed_3d,
    closure_info_3d,
    diophantine_approximation_quality,
    generate_lissajous_3d_points,
    plot_lissajous_3d,
    analyze_kam_diophantine_conditions,
    compare_denominator_families,
    classify_denominator,
    prime_factors,
)

import pytest
import numpy as np


# --- Lissajous3DParameters tests ---

def test_lissajous3d_parameters_creation():
    """Lissajous3DParameters can be created with all fields."""
    params = Lissajous3DParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        freq_z=Rational(1),
        phase_xy=Rational(1, 4),
        phase_xz=Rational(1, 2),
        amplitude_x=Rational(2),
        amplitude_y=Rational(3),
        amplitude_z=Rational(4),
    )
    assert params.freq_x == Rational(3)
    assert params.freq_y == Rational(2)
    assert params.freq_z == Rational(1)
    assert params.phase_xy == Rational(1, 4)
    assert params.phase_xz == Rational(1, 2)
    assert params.amplitude_x == Rational(2)
    assert params.amplitude_y == Rational(3)
    assert params.amplitude_z == Rational(4)


def test_lissajous3d_parameters_defaults():
    """Lissajous3DParameters uses correct defaults for optional fields."""
    params = Lissajous3DParameters(
        freq_x=Rational(1),
        freq_y=Rational(1),
        freq_z=Rational(1),
    )
    assert params.phase_xy == Rational(0)
    assert params.phase_xz == Rational(0)
    assert params.amplitude_x == Rational(1)
    assert params.amplitude_y == Rational(1)
    assert params.amplitude_z == Rational(1)


def test_lissajous3d_parameters_frequency_ratios():
    """frequency_ratios returns correct pairwise ratios."""
    params = Lissajous3DParameters(
        freq_x=Rational(6),
        freq_y=Rational(4),
        freq_z=Rational(3),
    )
    ratio_xy, ratio_xz = params.frequency_ratios()
    assert ratio_xy == Rational(6, 4)  # 3/2
    assert ratio_xz == Rational(6, 3)  # 2/1


def test_lissajous3d_parameters_all_ratios_rational():
    """all_ratios_rational returns True (by construction with Rational)."""
    params = Lissajous3DParameters(
        freq_x=Rational(7),
        freq_y=Rational(5),
        freq_z=Rational(3),
    )
    assert params.all_ratios_rational() is True


def test_lissajous3d_parameters_immutable():
    """Lissajous3DParameters is frozen (immutable)."""
    params = Lissajous3DParameters(
        freq_x=Rational(1),
        freq_y=Rational(1),
        freq_z=Rational(1),
    )
    with pytest.raises(Exception):  # dataclass frozen raises FrozenInstanceError
        params.freq_x = Rational(2)


# --- ClosureInfo3D tests ---

def test_closure_info3d_creation():
    """ClosureInfo3D can be created with all fields."""
    info = ClosureInfo3D(
        is_closed=True,
        closure_period=12,
        ratios=(Rational(3, 2), Rational(2, 1)),
        denominators=(2, 1),
        lcm_denominator=2,
        factorization={2: 1},
        prime_class="2_3_5_smooth",
        diophantine_quality=0.05,
    )
    assert info.is_closed is True
    assert info.closure_period == 12
    assert info.ratios == (Rational(3, 2), Rational(2, 1))
    assert info.denominators == (2, 1)
    assert info.lcm_denominator == 2
    assert info.factorization == {2: 1}
    assert info.prime_class == "2_3_5_smooth"
    assert info.diophantine_quality == 0.05


def test_closure_info3d_str_closed():
    """ClosureInfo3D string representation for closed figures."""
    info = ClosureInfo3D(
        is_closed=True,
        closure_period=6,
        ratios=(Rational(3, 2), Rational(4, 3)),
        denominators=(2, 3),
        lcm_denominator=6,
        factorization={2: 1, 3: 1},
        prime_class="2_3_5_smooth",
        diophantine_quality=0.0,
    )
    s = str(info)
    assert "Closed on 3-torus" in s
    assert "period=6" in s
    assert "3/2" in s or "Rational(3, 2)" in s
    assert "6" in s  # LCM denominator
    assert "2_3_5_smooth" in s


def test_closure_info3d_str_not_closed():
    """ClosureInfo3D string representation for non-closed figures."""
    info = ClosureInfo3D(
        is_closed=False,
        closure_period=None,
        ratios=(Rational(1), Rational(1)),
        denominators=(1, 1),
        lcm_denominator=1,
        factorization={},
        prime_class="2_3_5_smooth",
        diophantine_quality=None,
    )
    s = str(info)
    assert "Not closed" in s


def test_closure_info3d_immutable():
    """ClosureInfo3D is frozen (immutable)."""
    info = ClosureInfo3D(
        is_closed=True,
        closure_period=6,
        ratios=(Rational(1), Rational(1)),
        denominators=(1, 1),
        lcm_denominator=1,
        factorization={},
        prime_class="2_3_5_smooth",
        diophantine_quality=0.0,
    )
    with pytest.raises(Exception):
        info.is_closed = False


# --- is_closed_3d tests ---

def test_is_closed_3d_true_for_rational_ratios():
    """3D Lissajous figure with rational frequency ratios is closed."""
    assert is_closed_3d(3, 2, 1) is True
    assert is_closed_3d(6, 4, 3) is True
    assert is_closed_3d(Rational(5), Rational(3), Rational(2)) is True


def test_is_closed_3d_with_rational_objects():
    """is_closed_3d works with Rational objects."""
    assert is_closed_3d(Rational(7), Rational(5), Rational(3)) is True
    assert is_closed_3d(Rational(2, 3), Rational(1, 2), Rational(1, 5)) is True


def test_is_closed_3d_zero_frequency_y_raises():
    """Zero frequency in y direction raises ValueError."""
    with pytest.raises(ValueError, match="cannot be zero"):
        is_closed_3d(1, 0, 1)


def test_is_closed_3d_zero_frequency_z_raises():
    """Zero frequency in z direction raises ValueError."""
    with pytest.raises(ValueError, match="cannot be zero"):
        is_closed_3d(1, 1, 0)


def test_is_closed_3d_negative_frequencies():
    """Negative frequencies work (ratio sign doesn't affect closure)."""
    assert is_closed_3d(-3, 2, 1) is True
    assert is_closed_3d(3, -2, 1) is True
    assert is_closed_3d(3, 2, -1) is True
    assert is_closed_3d(-3, -2, -1) is True


# --- closure_info_3d tests ---

def test_closure_info_3d_basic():
    """closure_info_3d returns correct closure information for simple ratios."""
    info = closure_info_3d(3, 2, 1)
    assert info.is_closed is True
    assert info.closure_period == 2  # LCM of denominators of 3/2 and 3/1
    assert info.ratios == (Rational(3, 2), Rational(3, 1))
    assert info.denominators == (2, 1)
    assert info.lcm_denominator == 2
    assert info.factorization == {2: 1}
    assert info.prime_class == "2_3_5_smooth"


def test_closure_info_3d_reduced_fractions():
    """closure_info_3d reduces fractions before computing LCM."""
    # 6/4 = 3/2, 6/3 = 2/1
    info = closure_info_3d(6, 4, 3)
    assert info.ratios == (Rational(3, 2), Rational(2, 1))
    assert info.denominators == (2, 1)
    assert info.lcm_denominator == 2
def test_closure_info_3d_multiple_prime_factors():
    """closure_info_3d correctly computes prime factorization for multiple primes."""
    # fx=6, fy=5, fz=7 -> ratios: 6/5, 6/7
    # denominators: 5, 7 -> LCM = 35 = 5*7
    # 35 has primes {5, 7} which is mixed (not pure 2_3_5 or 7_11_13)
    info = closure_info_3d(6, 5, 7)
    assert info.denominators == (5, 7)
    assert info.lcm_denominator == 35
    assert info.factorization == {5: 1, 7: 1}
    assert info.prime_class == "mixed"  # 5 and 7 together = mixed
    # fx=30, fy=7, fz=11 -> denominators: 7, 11 -> LCM = 77 = 7*11
    info = closure_info_3d(30, 7, 11)
    assert info.lcm_denominator == 77
    assert info.factorization == {7: 1, 11: 1}
    assert info.prime_class == "prime_7_11_13"


def test_closure_info_3d_complex_lcm():
    """closure_info_3d handles complex LCM calculations."""
    # fx=12, fy=8, fz=9 -> ratios: 12/8=3/2, 12/9=4/3
    # denominators: 2, 3 -> LCM = 6
    info = closure_info_3d(12, 8, 9)
    assert info.ratios == (Rational(3, 2), Rational(4, 3))
    assert info.denominators == (2, 3)
    assert info.lcm_denominator == 6
    assert info.factorization == {2: 1, 3: 1}
    assert info.closure_period == 6


def test_closure_info_3d_zero_frequency_raises():
    """closure_info_3d raises ValueError for zero frequency."""
    with pytest.raises(ValueError, match="cannot be zero"):
        closure_info_3d(1, 0, 1)
    with pytest.raises(ValueError, match="cannot be zero"):
        closure_info_3d(1, 1, 0)


# --- diophantine_approximation_quality tests ---

def test_diophantine_approximation_quality_returns_float():
    """diophantine_approximation_quality returns a float."""
    quality = diophantine_approximation_quality(3, 2, 1)
    assert isinstance(quality, float)


def test_diophantine_approximation_quality_range():
    """diophantine_approximation_quality returns value >= 0."""
    quality = diophantine_approximation_quality(3, 2, 1, max_denominator=100)
    assert quality >= 0.0


def test_diophantine_approximation_quality_exact_ratios():
    """For exact rational ratios, quality should be very small (exactly representable)."""
    # 3:2:1 -> exact rational ratios, should have quality 0 or very close
    quality = diophantine_approximation_quality(3, 2, 1, max_denominator=100)
    # Since ratios are exactly representable with denominator <= max_denominator
    # the distance should be 0
    assert quality == 0.0 or quality < 1e-10


def test_diophantine_approximation_quality_with_rational_objects():
    """diophantine_approximation_quality works with Rational objects."""
    quality = diophantine_approximation_quality(
        Rational(5), Rational(3), Rational(2), max_denominator=50
    )
    assert isinstance(quality, float)
    assert quality >= 0.0


def test_diophantine_approximation_quality_zero_fx():
    """diophantine_approximation_quality returns inf for zero fx."""
    quality = diophantine_approximation_quality(0, 1, 1)
    assert quality == float('inf')


def test_diophantine_approximation_quality_different_max_denominator():
    """Quality improves (decreases) with larger max_denominator."""
    quality_small = diophantine_approximation_quality(5, 3, 2, max_denominator=10)
    quality_large = diophantine_approximation_quality(5, 3, 2, max_denominator=100)
    assert quality_large <= quality_small


# --- generate_lissajous_3d_points tests ---

def test_generate_lissajous_3d_points_returns_correct_shape():
    """generate_lissajous_3d_points returns arrays of correct shape."""
    params = Lissajous3DParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        freq_z=Rational(1),
    )
    x, y, z = generate_lissajous_3d_points(params, num_points=100)
    assert x.shape == (100,)
    assert y.shape == (100,)
    assert z.shape == (100,)


def test_generate_lissajous_3d_points_default_num_points():
    """Default num_points is 2000."""
    params = Lissajous3DParameters(
        freq_x=Rational(1),
        freq_y=Rational(1),
        freq_z=Rational(1),
    )
    x, y, z = generate_lissajous_3d_points(params)
    assert x.shape == (2000,)
    assert y.shape == (2000,)
    assert z.shape == (2000,)


def test_generate_lissajous_3d_points_amplitude_scaling():
    """Amplitude parameters scale the output correctly."""
    params = Lissajous3DParameters(
        freq_x=Rational(1),
        freq_y=Rational(1),
        freq_z=Rational(1),
        amplitude_x=Rational(2),
        amplitude_y=Rational(3),
        amplitude_z=Rational(4),
    )
    x, y, z = generate_lissajous_3d_points(params, num_points=1000)
    assert np.max(np.abs(x)) <= 2.0 + 1e-10
    assert np.max(np.abs(y)) <= 3.0 + 1e-10
    assert np.max(np.abs(z)) <= 4.0 + 1e-10
    assert np.max(np.abs(x)) > 1.0  # Should reach near amplitude
    assert np.max(np.abs(y)) > 2.0
    assert np.max(np.abs(z)) > 3.0


def test_generate_lissajous_3d_points_phase_shift():
    """Phase parameters shift the output correctly."""
    params = Lissajous3DParameters(
        freq_x=Rational(1),
        freq_y=Rational(1),
        freq_z=Rational(1),
        phase_xy=Rational(1, 2),  # pi/2 shift
        phase_xz=Rational(1, 2),
    )
    x, y, z = generate_lissajous_3d_points(params, num_points=1000)
    # At t=0: x=0, y=sin(pi/2)=1, z=sin(pi/2)=1
    assert abs(x[0]) < 1e-10
    assert abs(y[0] - 1.0) < 1e-10
    assert abs(z[0] - 1.0) < 1e-10


def test_generate_lissajous_3d_points_deterministic():
    """Point generation is deterministic."""
    params = Lissajous3DParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        freq_z=Rational(1),
    )
    x1, y1, z1 = generate_lissajous_3d_points(params, num_points=500)
    x2, y2, z2 = generate_lissajous_3d_points(params, num_points=500)
    assert np.array_equal(x1, x2)
    assert np.array_equal(y1, y2)
    assert np.array_equal(z1, z2)


# --- plot_lissajous_3d tests ---

def test_plot_lissajous_3d_creates_figure(tmp_path):
    """plot_lissajous_3d creates and returns a matplotlib Figure."""
    params = Lissajous3DParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        freq_z=Rational(1),
    )
    fig = plot_lissajous_3d(params)
    import matplotlib.pyplot as plt
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_plot_lissajous_3d_saves_file(tmp_path):
    """plot_lissajous_3d saves figure to output_path."""
    params = Lissajous3DParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        freq_z=Rational(1),
    )
    output_path = tmp_path / "test_3d_plot.png"
    fig = plot_lissajous_3d(params, output_path=str(output_path))
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    import matplotlib.pyplot as plt
    plt.close(fig)


def test_plot_lissajous_3d_without_projections(tmp_path):
    """plot_lissajous_3d works with show_projections=False."""
    params = Lissajous3DParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        freq_z=Rational(1),
    )
    output_path = tmp_path / "test_3d_no_proj.png"
    fig = plot_lissajous_3d(params, output_path=str(output_path), show_projections=False)
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    import matplotlib.pyplot as plt
    plt.close(fig)


def test_plot_lissajous_3d_with_title(tmp_path):
    """plot_lissajous_3d accepts custom title."""
    params = Lissajous3DParameters(
        freq_x=Rational(3),
        freq_y=Rational(2),
        freq_z=Rational(1),
    )
    output_path = tmp_path / "test_3d_title.png"
    fig = plot_lissajous_3d(params, output_path=str(output_path), title="Test 3D Lissajous")
    assert output_path.exists()
    import matplotlib.pyplot as plt
    plt.close(fig)


# --- analyze_kam_diophantine_conditions tests ---

def test_analyze_kam_diophantine_conditions_returns_list():
    """analyze_kam_diophantine_conditions returns a list of dicts."""
    freq_triplets = [(3, 2, 1), (5, 3, 2), (7, 4, 3)]
    results = analyze_kam_diophantine_conditions(freq_triplets, max_denominator=100)
    assert isinstance(results, list)
    assert len(results) == 3


def test_analyze_kam_diophantine_conditions_dict_structure():
    """Each result dict has correct structure."""
    freq_triplets = [(3, 2, 1)]
    results = analyze_kam_diophantine_conditions(freq_triplets, max_denominator=100)
    result = results[0]
    assert "frequencies" in result
    assert "ratio_xy" in result
    assert "ratio_xz" in result
    assert "closure_info" in result
    assert "diophantine_quality" in result
    assert "prime_class" in result
    assert "lcm_denominator" in result
    assert "resonances" in result


def test_analyze_kam_diophantine_conditions_frequencies_preserved():
    """Input frequencies are preserved in results."""
    freq_triplets = [(7, 5, 3), (11, 7, 5)]
    results = analyze_kam_diophantine_conditions(freq_triplets, max_denominator=100)
    assert results[0]["frequencies"] == (7, 5, 3)
    assert results[1]["frequencies"] == (11, 7, 5)


def test_analyze_kam_diophantine_conditions_resonances():
    """Resonances list contains exact rational relations."""
    # 3:2:1 has resonance 1*2 + 1*1 = 1*3? No.
    # But 1*fy + (-1)*fz = 0*fx for 2,1? No.
    freq_triplets = [(3, 2, 1)]
    results = analyze_kam_diophantine_conditions(freq_triplets, max_denominator=100)
    resonances = results[0]["resonances"]
    assert isinstance(resonances, list)
    # At least check structure if any resonances found
    for r in resonances:
        assert "relation" in r
        assert "exact" in r
        assert r["exact"] is True


def test_analyze_kam_diophantine_conditions_quality_in_results():
    """Diophantine quality is included in results."""
    freq_triplets = [(3, 2, 1)]
    results = analyze_kam_diophantine_conditions(freq_triplets, max_denominator=100)
    quality = results[0]["diophantine_quality"]
    assert isinstance(quality, float)
    assert quality >= 0.0


def test_analyze_kam_diophantine_conditions_deterministic():
    """Results are deterministic across runs."""
    freq_triplets = [(5, 3, 2), (7, 4, 3)]
    results1 = analyze_kam_diophantine_conditions(freq_triplets, max_denominator=100)
    results2 = analyze_kam_diophantine_conditions(freq_triplets, max_denominator=100)
    assert len(results1) == len(results2)
    for r1, r2 in zip(results1, results2):
        assert r1["frequencies"] == r2["frequencies"]
        assert r1["ratio_xy"] == r2["ratio_xy"]
        assert r1["ratio_xz"] == r2["ratio_xz"]
        assert r1["prime_class"] == r2["prime_class"]
        assert r1["lcm_denominator"] == r2["lcm_denominator"]


# --- compare_denominator_families tests ---

def test_compare_denominator_families_returns_dict():
    """compare_denominator_families returns a dict with three families."""
    families = compare_denominator_families(max_freq=10)
    assert isinstance(families, dict)
    assert "2_3_5_smooth" in families
    assert "prime_7_11_13" in families
    assert "mixed" in families


def test_compare_denominator_families_all_lists():
    """Each family contains a list of results."""
    families = compare_denominator_families(max_freq=5)
    for family_name in ["2_3_5_smooth", "prime_7_11_13", "mixed"]:
        assert isinstance(families[family_name], list)


def test_compare_denominator_families_result_structure():
    """Each result has correct structure."""
    families = compare_denominator_families(max_freq=5)
    for family_results in families.values():
        for result in family_results:
            assert "frequencies" in result
            assert "ratio_xy" in result
            assert "ratio_xz" in result
            assert "closure_period" in result
            assert "lcm_denominator" in result
            assert "factorization" in result
            assert "prime_class" in result


def test_compare_denominator_families_categorization():
    """Results are correctly categorized by prime class."""
    families = compare_denominator_families(max_freq=10)
    for result in families["2_3_5_smooth"]:
        assert result["prime_class"] == "2_3_5_smooth"
    for result in families["prime_7_11_13"]:
        assert result["prime_class"] == "prime_7_11_13"
    for result in families["mixed"]:
        assert result["prime_class"] == "mixed"


def test_compare_denominator_families_max_freq():
    """max_freq limits the frequency range."""
    families_small = compare_denominator_families(max_freq=5)
    families_large = compare_denominator_families(max_freq=10)
    # More results with larger max_freq
    total_small = sum(len(v) for v in families_small.values())
    total_large = sum(len(v) for v in families_large.values())
    assert total_large > total_small


def test_compare_denominator_families_deterministic():
    """Results are deterministic."""
    families1 = compare_denominator_families(max_freq=10)
    families2 = compare_denominator_families(max_freq=10)
    for key in families1:
        assert len(families1[key]) == len(families2[key])
        for r1, r2 in zip(families1[key], families2[key]):
            assert r1["frequencies"] == r2["frequencies"]
            assert r1["ratio_xy"] == r2["ratio_xy"]
            assert r1["ratio_xz"] == r2["ratio_xz"]
            assert r1["closure_period"] == r2["closure_period"]
            assert r1["lcm_denominator"] == r2["lcm_denominator"]
            assert r1["factorization"] == r2["factorization"]
            assert r1["prime_class"] == r2["prime_class"]


# --- Exact rational arithmetic tests ---

def test_exact_rational_arithmetic_no_floats_in_computation():
    """All internal computations use exact Rational arithmetic."""
    # closure_info_3d should use only Rational internally
    # This is tested by checking that reduced fractions are used
    info = closure_info_3d(6, 4, 3)  # 6/4 = 3/2, 6/3 = 2/1
    # If floats were used, 6/4 might not reduce perfectly
    assert info.ratios == (Rational(3, 2), Rational(2, 1))
    assert info.lcm_denominator == 2


def test_exact_rational_arithmetic_large_numbers():
    """Exact arithmetic works with large numbers."""
    # Using large numbers that would lose precision in float
    info = closure_info_3d(1009, 1007, 1003)  # Large primes
    assert info.lcm_denominator == 1007 * 1003  # Since gcd(1009, 1007)=1, gcd(1009, 1003)=1
    assert info.factorization == {19: 1, 53: 1, 17: 1, 59: 1}  # 1007=19*53, 1003=17*59


def test_exact_rational_arithmetic_negative_denominators():
    """Rational handles negative denominators correctly."""
    info = closure_info_3d(-6, 4, 3)
    # -6/4 = -3/2, denominator is 2
    # -6/3 = -2/1, denominator is 1
    assert info.denominators == (2, 1)
    assert info.lcm_denominator == 2


def test_exact_rational_arithmetic_ratios():
    """Frequency ratios are computed exactly."""
    params = Lissajous3DParameters(
        freq_x=Rational(22, 7),
        freq_y=Rational(3),
        freq_z=Rational(5),
    )
    ratio_xy, ratio_xz = params.frequency_ratios()
    assert ratio_xy == Rational(22, 21)  # (22/7) / 3 = 22/21
    assert ratio_xz == Rational(22, 35)  # (22/7) / 5 = 22/35


# --- Edge case / adversarial tests ---

def test_zero_frequency_x_in_functions():
    """Functions handle zero frequency in x direction."""
    # closure_info_3d computes 0/fy = 0, 0/fz = 0 (valid Rational)
    info = closure_info_3d(0, 1, 1)
    assert info.is_closed is True
    # ratios are 0/1 = 0, denominators are 1
    assert info.ratios == (Rational(0), Rational(0))
    assert info.denominators == (1, 1)
    assert info.lcm_denominator == 1
    assert info.is_closed is True
    assert info.lcm_denominator > 0


def test_prime_factors_edge_cases():
    """prime_factors handles edge cases."""
    assert prime_factors(1) == {}
    assert prime_factors(2) == {2: 1}
    assert prime_factors(4) == {2: 2}
    assert prime_factors(60) == {2: 2, 3: 1, 5: 1}


def test_classify_denominator_edge_cases():
    """classify_denominator handles edge cases."""
    assert classify_denominator(1) == "2_3_5_smooth"
    assert classify_denominator(2) == "2_3_5_smooth"
    assert classify_denominator(3) == "2_3_5_smooth"
    assert classify_denominator(5) == "2_3_5_smooth"
    assert classify_denominator(7) == "prime_7_11_13"
    assert classify_denominator(11) == "prime_7_11_13"
    assert classify_denominator(13) == "prime_7_11_13"
    assert classify_denominator(17) == "mixed"
    assert classify_denominator(14) == "mixed"  # 2*7 = mixed (has 2 from smooth and 7 from prime group)


def test_all_3d_functions_deterministic():
    """All 3D functions produce deterministic results."""
    params = Lissajous3DParameters(
        freq_x=Rational(7),
        freq_y=Rational(5),
        freq_z=Rational(3),
    )
    # Multiple runs should produce identical results
    for _ in range(3):
        info1 = closure_info_3d(params.freq_x, params.freq_y, params.freq_z)
        info2 = closure_info_3d(params.freq_x, params.freq_y, params.freq_z)
        assert info1.closure_period == info2.closure_period
        assert info1.lcm_denominator == info2.lcm_denominator
        assert info1.factorization == info2.factorization
        
        quality1 = diophantine_approximation_quality(params.freq_x, params.freq_y, params.freq_z)
        quality2 = diophantine_approximation_quality(params.freq_x, params.freq_y, params.freq_z)
        assert quality1 == quality2
        
        x1, y1, z1 = generate_lissajous_3d_points(params, num_points=100)
        x2, y2, z2 = generate_lissajous_3d_points(params, num_points=100)
        assert np.array_equal(x1, x2)
        assert np.array_equal(y1, y2)
        assert np.array_equal(z1, z2)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])