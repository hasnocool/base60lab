"""Tests for frequency module - comprehensive coverage."""

import pytest

from base60lab.core.rational import Rational
from base60lab.frequency import (
    ratio_to_fraction,
    FrequencyRatio,
    Harmonic,
    Phase,
)
def test_ratio_to_fraction_basic():
    """Test ratio_to_fraction returns Rational for basic ratios."""
    from base60lab.frequency import ratio_to_fraction
    from base60lab.core.rational import Rational

    # Test unison 1:1
    result = ratio_to_fraction(1, 1)
    assert isinstance(result, Rational)
    assert result == Rational(1, 1)

    # Test octave 2:1
    result = ratio_to_fraction(2, 1)
    assert isinstance(result, Rational)
    assert result == Rational(2, 1)
    assert str(result) == "Rational(2)"


def test_ratio_to_fraction_musical_intervals():
    """Test ratio_to_fraction for standard musical intervals."""
    from base60lab.frequency import ratio_to_fraction
    from base60lab.core.rational import Rational

    # Perfect fifth 3:2
    assert ratio_to_fraction(3, 2) == Rational(3, 2)

    # Perfect fourth 4:3
    assert ratio_to_fraction(4, 3) == Rational(4, 3)

    # Major third 5:4
    assert ratio_to_fraction(5, 4) == Rational(5, 4)

    # Major sixth 5:3
    assert ratio_to_fraction(5, 3) == Rational(5, 3)


def test_ratio_to_fraction_invalid_numerator():
    """Test ratio_to_fraction raises ValueError for non-positive numerator."""
    from base60lab.frequency import ratio_to_fraction

    with pytest.raises(ValueError, match="numerator must be positive"):
        ratio_to_fraction(0, 1)

    with pytest.raises(ValueError, match="numerator must be positive"):
        ratio_to_fraction(-1, 1)

    with pytest.raises(ValueError, match="numerator must be positive"):
        ratio_to_fraction(-5, 2)


def test_ratio_to_fraction_invalid_denominator():
    """Test ratio_to_fraction raises ValueError for non-positive denominator."""
    from base60lab.frequency import ratio_to_fraction

    with pytest.raises(ValueError, match="denominator must be positive"):
        ratio_to_fraction(1, 0)

    with pytest.raises(ValueError, match="denominator must be positive"):
        ratio_to_fraction(1, -1)

    with pytest.raises(ValueError, match="denominator must be positive"):
        ratio_to_fraction(3, -2)


def test_frequency_ratio_class():
    """Test FrequencyRatio class for exact rational ratios."""
    from base60lab.frequency import FrequencyRatio
    from base60lab.core.rational import Rational

    # Create from numerator/denominator
    ratio = FrequencyRatio(3, 2)
    assert ratio.numerator == 3
    assert ratio.denominator == 2
    assert ratio.value == Rational(3, 2)

    # Create from Rational
    ratio = FrequencyRatio(Rational(4, 3))
    assert ratio.value == Rational(4, 3)

    # String representation
    assert str(FrequencyRatio(2, 1)) == "2:1"
    assert str(FrequencyRatio(3, 2)) == "3:2"


def test_frequency_ratio_init_errors():
    """Test FrequencyRatio initialization errors."""
    from base60lab.frequency import FrequencyRatio
    from base60lab.core.rational import Rational

    # Zero denominator
    with pytest.raises(ZeroDivisionError, match="denominator cannot be zero"):
        FrequencyRatio(1, 0)

    # Negative denominator
    with pytest.raises(ValueError, match="denominator must be positive"):
        FrequencyRatio(1, -1)

    # Negative numerator
    with pytest.raises(ValueError, match="numerator must be positive"):
        FrequencyRatio(-1, 1)

    # Zero numerator
    with pytest.raises(ValueError, match="numerator must be positive"):
        FrequencyRatio(0, 1)

    # Negative denominator with Rational should also work via Rational path
    # This tests the Rational path in __init__
    ratio = FrequencyRatio(Rational(1, -2))  # Rational normalizes sign
    assert ratio.value == Rational(-1, 2)


def test_frequency_ratio_arithmetic():
    """Test FrequencyRatio arithmetic operations."""
    from base60lab.frequency import FrequencyRatio
    from base60lab.core.rational import Rational

    r1 = FrequencyRatio(3, 2)  # perfect fifth
    r2 = FrequencyRatio(4, 3)  # perfect fourth

    # Multiplication: fifth * fourth = octave
    product = r1 * r2
    assert isinstance(product, FrequencyRatio)
    assert product.value == Rational(2, 1)

    # Division: fifth / fourth = major tone (9:8)
    quotient = r1 / r2
    assert isinstance(quotient, FrequencyRatio)
    assert quotient.value == Rational(9, 8)

    # Power: octave squared = double octave
    octave = FrequencyRatio(2, 1)
    double_octave = octave ** 2
    assert double_octave.value == Rational(4, 1)

    # Power with negative exponent
    half_octave = octave ** -1
    assert half_octave.value == Rational(1, 2)

    # Power with zero exponent
    unison = octave ** 0
    assert unison.value == Rational(1, 1)


def test_frequency_ratio_mul_not_implemented():
    """Test FrequencyRatio.__mul__ returns NotImplemented for non-FrequencyRatio."""
    from base60lab.frequency import FrequencyRatio

    r = FrequencyRatio(3, 2)
    result = r.__mul__("not a ratio")
    assert result is NotImplemented

    result = r.__mul__(42)
    assert result is NotImplemented

    result = r.__mul__(None)
    assert result is NotImplemented


def test_frequency_ratio_div_not_implemented():
    """Test FrequencyRatio.__truediv__ returns NotImplemented for non-FrequencyRatio."""
    from base60lab.frequency import FrequencyRatio

    r = FrequencyRatio(3, 2)
    result = r.__truediv__("not a ratio")
    assert result is NotImplemented

    result = r.__truediv__(42)
    assert result is NotImplemented


def test_frequency_ratio_eq_not_implemented():
    """Test FrequencyRatio.__eq__ returns NotImplemented for non-FrequencyRatio."""
    from base60lab.frequency import FrequencyRatio

    r = FrequencyRatio(3, 2)
    result = r.__eq__("not a ratio")
    assert result is NotImplemented

    result = r.__eq__(42)
    assert result is NotImplemented

    result = r.__eq__(None)
    assert result is NotImplemented


def test_frequency_ratio_hash():
    """Test FrequencyRatio.__hash__."""
    from base60lab.frequency import FrequencyRatio

    r1 = FrequencyRatio(3, 2)
    r2 = FrequencyRatio(3, 2)
    r3 = FrequencyRatio(2, 1)

    # Equal ratios should have equal hashes
    assert hash(r1) == hash(r2)
    # Different ratios should have different hashes (with high probability)
    # Can't guarantee different, but can test it's an int
    assert isinstance(hash(r1), int)
    assert isinstance(hash(r3), int)

    # Can be used in sets/dicts
    s = {r1, r2, r3}
    assert len(s) == 2  # r1 and r2 are equal
    d = {r1: "fifth"}
    assert d[r2] == "fifth"


def test_frequency_ratio_repr():
    """Test FrequencyRatio.__repr__."""
    from base60lab.frequency import FrequencyRatio

    r = FrequencyRatio(3, 2)
    assert repr(r) == "FrequencyRatio(3, 2)"

    r2 = FrequencyRatio(5, 4)
    assert repr(r2) == "FrequencyRatio(5, 4)"


def test_frequency_ratio_class_constants():
    """Test FrequencyRatio class constants for musical intervals."""
    from base60lab.frequency import FrequencyRatio
    from base60lab.core.rational import Rational

    assert FrequencyRatio.UNISON.value == Rational(1, 1)
    assert FrequencyRatio.OCTAVE.value == Rational(2, 1)
    assert FrequencyRatio.PERFECT_FIFTH.value == Rational(3, 2)
    assert FrequencyRatio.PERFECT_FOURTH.value == Rational(4, 3)
    assert FrequencyRatio.MAJOR_THIRD.value == Rational(5, 4)
    assert FrequencyRatio.MAJOR_SIXTH.value == Rational(5, 3)
    assert FrequencyRatio.MINOR_THIRD.value == Rational(6, 5)
    assert FrequencyRatio.MINOR_SIXTH.value == Rational(8, 5)
    assert FrequencyRatio.MAJOR_SECOND.value == Rational(9, 8)
    assert FrequencyRatio.MINOR_SECOND.value == Rational(16, 15)
    assert FrequencyRatio.TRITONE.value == Rational(45, 32)

    # Test they are FrequencyRatio instances
    assert isinstance(FrequencyRatio.UNISON, FrequencyRatio)
    assert isinstance(FrequencyRatio.OCTAVE, FrequencyRatio)

    # Test string representations
    assert str(FrequencyRatio.UNISON) == "1:1"
    assert str(FrequencyRatio.OCTAVE) == "2:1"
    assert str(FrequencyRatio.PERFECT_FIFTH) == "3:2"


def test_harmonic_waveform():
    """Test Harmonic class for harmonic waveforms."""
    from base60lab.frequency import Harmonic, FrequencyRatio
    from base60lab.core.rational import Rational

    # Fundamental (1st harmonic)
    h1 = Harmonic(1)
    assert h1.number == 1
    assert h1.ratio == FrequencyRatio(1, 1)
    assert h1.ratio.value == Rational(1, 1)

    # 2nd harmonic (octave)
    h2 = Harmonic(2)
    assert h2.number == 2
    assert h2.ratio == FrequencyRatio(2, 1)

    # 3rd harmonic (octave + fifth)
    h3 = Harmonic(3)
    assert h3.number == 3
    assert h3.ratio == FrequencyRatio(3, 1)

    # Harmonic series up to N
    harmonics = Harmonic.series(5)
    assert len(harmonics) == 5
    assert [h.number for h in harmonics] == [1, 2, 3, 4, 5]
    assert [h.ratio.value for h in harmonics] == [
        Rational(1, 1),
        Rational(2, 1),
        Rational(3, 1),
        Rational(4, 1),
        Rational(5, 1),
    ]


def test_harmonic_errors():
    """Test Harmonic validation errors."""
    from base60lab.frequency import Harmonic

    # Zero harmonic number
    with pytest.raises(ValueError, match="harmonic number must be positive"):
        Harmonic(0)

    # Negative harmonic number
    with pytest.raises(ValueError, match="harmonic number must be positive"):
        Harmonic(-1)


def test_harmonic_series_errors():
    """Test Harmonic.series validation errors."""
    from base60lab.frequency import Harmonic

    # Zero count
    with pytest.raises(ValueError, match="count must be positive"):
        Harmonic.series(0)

    # Negative count
    with pytest.raises(ValueError, match="count must be positive"):
        Harmonic.series(-1)

    # Negative count larger magnitude
    with pytest.raises(ValueError, match="count must be positive"):
        Harmonic.series(-5)


def test_harmonic_str_repr():
    """Test Harmonic __str__ and __repr__."""
    from base60lab.frequency import Harmonic

    h = Harmonic(1)
    assert str(h) == "Harmonic(1)"
    assert repr(h) == "Harmonic(1)"

    h2 = Harmonic(42)
    assert str(h2) == "Harmonic(42)"
    assert repr(h2) == "Harmonic(42)"


def test_phase_as_fraction():
    """Test Phase class representing fraction of complete turn."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    # Phase as rational fraction of turn
    p = Phase(Rational(1, 4))  # quarter turn (90 degrees)
    assert p.value == Rational(1, 4)

    # Phase from numerator/denominator
    p = Phase(1, 2)  # half turn (180 degrees)
    assert p.value == Rational(1, 2)

    # Phase arithmetic (mod 1)
    p1 = Phase(1, 4)
    p2 = Phase(1, 2)
    p3 = p1 + p2
    assert p3.value == Rational(3, 4)

    # Full turn wraps to 0
    p_full = Phase(1, 1)
    assert p_full.value == Rational(0, 1)

    # Negative phase wraps
    p_neg = Phase(-1, 4)
    assert p_neg.value == Rational(3, 4)

    # Phase greater than 1 wraps
    p_wrap = Phase(5, 4)
    assert p_wrap.value == Rational(1, 4)


def test_phase_init_errors():
    """Test Phase initialization errors."""
    from base60lab.frequency import Phase

    # Zero denominator
    with pytest.raises(ValueError, match="denominator must be positive"):
        Phase(1, 0)

    # Negative denominator
    with pytest.raises(ValueError, match="denominator must be positive"):
        Phase(1, -1)


def test_phase_properties():
    """Test Phase numerator and denominator properties."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    p = Phase(3, 8)
    assert p.numerator == 3
    assert p.denominator == 8

    # Test with Rational input
    p2 = Phase(Rational(5, 12))
    assert p2.numerator == 5
    assert p2.denominator == 12

    # Test zero phase
    p_zero = Phase(0, 1)
    assert p_zero.numerator == 0
    assert p_zero.denominator == 1


def test_phase_add():
    """Test Phase addition."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    p1 = Phase(1, 4)
    p2 = Phase(1, 3)
    p3 = p1 + p2
    assert p3.value == Rational(7, 12)

    # Adding zero
    p_zero = Phase.ZERO
    p4 = p1 + p_zero
    assert p4.value == p1.value

    # Wrap around
    p5 = Phase(3, 4) + Phase(1, 2)
    assert p5.value == Rational(1, 4)


def test_phase_add_not_implemented():
    """Test Phase.__add__ returns NotImplemented for non-Phase."""
    from base60lab.frequency import Phase

    p = Phase(1, 4)
    result = p.__add__("not a phase")
    assert result is NotImplemented

    result = p.__add__(42)
    assert result is NotImplemented

    result = p.__add__(None)
    assert result is NotImplemented


def test_phase_sub():
    """Test Phase subtraction."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    p1 = Phase(3, 4)
    p2 = Phase(1, 4)
    p3 = p1 - p2
    assert p3.value == Rational(1, 2)

    # Subtracting larger phase wraps
    p4 = Phase(1, 4) - Phase(3, 4)
    assert p4.value == Rational(1, 2)

    # Subtracting zero
    p_zero = Phase.ZERO
    p5 = p1 - p_zero
    assert p5.value == p1.value


def test_phase_sub_not_implemented():
    """Test Phase.__sub__ returns NotImplemented for non-Phase."""
    from base60lab.frequency import Phase

    p = Phase(1, 4)
    result = p.__sub__("not a phase")
    assert result is NotImplemented

    result = p.__sub__(42)
    assert result is NotImplemented


def test_phase_mul():
    """Test Phase multiplication by integer."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    p = Phase(1, 4)
    p2 = p * 2
    assert p2.value == Rational(1, 2)

    p3 = p * 3
    assert p3.value == Rational(3, 4)

    p4 = p * 4
    assert p4.value == Rational(0, 1)  # wraps to 0

    # Negative multiplier
    p5 = p * -1
    assert p5.value == Rational(3, 4)

    # Zero multiplier
    p6 = p * 0
    assert p6.value == Rational(0, 1)


def test_phase_mul_not_implemented():
    """Test Phase.__mul__ returns NotImplemented for non-int."""
    from base60lab.frequency import Phase

    p = Phase(1, 4)
    result = p.__mul__("not an int")
    assert result is NotImplemented

    result = p.__mul__(1.5)
    assert result is NotImplemented

    result = p.__mul__(None)
    assert result is NotImplemented


def test_phase_eq():
    """Test Phase equality."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    p1 = Phase(1, 4)
    p2 = Phase(1, 4)
    p3 = Phase(2, 8)  # equivalent
    p4 = Phase(1, 2)

    assert p1 == p2
    assert p1 == p3  # equivalent rationals
    assert not (p1 == p4)

    # Equal with different representations
    p5 = Phase(Rational(1, 4))
    assert p1 == p5


def test_phase_eq_not_implemented():
    """Test Phase.__eq__ returns NotImplemented for non-Phase."""
    from base60lab.frequency import Phase

    p = Phase(1, 4)
    result = p.__eq__("not a phase")
    assert result is NotImplemented

    result = p.__eq__(42)
    assert result is NotImplemented

    result = p.__eq__(None)
    assert result is NotImplemented


def test_phase_hash():
    """Test Phase.__hash__."""
    from base60lab.frequency import Phase

    p1 = Phase(1, 4)
    p2 = Phase(1, 4)
    p3 = Phase(1, 2)

    # Equal phases should have equal hashes
    assert hash(p1) == hash(p2)
    # Different phases should have different hashes (with high probability)
    assert isinstance(hash(p1), int)
    assert isinstance(hash(p3), int)

    # Can be used in sets/dicts
    s = {p1, p2, p3}
    assert len(s) == 2  # p1 and p2 are equal
    d = {p1: "quarter"}
    assert d[p2] == "quarter"


def test_phase_str():
    """Test Phase __str__ various branches."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    # Zero phase
    p_zero = Phase(0, 1)
    assert str(p_zero) == "Phase(0)"

    # Phase with denominator 1
    p_one = Phase(1, 1)
    assert str(p_one) == "Phase(0)"  # wraps to 0

    # Phase with numerator != 0, denominator == 1 (after normalization)
    p_half = Phase(1, 2)
    assert str(p_half) == "Phase(1/2)"

    # Phase with both numerator and denominator != 1
    p_third = Phase(1, 3)
    assert str(p_third) == "Phase(1/3)"

    # Using Rational input
    p_quarter = Phase(Rational(1, 4))
    assert str(p_quarter) == "Phase(1/4)"


def test_phase_repr():
    """Test Phase __repr__."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    p = Phase(1, 4)
    assert repr(p) == "Phase(1, 4)"

    p2 = Phase(Rational(3, 8))
    assert repr(p2) == "Phase(3, 8)"

    p_zero = Phase(0, 1)
    assert repr(p_zero) == "Phase(0, 1)"


def test_phase_to_frequency_ratio():
    """Test converting phase to frequency ratio (for angular frequency)."""
    from base60lab.frequency import Phase, FrequencyRatio
    from base60lab.core.rational import Rational

    # Phase per sample at sample rate gives frequency ratio
    phase_per_sample = Phase(1, 100)  # 1/100 turn per sample
    # At 100 samples per turn, frequency = 1 turn per 100 samples = 1/100
    freq_ratio = phase_per_sample.to_frequency_ratio(100)
    assert freq_ratio.value == Rational(1, 100)

    # Different samples per turn
    phase_per_sample2 = Phase(1, 4)
    freq_ratio2 = phase_per_sample2.to_frequency_ratio(4)
    assert freq_ratio2.value == Rational(1, 4)


def test_phase_to_frequency_ratio_error():
    """Test Phase.to_frequency_ratio with invalid samples_per_turn."""
    from base60lab.frequency import Phase

    p = Phase(1, 4)
    with pytest.raises(ValueError, match="samples_per_turn must be positive"):
        p.to_frequency_ratio(0)

    with pytest.raises(ValueError, match="samples_per_turn must be positive"):
        p.to_frequency_ratio(-1)

    with pytest.raises(ValueError, match="samples_per_turn must be positive"):
        p.to_frequency_ratio(-100)


def test_phase_to_degrees():
    """Test Phase.to_degrees conversion."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    p = Phase(1, 4)  # 90 degrees
    assert p.to_degrees() == Rational(90)

    p = Phase(1, 2)  # 180 degrees
    assert p.to_degrees() == Rational(180)

    p = Phase(3, 4)  # 270 degrees
    assert p.to_degrees() == Rational(270)

    p = Phase(1, 1)  # 360 degrees = 0
    assert p.to_degrees() == Rational(0)

    p = Phase(1, 8)  # 45 degrees
    assert p.to_degrees() == Rational(45)


def test_phase_to_radians():
    """Test Phase.to_radians conversion (as rational multiple of π)."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    p = Phase(1, 4)  # π/2 radians -> returns 1/2 (multiple of π)
    assert p.to_radians() == Rational(1, 2)

    p = Phase(1, 2)  # π radians -> returns 1
    assert p.to_radians() == Rational(1)

    p = Phase(3, 4)  # 3π/2 radians -> returns 3/2
    assert p.to_radians() == Rational(3, 2)

    p = Phase(1, 1)  # 2π radians -> returns 2, but phase wraps to 0
    assert p.to_radians() == Rational(0)

    p = Phase(1, 8)  # π/4 radians -> returns 1/4
    assert p.to_radians() == Rational(1, 4)


def test_phase_class_constants():
    """Test Phase class constants."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    assert Phase.ZERO.value == Rational(0, 1)
    assert Phase.QUARTER_TURN.value == Rational(1, 4)
    assert Phase.HALF_TURN.value == Rational(1, 2)
    assert Phase.THREE_QUARTER_TURN.value == Rational(3, 4)
    assert Phase.FULL_TURN.value == Rational(0, 1)  # wraps to 0

    # Test they are Phase instances
    assert isinstance(Phase.ZERO, Phase)
    assert isinstance(Phase.QUARTER_TURN, Phase)

    # Test string representations
    assert str(Phase.ZERO) == "Phase(0)"
    assert str(Phase.QUARTER_TURN) == "Phase(1/4)"
    assert str(Phase.HALF_TURN) == "Phase(1/2)"
    assert str(Phase.THREE_QUARTER_TURN) == "Phase(3/4)"


def test_invalid_inputs():
    """Test that invalid inputs raise appropriate errors."""
    from base60lab.frequency import FrequencyRatio, Harmonic, Phase

    # Zero denominator
    with pytest.raises(ZeroDivisionError):
        FrequencyRatio(1, 0)

    # Negative frequency (numerator)
    with pytest.raises(ValueError):
        FrequencyRatio(-1, 1)

    # Zero harmonic number
    with pytest.raises(ValueError):
        Harmonic(0)

    # Negative harmonic number
    with pytest.raises(ValueError):
        Harmonic(-1)


def test_no_floating_point_internal():
    """Verify no floating-point is used internally."""
    from base60lab.frequency import ratio_to_fraction, FrequencyRatio, Harmonic, Phase
    from base60lab.core.rational import Rational

    # All operations should return Rational, never float
    result = ratio_to_fraction(3, 2)
    assert isinstance(result, Rational)
    assert not isinstance(result, float)

    ratio = FrequencyRatio(5, 4)
    assert isinstance(ratio.value, Rational)

    harmonic = Harmonic(3)
    assert isinstance(harmonic.ratio.value, Rational)

    phase = Phase(1, 3)
    assert isinstance(phase.value, Rational)


def test_frequency_ratio_comparison():
    """Test FrequencyRatio comparison operators (order=True)."""
    from base60lab.frequency import FrequencyRatio

    r1 = FrequencyRatio(1, 2)
    r2 = FrequencyRatio(2, 3)
    r3 = FrequencyRatio(3, 4)

    # Order by value
    assert r1 < r2 < r3
    assert r3 > r2 > r1
    assert r1 <= r2
    assert r2 >= r1


def test_harmonic_comparison():
    """Test Harmonic comparison operators (order=True)."""
    from base60lab.frequency import Harmonic

    h1 = Harmonic(1)
    h2 = Harmonic(2)
    h3 = Harmonic(3)

    # Order by number
    assert h1 < h2 < h3
    assert h3 > h2 > h1
    assert h1 <= h2
    assert h2 >= h1


def test_phase_comparison():
    """Test Phase comparison operators (order=True)."""
    from base60lab.frequency import Phase

    p1 = Phase(1, 4)
    p2 = Phase(1, 2)
    p3 = Phase(3, 4)

    # Order by value
    assert p1 < p2 < p3
    assert p3 > p2 > p1
    assert p1 <= p2
    assert p2 >= p1


def test_complex_frequency_ratio_operations():
    """Test complex FrequencyRatio operations."""
    from base60lab.frequency import FrequencyRatio
    from base60lab.core.rational import Rational

    # Chain operations
    fifth = FrequencyRatio.PERFECT_FIFTH
    fourth = FrequencyRatio.PERFECT_FOURTH
    major_third = FrequencyRatio.MAJOR_THIRD

    # Fifth * fourth = octave
    assert (fifth * fourth).value == Rational(2, 1)

    # Octave / fifth = fourth
    octave = FrequencyRatio.OCTAVE
    assert (octave / fifth).value == fourth.value

    # Major third ^ 2 = 25/16
    assert (major_third ** 2).value == Rational(25, 16)

    # Major third ^ 3 = 125/64
    assert (major_third ** 3).value == Rational(125, 64)


def test_phase_edge_cases():
    """Test Phase edge cases and normalization."""
    from base60lab.frequency import Phase
    from base60lab.core.rational import Rational

    # Very large numerator normalizes
    p = Phase(101, 4)  # 25.25 turns -> 1/4 turn
    assert p.value == Rational(1, 4)

    # Large negative numerator
    p = Phase(-101, 4)
    assert p.value == Rational(3, 4)

    # Multiple wraps
    p = Phase(17, 4)
    assert p.value == Rational(1, 4)

    # Using Rational that's > 1
    p = Phase(Rational(9, 4))
    assert p.value == Rational(1, 4)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])