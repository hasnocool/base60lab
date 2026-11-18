"""Tests for exact trigonometric values and identities across angle representations.

Baseline characterization: module doesn't exist → ImportError
Then failing-first proof tests that define expected behavior.
"""

import pytest
from base60lab.core.rational import Rational


# =============================================================================
# BASELINE CHARACTERIZATION TESTS (run first, expect ImportError before impl)
# =============================================================================

def test_module_imports():
    """Test that the trigonometry module can be imported."""
    from base60lab import trigonometry
    assert trigonometry is not None


def test_trigvalue_exists():
    """Test that TrigValue class exists."""
    from base60lab.trigonometry import TrigValue
    assert TrigValue is not None


# =============================================================================
# TRIGVALUE CLASS TESTS
# =============================================================================

def test_trigvalue_rational_creation():
    """Test TrigValue creation for rational values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2))
    assert v.is_rational()
    assert v.to_rational() == Rational(1, 2)
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 1


def test_trigvalue_algebraic_creation():
    """Test TrigValue creation for algebraic values (with sqrt)."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2), 2)  # √2/2
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 2


def test_trigvalue_simplification():
    """Test that TrigValue simplifies square factors in radicand."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # √4 = 2, so TrigValue(1, 4) should become TrigValue(2, 1)
    v = TrigValue(Rational(1), 4)
    assert v.is_rational()
    assert v.to_rational() == Rational(2)

    # √12 = 2√3
    v = TrigValue(Rational(1), 12)
    assert v.coeff == Rational(2)
    assert v.radicand == 3


def test_trigvalue_equality():
    """Test TrigValue equality comparison."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    assert TrigValue(Rational(1, 2)) == TrigValue(Rational(1, 2))
    assert TrigValue(Rational(1, 2), 2) == TrigValue(Rational(1, 2), 2)
    assert TrigValue(Rational(2, 4)) == TrigValue(Rational(1, 2))
    assert TrigValue(Rational(1, 2)) == Rational(1, 2)
    assert TrigValue(Rational(1)) == 1


def test_trigvalue_arithmetic():
    """Test TrigValue arithmetic operations."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # Multiplication: (a√r1) * (b√r2) = (ab)√(r1*r2)
    v1 = TrigValue(Rational(1, 2), 2)  # √2/2
    v2 = TrigValue(Rational(1, 2), 2)  # √2/2
    result = v1 * v2
    assert result == TrigValue(Rational(1, 4), 4)
    # Simplified: √4/4 = 2/4 = 1/2
    assert result.is_rational()
    assert result.to_rational() == Rational(1, 2)

    # Division
    v1 = TrigValue(Rational(1), 3)  # √3
    v2 = TrigValue(Rational(1, 3), 3)  # √3/3
    result = v1 / v2
    assert result.is_rational()
    assert result.to_rational() == Rational(3)


def test_trigvalue_negation():
    """Test TrigValue negation."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2), 2)
    neg = -v
    assert neg.coeff == Rational(-1, 2)
    assert neg.radicand == 2


def test_trigvalue_repr():
    """Test TrigValue string representation."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    assert str(TrigValue(Rational(1, 2))) == "Rational(1/2)"
    assert str(TrigValue(Rational(1, 2), 2)) == "√2/2"
    assert str(TrigValue(Rational(1), 3)) == "√3"
    assert str(TrigValue(Rational(-1, 2), 2)) == "-√2/2"


# =============================================================================
# SINE FUNCTION TESTS (degrees)
# =============================================================================

def test_sin_degrees_exact_rational():
    """Test sin_degrees returns exact rational values."""
    from base60lab.trigonometry import sin_degrees
    from base60lab.core.rational import Rational

    # sin(0°) = 0
    assert sin_degrees(0).is_rational()
    assert sin_degrees(0).to_rational() == Rational(0)

    # sin(30°) = 1/2
    assert sin_degrees(30).is_rational()
    assert sin_degrees(30).to_rational() == Rational(1, 2)

    # sin(90°) = 1
    assert sin_degrees(90).is_rational()
    assert sin_degrees(90).to_rational() == Rational(1)

    # sin(180°) = 0
    assert sin_degrees(180).is_rational()
    assert sin_degrees(180).to_rational() == Rational(0)

    # sin(270°) = -1
    assert sin_degrees(270).is_rational()
    assert sin_degrees(270).to_rational() == Rational(-1)

    # sin(360°) = 0
    assert sin_degrees(360).is_rational()
    assert sin_degrees(360).to_rational() == Rational(0)


def test_sin_degrees_exact_algebraic():
    """Test sin_degrees returns exact algebraic values."""
    from base60lab.trigonometry import sin_degrees
    from base60lab.core.rational import Rational

    # sin(45°) = √2/2
    v = sin_degrees(45)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 2

    # sin(60°) = √3/2
    v = sin_degrees(60)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3

    # sin(120°) = √3/2
    v = sin_degrees(120)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3

    # sin(135°) = √2/2
    v = sin_degrees(135)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 2

    # sin(150°) = 1/2
    assert sin_degrees(150).to_rational() == Rational(1, 2)

    # sin(210°) = -1/2
    assert sin_degrees(210).to_rational() == Rational(-1, 2)

    # sin(225°) = -√2/2
    v = sin_degrees(225)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 2)
    assert v.radicand == 2

    # sin(240°) = -√3/2
    v = sin_degrees(240)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 2)
    assert v.radicand == 3

    # sin(300°) = -√3/2
    v = sin_degrees(300)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 2)
    assert v.radicand == 3

    # sin(315°) = -√2/2
    v = sin_degrees(315)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 2)
    assert v.radicand == 2

    # sin(330°) = -1/2
    assert sin_degrees(330).to_rational() == Rational(-1, 2)


def test_sin_degrees_with_rational_input():
    """Test sin_degrees accepts Rational input."""
    from base60lab.trigonometry import sin_degrees
    from base60lab.core.rational import Rational

    assert sin_degrees(Rational(30)).to_rational() == Rational(1, 2)
    assert sin_degrees(Rational(90)).to_rational() == Rational(1)


def test_sin_degrees_normalization():
    """Test sin_degrees normalizes angles outside [0, 360)."""
    from base60lab.trigonometry import sin_degrees
    from base60lab.core.rational import Rational

    # Negative angles
    assert sin_degrees(-90).to_rational() == Rational(-1)
    assert sin_degrees(-30).to_rational() == Rational(-1, 2)

    # Angles >= 360
    assert sin_degrees(390).to_rational() == Rational(1, 2)  # 390° = 30°
    assert sin_degrees(720).to_rational() == Rational(0)  # 720° = 0°
    assert sin_degrees(450).to_rational() == Rational(1)  # 450° = 90°


def test_sin_degrees_unsupported_angle_raises():
    """Test sin_degrees raises ValueError for unsupported angles."""
    from base60lab.trigonometry import sin_degrees

    with pytest.raises(ValueError, match="No exact value available"):
        sin_degrees(15)  # Not a special angle

    with pytest.raises(ValueError, match="No exact value available"):
        sin_degrees(10)

    with pytest.raises(ValueError, match="No exact value available"):
        sin_degrees(20)


# =============================================================================
# COSINE FUNCTION TESTS (degrees)
# =============================================================================

def test_cos_degrees_exact_rational():
    """Test cos_degrees returns exact rational values."""
    from base60lab.trigonometry import cos_degrees
    from base60lab.core.rational import Rational

    # cos(0°) = 1
    assert cos_degrees(0).to_rational() == Rational(1)

    # cos(60°) = 1/2
    assert cos_degrees(60).to_rational() == Rational(1, 2)

    # cos(90°) = 0
    assert cos_degrees(90).to_rational() == Rational(0)

    # cos(180°) = -1
    assert cos_degrees(180).to_rational() == Rational(-1)

    # cos(270°) = 0
    assert cos_degrees(270).to_rational() == Rational(0)

    # cos(360°) = 1
    assert cos_degrees(360).to_rational() == Rational(1)


def test_cos_degrees_exact_algebraic():
    """Test cos_degrees returns exact algebraic values."""
    from base60lab.trigonometry import cos_degrees
    from base60lab.core.rational import Rational

    # cos(30°) = √3/2
    v = cos_degrees(30)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3

    # cos(45°) = √2/2
    v = cos_degrees(45)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 2

    # cos(120°) = -1/2
    assert cos_degrees(120).to_rational() == Rational(-1, 2)

    # cos(135°) = -√2/2
    v = cos_degrees(135)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 2)
    assert v.radicand == 2

    # cos(150°) = -√3/2
    v = cos_degrees(150)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 2)
    assert v.radicand == 3

    # cos(210°) = -√3/2
    v = cos_degrees(210)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 2)
    assert v.radicand == 3

    # cos(225°) = -√2/2
    v = cos_degrees(225)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 2)
    assert v.radicand == 2

    # cos(240°) = -1/2
    assert cos_degrees(240).to_rational() == Rational(-1, 2)

    # cos(300°) = 1/2
    assert cos_degrees(300).to_rational() == Rational(1, 2)

    # cos(315°) = √2/2
    v = cos_degrees(315)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 2

    # cos(330°) = √3/2
    v = cos_degrees(330)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3


# =============================================================================
# TANGENT FUNCTION TESTS (degrees)
# =============================================================================

def test_tan_degrees_exact_rational():
    """Test tan_degrees returns exact rational values."""
    from base60lab.trigonometry import tan_degrees
    from base60lab.core.rational import Rational

    # tan(0°) = 0
    assert tan_degrees(0).to_rational() == Rational(0)

    # tan(45°) = 1
    assert tan_degrees(45).to_rational() == Rational(1)

    # tan(135°) = -1
    assert tan_degrees(135).to_rational() == Rational(-1)

    # tan(180°) = 0
    assert tan_degrees(180).to_rational() == Rational(0)

    # tan(225°) = 1
    assert tan_degrees(225).to_rational() == Rational(1)

    # tan(315°) = -1
    assert tan_degrees(315).to_rational() == Rational(-1)

    # tan(360°) = 0
    assert tan_degrees(360).to_rational() == Rational(0)


def test_tan_degrees_exact_algebraic():
    """Test tan_degrees returns exact algebraic values."""
    from base60lab.trigonometry import tan_degrees
    from base60lab.core.rational import Rational

    # tan(30°) = 1/√3 = √3/3
    v = tan_degrees(30)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 3)
    assert v.radicand == 3

    # tan(60°) = √3
    v = tan_degrees(60)
    assert not v.is_rational()
    assert v.coeff == Rational(1)
    assert v.radicand == 3

    # tan(120°) = -√3
    v = tan_degrees(120)
    assert not v.is_rational()
    assert v.coeff == Rational(-1)
    assert v.radicand == 3

    # tan(150°) = -1/√3 = -√3/3
    v = tan_degrees(150)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 3)
    assert v.radicand == 3

    # tan(210°) = 1/√3 = √3/3
    v = tan_degrees(210)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 3)
    assert v.radicand == 3

    # tan(240°) = √3
    v = tan_degrees(240)
    assert not v.is_rational()
    assert v.coeff == Rational(1)
    assert v.radicand == 3

    # tan(300°) = -√3
    v = tan_degrees(300)
    assert not v.is_rational()
    assert v.coeff == Rational(-1)
    assert v.radicand == 3

    # tan(330°) = -1/√3 = -√3/3
    v = tan_degrees(330)
    assert not v.is_rational()
    assert v.coeff == Rational(-1, 3)
    assert v.radicand == 3


def test_tan_degrees_undefined_raises():
    """Test tan_degrees raises for undefined angles (90°, 270°)."""
    from base60lab.trigonometry import tan_degrees

    with pytest.raises(ValueError, match="undefined"):
        tan_degrees(90)

    with pytest.raises(ValueError, match="undefined"):
        tan_degrees(270)

    with pytest.raises(ValueError, match="undefined"):
        tan_degrees(450)  # 450° = 90°


# =============================================================================
# TURN-BASED ANGLE TESTS
# =============================================================================

def test_sin_turns():
    """Test sin_turns with turn-based angles."""
    from base60lab.trigonometry import sin_turns
    from base60lab.core.rational import Rational

    # 0 turns = 0°
    assert sin_turns(0).to_rational() == Rational(0)

    # 1/12 turn = 30°
    assert sin_turns(Rational(1, 12)).to_rational() == Rational(1, 2)

    # 1/8 turn = 45°
    v = sin_turns(Rational(1, 8))
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 2

    # 1/6 turn = 60°
    v = sin_turns(Rational(1, 6))
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3

    # 1/4 turn = 90°
    assert sin_turns(Rational(1, 4)).to_rational() == Rational(1)

    # 1/2 turn = 180°
    assert sin_turns(Rational(1, 2)).to_rational() == Rational(0)

    # 3/4 turn = 270°
    assert sin_turns(Rational(3, 4)).to_rational() == Rational(-1)

    # 1 turn = 360°
    assert sin_turns(1).to_rational() == Rational(0)


def test_cos_turns():
    """Test cos_turns with turn-based angles."""
    from base60lab.trigonometry import cos_turns
    from base60lab.core.rational import Rational

    assert cos_turns(0).to_rational() == Rational(1)
    assert cos_turns(Rational(1, 12)).is_rational() is False  # cos(30°) = √3/2
    v = cos_turns(Rational(1, 12))
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3

    assert cos_turns(Rational(1, 4)).to_rational() == Rational(0)  # cos(90°)
    assert cos_turns(Rational(1, 2)).to_rational() == Rational(-1)  # cos(180°)
    assert cos_turns(1).to_rational() == Rational(1)  # cos(360°)


def test_tan_turns():
    """Test tan_turns with turn-based angles."""
    from base60lab.trigonometry import tan_turns
    from base60lab.core.rational import Rational

    assert tan_turns(0).to_rational() == Rational(0)
    assert tan_turns(Rational(1, 8)).to_rational() == Rational(1)  # tan(45°)

    with pytest.raises(ValueError, match="undefined"):
        tan_turns(Rational(1, 4))  # tan(90°)


# =============================================================================
# DOZENAL ANGLE TESTS
# =============================================================================

def test_sin_dozenal():
    """Test sin_dozenal with dozenal (base-12) turns."""
    from base60lab.trigonometry import sin_dozenal
    from base60lab.core.rational import Rational

    # In dozenal: 0.1 = 1/12 turn = 30°
    assert sin_dozenal(Rational(1, 12)).to_rational() == Rational(1, 2)

    # 0.16 dozenal = 1/6 turn = 60° (in base-12, 0.16 = 1/6)
    # Actually 0.16 in base-12 = 1/12 + 6/144 = 1/12 + 1/24 = 3/24 = 1/8 turn = 45°
    # Let's use fraction 1/6
    v = sin_dozenal(Rational(1, 6))
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3

    # 0.2 dozenal = 2/12 = 1/6 turn = 60°
    v = sin_dozenal(Rational(1, 6))
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3


def test_cos_dozenal():
    """Test cos_dozenal with dozenal turns."""
    from base60lab.trigonometry import cos_dozenal
    from base60lab.core.rational import Rational

    v = cos_dozenal(Rational(1, 12))  # cos(30°) = √3/2
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3


def test_tan_dozenal():
    """Test tan_dozenal with dozenal turns."""
    from base60lab.trigonometry import tan_dozenal
    from base60lab.core.rational import Rational

    # tan(30°) = 1/√3
    v = tan_dozenal(Rational(1, 12))
    assert not v.is_rational()
    assert v.coeff == Rational(1, 3)
    assert v.radicand == 3


# =============================================================================
# DMS (DEGREES, MINUTES, SECONDS) TESTS
# =============================================================================

def test_sin_dms():
    """Test sin_dms with degrees, minutes, seconds."""
    from base60lab.trigonometry import sin_dms
    from base60lab.core.rational import Rational

    # 30° 0' 0" = 30°
    assert sin_dms(30, 0, 0).to_rational() == Rational(1, 2)

    # 45° 0' 0" = 45°
    v = sin_dms(45, 0, 0)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 2

    # 60° 0' 0" = 60°
    v = sin_dms(60, 0, 0)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3

    # 0° 30' 0" = 0.5° (not a special angle)
    with pytest.raises(ValueError, match="No exact value available"):
        sin_dms(0, 30, 0)


def test_cos_dms():
    """Test cos_dms with degrees, minutes, seconds."""
    from base60lab.trigonometry import cos_dms
    from base60lab.core.rational import Rational

    v = cos_dms(30, 0, 0)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 2)
    assert v.radicand == 3

    assert cos_dms(60, 0, 0).to_rational() == Rational(1, 2)


def test_tan_dms():
    """Test tan_dms with degrees, minutes, seconds."""
    from base60lab.trigonometry import tan_dms
    from base60lab.core.rational import Rational

    assert tan_dms(45, 0, 0).to_rational() == Rational(1)

    v = tan_dms(30, 0, 0)
    assert not v.is_rational()
    assert v.coeff == Rational(1, 3)
    assert v.radicand == 3


def test_dms_validation():
    """Test DMS input validation."""
    from base60lab.trigonometry import sin_dms

    with pytest.raises(ValueError, match="minutes must be in"):
        sin_dms(30, 60, 0)

    with pytest.raises(ValueError, match="minutes must be in"):
        sin_dms(30, -1, 0)

    with pytest.raises(ValueError, match="seconds must be in"):
        sin_dms(30, 0, 60)

    with pytest.raises(ValueError, match="seconds must be in"):
        sin_dms(30, 0, -1)


# =============================================================================
# CONVERSION UTILITY TESTS
# =============================================================================

def test_degrees_to_turns():
    """Test degrees to turns conversion."""
    from base60lab.trigonometry import degrees_to_turns
    from base60lab.core.rational import Rational

    assert degrees_to_turns(0) == Rational(0)
    assert degrees_to_turns(90) == Rational(1, 4)
    assert degrees_to_turns(180) == Rational(1, 2)
    assert degrees_to_turns(360) == Rational(1)
    assert degrees_to_turns(30) == Rational(1, 12)


def test_turns_to_degrees():
    """Test turns to degrees conversion."""
    from base60lab.trigonometry import turns_to_degrees
    from base60lab.core.rational import Rational

    assert turns_to_degrees(0) == Rational(0)
    assert turns_to_degrees(Rational(1, 4)) == Rational(90)
    assert turns_to_degrees(Rational(1, 2)) == Rational(180)
    assert turns_to_degrees(1) == Rational(360)
    assert turns_to_degrees(Rational(1, 12)) == Rational(30)


def test_degrees_to_dozenal():
    """Test degrees to dozenal conversion."""
    from base60lab.trigonometry import degrees_to_dozenal
    from base60lab.core.rational import Rational

    # 30° = 1/12 turn = 0.1 dozenal
    assert degrees_to_dozenal(30) == Rational(1, 12)

    # 60° = 1/6 turn
    assert degrees_to_dozenal(60) == Rational(1, 6)

    # 90° = 1/4 turn
    assert degrees_to_dozenal(90) == Rational(1, 4)


def test_dozenal_to_degrees():
    """Test dozenal to degrees conversion."""
    from base60lab.trigonometry import dozenal_to_degrees
    from base60lab.core.rational import Rational

    # 0.1 dozenal = 1/12 turn = 30°
    assert dozenal_to_degrees(Rational(1, 12)) == Rational(30)

    # 1/6 turn = 60°
    assert dozenal_to_degrees(Rational(1, 6)) == Rational(60)


def test_degrees_to_dms():
    """Test decimal degrees to DMS conversion."""
    from base60lab.trigonometry import degrees_to_dms

    assert degrees_to_dms(30) == (30, 0, 0)
    assert degrees_to_dms(45) == (45, 0, 0)
    # 30.5° = 30° 30' 0"
    assert degrees_to_dms(30.5) == (30, 30, 0)
    # 30.25° = 30° 15' 0"
    assert degrees_to_dms(30.25) == (30, 15, 0)


def test_dms_to_degrees():
    """Test DMS to decimal degrees conversion."""
    from base60lab.trigonometry import dms_to_degrees
    from base60lab.core.rational import Rational

    assert dms_to_degrees(30, 0, 0) == Rational(30)
    assert dms_to_degrees(30, 30, 0) == Rational(61, 2)  # 30.5
    assert dms_to_degrees(30, 15, 0) == Rational(121, 4)  # 30.25
    assert dms_to_degrees(0, 30, 0) == Rational(1, 2)  # 0.5°


# =============================================================================
# IDENTITY VERIFICATION TESTS
# =============================================================================

def test_pythagorean_identity():
    """Test sin²(θ) + cos²(θ) = 1 for supported angles."""
    from base60lab.trigonometry import verify_pythagorean_identity

    # Test all special angles
    for angle in [0, 30, 45, 60, 90, 120, 135, 150, 180,
                  210, 225, 240, 270, 300, 315, 330, 360]:
        assert verify_pythagorean_identity(angle), f"Failed for {angle}°"


def test_is_supported_angle():
    """Test is_supported_angle function."""
    from base60lab.trigonometry import is_supported_angle

    assert is_supported_angle(30, "sin") is True
    assert is_supported_angle(45, "sin") is True
    assert is_supported_angle(60, "sin") is True
    assert is_supported_angle(15, "sin") is False
    assert is_supported_angle(10, "sin") is False

    assert is_supported_angle(30, "cos") is True
    assert is_supported_angle(30, "tan") is True
    assert is_supported_angle(90, "tan") is True  # 90° is in list but undefined
    assert is_supported_angle(90, "sin") is True


# =============================================================================
# ADVERSARIAL / EDGE CASE TESTS
# =============================================================================

def test_malformed_input_float():
    """Test that float input is handled (with potential precision loss warning)."""
    from base60lab.trigonometry import sin_degrees
    from base60lab.core.rational import Rational

    # Float input should work for exact values
    assert sin_degrees(30.0).to_rational() == Rational(1, 2)
    assert sin_degrees(45.0).coeff == Rational(1, 2)
    assert sin_degrees(45.0).radicand == 2


def test_deterministic_results():
    """Test that results are deterministic (no flaky randomness)."""
    from base60lab.trigonometry import sin_degrees, cos_degrees, tan_degrees
    from base60lab.core.rational import Rational

    # Run multiple times
    for _ in range(10):
        assert sin_degrees(30).to_rational() == Rational(1, 2)
        assert sin_degrees(45).coeff == Rational(1, 2)
        assert sin_degrees(45).radicand == 2
        assert cos_degrees(60).to_rational() == Rational(1, 2)
        assert tan_degrees(45).to_rational() == Rational(1)


def test_rational_equality_verification():
    """Test actual Rational equality (not string comparison)."""
    from base60lab.trigonometry import sin_degrees
    from base60lab.core.rational import Rational

    result = sin_degrees(30)
    expected = Rational(1, 2)

    # Must verify actual Rational equality, not just string representation
    assert result.is_rational()
    assert result.to_rational() == expected
    assert result.to_rational().numerator == 1
    assert result.to_rational().denominator == 2


def test_manual_qa_sin_30():
    """Manual QA test: sin_degrees(30) should print exactly 0.5 (Rational(1,2))."""
    from base60lab.trigonometry import sin_degrees
    from base60lab.core.rational import Rational

    result = sin_degrees(30)
    # This simulates: python -c "from base60lab.trigonometry import *; print(sin_degrees(30))"
    # Should print exactly Rational(1/2) which displays as 0.5 when converted to float
    assert result.to_rational() == Rational(1, 2)
    assert result.to_rational().to_float() == 0.5


def test_negative_angles():
    """Test negative angle handling."""
    from base60lab.trigonometry import sin_degrees, cos_degrees, tan_degrees
    from base60lab.core.rational import Rational

    # sin(-30°) = -1/2
    assert sin_degrees(-30).to_rational() == Rational(-1, 2)

    # cos(-60°) = 1/2
    assert cos_degrees(-60).to_rational() == Rational(1, 2)

    # tan(-45°) = -1
    assert tan_degrees(-45).to_rational() == Rational(-1)


def test_large_angles():
    """Test large angle normalization."""
    from base60lab.trigonometry import sin_degrees, cos_degrees, tan_degrees
    from base60lab.core.rational import Rational

    # 720° = 2 full turns = 0°
    assert sin_degrees(720).to_rational() == Rational(0)
    assert cos_degrees(720).to_rational() == Rational(1)
    assert tan_degrees(720).to_rational() == Rational(0)

    # 1080° = 3 full turns = 0°
    assert sin_degrees(1080).to_rational() == Rational(0)


# =============================================================================
# REGRESSION TESTS FOR SPECIFIC ISSUES
# =============================================================================

def test_trigvalue_simplification_preserves_sign():
    """Test that TrigValue simplification preserves negative sign."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # -√4 should become -2, not 2
    v = TrigValue(Rational(-1), 4)
    assert v.is_rational()
    assert v.to_rational() == Rational(-2)


def test_trigvalue_zero_handling():
    """Test TrigValue with zero coefficient."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(0), 5)
    assert v.is_zero()
    assert v.is_rational()
    assert v.to_rational() == Rational(0)


def test_trigvalue_sqrt_of_square():
    """Test sqrt of perfect square simplification."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # √9 = 3
    v = TrigValue(Rational(1), 9)
    assert v.is_rational()
    assert v.to_rational() == Rational(3)

    # √(1/4) not directly representable, but √4/2 = 1
    v = TrigValue(Rational(1, 2), 4)
    assert v.is_rational()
    assert v.to_rational() == Rational(1)
# =============================================================================
# TRIGVALUE CLASS EDGE CASE TESTS (covering missing lines)
# =============================================================================

def test_trigvalue_invalid_radicand_raises():
    """Test TrigValue raises ValueError for invalid radicand."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    with pytest.raises(ValueError, match="radicand must be >= 1"):
        TrigValue(Rational(1), 0)
    with pytest.raises(ValueError, match="radicand must be >= 1"):
        TrigValue(Rational(1), -1)


def test_trigvalue_to_rational_raises_on_algebraic():
    """Test TrigValue.to_rational raises for non-rational values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2), 2)  # √2/2
    with pytest.raises(ValueError, match="not rational"):
        v.to_rational()


def test_trigvalue_to_float():
    """Test TrigValue.to_float conversion."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # Rational value
    v = TrigValue(Rational(1, 2))
    assert abs(v.to_float() - 0.5) < 1e-10

    # Algebraic value
    v = TrigValue(Rational(1, 2), 2)  # √2/2 ≈ 0.7071
    assert abs(v.to_float() - 0.7071067811865475) < 1e-10

    v = TrigValue(Rational(1), 3)  # √3 ≈ 1.732
    assert abs(v.to_float() - 1.7320508075688772) < 1e-10


def test_trigvalue_mul_trigvalue():
    """Test TrigValue multiplication with another TrigValue."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # √2 * √2 = 2 (rational result after simplification)
    a = TrigValue(Rational(1), 2)  # √2
    b = TrigValue(Rational(1), 2)  # √2
    result = a * b
    assert result.is_rational()
    assert result.to_rational() == Rational(2)

    # √3 * √2 = √6
    a = TrigValue(Rational(1), 3)
    b = TrigValue(Rational(1), 2)
    result = a * b
    assert result.coeff == Rational(1)
    assert result.radicand == 6


def test_trigvalue_mul_rational():
    """Test TrigValue multiplication with Rational."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2), 2)  # √2/2
    result = v * Rational(2)
    assert result.coeff == Rational(1)
    assert result.radicand == 2


def test_trigvalue_mul_int():
    """Test TrigValue multiplication with int."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2), 3)  # √3/2
    result = v * 2
    assert result.coeff == Rational(1)
    assert result.radicand == 3


def test_trigvalue_rmul_rational():
    """Test TrigValue reverse multiplication with Rational."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2), 2)
    # Test __rmul__ directly since Rational.__mul__ doesn't return NotImplemented
    result = v.__rmul__(Rational(3))
    assert result.coeff == Rational(3, 2)
    assert result.radicand == 2


def test_trigvalue_rmul_int():
    """Test TrigValue reverse multiplication with int."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1), 3)
    # Test __rmul__ directly since int.__mul__ doesn't know about TrigValue
    result = v.__rmul__(2)
    assert result.coeff == Rational(2)
    assert result.radicand == 3


def test_trigvalue_div_trigvalue_same_radicand():
    """Test TrigValue division by TrigValue with same radicand (rational result)."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # √3 / (√3/3) = 3
    a = TrigValue(Rational(1), 3)  # √3
    b = TrigValue(Rational(1, 3), 3)  # √3/3
    result = a / b
    assert result.is_rational()
    assert result.to_rational() == Rational(3)


def test_trigvalue_div_trigvalue_diff_radicand():
    """Test TrigValue division by TrigValue with different radicand."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # √2 / √3 = √2/√3 = √6/3
    a = TrigValue(Rational(1), 2)  # √2
    b = TrigValue(Rational(1), 3)  # √3
    result = a / b
    # (1√2) / (1√3) = (1/1) * √(2*3) / 3 = √6/3
    assert result.coeff == Rational(1, 3)
    assert result.radicand == 6


def test_trigvalue_div_rational():
    """Test TrigValue division by Rational."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1), 2)  # √2
    result = v / Rational(2)
    assert result.coeff == Rational(1, 2)
    assert result.radicand == 2


def test_trigvalue_div_int():
    """Test TrigValue division by int."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1), 3)  # √3
    result = v / 3
    assert result.coeff == Rational(1, 3)
    assert result.radicand == 3


def test_trigvalue_negation():
    """Test TrigValue negation."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2), 2)
    neg = -v
    assert neg.coeff == Rational(-1, 2)
    assert neg.radicand == 2

    # Test negation of rational
    v = TrigValue(Rational(3))
    neg = -v
    assert neg.coeff == Rational(-3)
    assert neg.radicand == 1


def test_trigvalue_equality_with_rational():
    """Test TrigValue equality with Rational and int."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2))
    assert v == Rational(1, 2)
    # Actually, the __eq__ returns NotImplemented for float, so it uses float.__eq__
    # Let's test with int
    v2 = TrigValue(Rational(2))
    assert v2 == 2
    assert v2 == Rational(2)


def test_trigvalue_equality_not_implemented():
    """Test TrigValue equality returns NotImplemented for non-TrigValue/Rational/int."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2))
    # Comparing with string should return NotImplemented
    result = v.__eq__("not a trigvalue")
    assert result is NotImplemented


def test_trigvalue_normalized():
    """Test TrigValue._normalized method."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # Already normalized
    v = TrigValue(Rational(1, 2), 2)
    norm = v._normalized()
    assert norm.coeff == Rational(1, 2)
    assert norm.radicand == 2

    # Has square factor: √8 = 2√2
    v = TrigValue(Rational(1), 8)
    norm = v._normalized()
    assert norm.coeff == Rational(2)
    assert norm.radicand == 2

    # Has square factor with coeff: 3√12 = 6√3
    v = TrigValue(Rational(3), 12)
    norm = v._normalized()
    assert norm.coeff == Rational(6)
    assert norm.radicand == 3


def test_trigvalue_repr_rational():
    """Test TrigValue __repr__ for rational values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2))
    assert repr(v) == "TrigValue(Rational(1/2))"

    v = TrigValue(Rational(-3))
    assert repr(v) == "TrigValue(Rational(-3))"


def test_trigvalue_repr_sqrt():
    """Test TrigValue __repr__ for sqrt values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1), 2)
    assert repr(v) == "TrigValue(√2)"

    v = TrigValue(Rational(-1), 3)
    assert repr(v) == "TrigValue(-√3)"


def test_trigvalue_repr_coeff_sqrt():
    """Test TrigValue __repr__ for coeff*sqrt values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(2), 3)
    assert repr(v) == "TrigValue(Rational(2)·√3)"

    v = TrigValue(Rational(-2), 5)
    assert repr(v) == "TrigValue(Rational(-2)·√5)"


def test_trigvalue_str_rational():
    """Test TrigValue __str__ for rational values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2))
    assert str(v) == "Rational(1/2)"

    v = TrigValue(Rational(-3))
    assert str(v) == "Rational(-3)"


def test_trigvalue_str_sqrt():
    """Test TrigValue __str__ for sqrt values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1), 2)
    assert str(v) == "√2"

    v = TrigValue(Rational(-1), 3)
    assert str(v) == "-√3"


def test_trigvalue_str_half_sqrt():
    """Test TrigValue __str__ for sqrt/2 values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1, 2), 2)
    assert str(v) == "√2/2"

    v = TrigValue(Rational(-1, 2), 3)
    assert str(v) == "-√3/2"


def test_trigvalue_str_coeff_sqrt():
    """Test TrigValue __str__ for general coeff*sqrt values."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(2), 3)
    assert str(v) == "Rational(2)·√3"

    v = TrigValue(Rational(3, 4), 5)
    assert str(v) == "Rational(3/4)·√5"


# =============================================================================
# _to_dms EDGE CASES (covering lines 246, 253)
# =============================================================================

def test_to_dms_negative_degrees():
    """Test _to_dms with negative degrees."""
    from base60lab.trigonometry import _to_dms
    from base60lab.core.rational import Rational

    # -30.5° = -30°30'0"
    result = _to_dms(Rational(-61, 2))
    assert result == (-30, 30, 0)

    # -0.5° = 0°-30'0" -> but we store as -0°30'0" 
    result = _to_dms(Rational(-1, 2))
    assert result == (0, 30, 0)  # degs=0, but neg makes it -0 which is 0


def test_to_dms_negative_with_minutes_seconds():
    """Test _to_dms with negative degrees with minutes and seconds."""
    from base60lab.trigonometry import _to_dms
    from base60lab.core.rational import Rational

    # -30°30'30" = -30.50833...°
    result = _to_dms(Rational(-109830, 3600))
    assert result == (-30, 30, 30)


# =============================================================================
# _cos_degrees_exact and _tan_degrees_exact unsupported angles (lines 320, 355)
# =============================================================================

def test_cos_degrees_unsupported_angle_raises():
    """Test cos_degrees raises for unsupported angles."""
    from base60lab.trigonometry import cos_degrees

    with pytest.raises(ValueError, match="No exact value available for cos"):
        cos_degrees(20)


def test_tan_degrees_unsupported_angle_raises():
    """Test tan_degrees raises for unsupported angles."""
    from base60lab.trigonometry import tan_degrees

    with pytest.raises(ValueError, match="No exact value available for tan"):
        tan_degrees(20)


# =============================================================================
# PUBLIC API FLOAT INPUT TESTS (lines 391, 400, 409, 419, 429, 442, 444, 453, 455, 464, 466)
# =============================================================================

def test_sin_degrees_float_input():
    """Test sin_degrees with float input."""
    from base60lab.trigonometry import sin_degrees
    from base60lab.core.rational import Rational

    # 30.0° -> should be treated as 30°
    result = sin_degrees(30.0)
    assert result.to_rational() == Rational(1, 2)


def test_cos_degrees_float_input():
    """Test cos_degrees with float input."""
    from base60lab.trigonometry import cos_degrees
    from base60lab.core.rational import Rational

    result = cos_degrees(60.0)
    assert result.to_rational() == Rational(1, 2)


def test_tan_degrees_float_input():
    """Test tan_degrees with float input."""
    from base60lab.trigonometry import tan_degrees
    from base60lab.core.rational import Rational

    result = tan_degrees(45.0)
    assert result.to_rational() == Rational(1)


def test_sin_turns_float_input():
    """Test sin_turns with float input."""
    from base60lab.trigonometry import sin_turns
    from base60lab.core.rational import Rational

    result = sin_turns(0.25)  # 90°
    assert result.to_rational() == Rational(1)


def test_cos_turns_float_input():
    """Test cos_turns with float input."""
    from base60lab.trigonometry import cos_turns
    from base60lab.core.rational import Rational

    result = cos_turns(0.5)  # 180°
    assert result.to_rational() == Rational(-1)


def test_tan_turns_float_input():
    """Test tan_turns with float input."""
    from base60lab.trigonometry import tan_turns
    from base60lab.core.rational import Rational

    result = tan_turns(1/8)  # 45°
    assert result.to_rational() == Rational(1)


def test_sin_dozenal_float_input():
    """Test sin_dozenal with float input."""
    from base60lab.trigonometry import sin_dozenal
    from base60lab.core.rational import Rational

    # 0.25 = 1/4 turn = 90° - exact float
    result = sin_dozenal(0.25)
    assert result.to_rational() == Rational(1)


def test_cos_dozenal_float_input():
    """Test cos_dozenal with float input."""
    from base60lab.trigonometry import cos_dozenal
    from base60lab.core.rational import Rational

    # 0.5 = 1/2 turn = 180° - exact float
    result = cos_dozenal(0.5)
    assert result.to_rational() == Rational(-1)


def test_tan_dozenal_float_input():
    """Test tan_dozenal with float input."""
    from base60lab.trigonometry import tan_dozenal
    from base60lab.core.rational import Rational

    # 0.25 = 1/4 turn = 90° - undefined for tan
    # Use 1/12 = 0.08333... which is not exact
    # Use 0.5 = 180° where tan = 0
    result = tan_dozenal(0.5)  # 180°
    assert result.to_rational() == Rational(0)


def test_sin_dms_with_various_inputs():
    """Test sin_dms with various valid inputs."""
    from base60lab.trigonometry import sin_dms
    from base60lab.core.rational import Rational

    # 30°0'0" = 30°
    result = sin_dms(30, 0, 0)
    assert result.to_rational() == Rational(1, 2)

    # 45°30'0" = 45.5° (not a special angle - should raise)
    with pytest.raises(ValueError):
        sin_dms(45, 30, 0)


def test_tan_dms_undefined():
    """Test tan_dms for undefined angles."""
    from base60lab.trigonometry import tan_dms

    # 90°0'0" = 90° - undefined
    with pytest.raises(ValueError, match="undefined"):
        tan_dms(90, 0, 0)


# =============================================================================
# verify_angle_sum_identity (lines 510-527)
# =============================================================================

def test_verify_angle_sum_identity_basic():
    """Test verify_angle_sum_identity with known identities."""
    from base60lab.trigonometry import verify_angle_sum_identity

    # sin(30+60) = sin(30)cos(60) + cos(30)sin(60)
    # sin(90) = 1 = (1/2)(1/2) + (√3/2)(√3/2) = 1/4 + 3/4 = 1
    assert verify_angle_sum_identity(30, 60) is True

    # sin(45+45) = sin(45)cos(45) + cos(45)sin(45)
    # sin(90) = 1 = (√2/2)(√2/2) + (√2/2)(√2/2) = 1/2 + 1/2 = 1
    assert verify_angle_sum_identity(45, 45) is True

    # sin(0+30) = sin(0)cos(30) + cos(0)sin(30)
    # sin(30) = 1/2 = 0*(√3/2) + 1*(1/2) = 1/2
    assert verify_angle_sum_identity(0, 30) is True


def test_verify_angle_sum_identity_with_rational():
    """Test verify_angle_sum_identity with Rational inputs."""
    from base60lab.trigonometry import verify_angle_sum_identity
    from base60lab.core.rational import Rational

    assert verify_angle_sum_identity(Rational(30), Rational(60)) is True
    assert verify_angle_sum_identity(Rational(45), Rational(45)) is True


def test_verify_angle_sum_identity_negative():
    """Test verify_angle_sum_identity with negative angles."""
    from base60lab.trigonometry import verify_angle_sum_identity

    # sin(-30+60) = sin(30) = 1/2
    assert verify_angle_sum_identity(-30, 60) is True


def test_verify_angle_sum_identity_large_angles():
    """Test verify_angle_sum_identity with angles > 360."""
    from base60lab.trigonometry import verify_angle_sum_identity

    # 390° + 60° = 450° = 90°
    assert verify_angle_sum_identity(390, 60) is True


# =============================================================================
# is_supported_angle edge cases (line 596)
# =============================================================================

def test_is_supported_angle_invalid_func():
    """Test is_supported_angle with invalid function name."""
    from base60lab.trigonometry import is_supported_angle

    assert is_supported_angle(30, "sin") is True
    assert is_supported_angle(30, "cos") is True
    assert is_supported_angle(30, "tan") is True
    # Invalid function should return False (line 596)
    assert is_supported_angle(30, "sec") is False
    assert is_supported_angle(30, "csc") is False
    assert is_supported_angle(30, "cot") is False
    assert is_supported_angle(30, "invalid") is False


def test_is_supported_angle_unsupported_angles():
    """Test is_supported_angle for unsupported angles."""
    from base60lab.trigonometry import is_supported_angle

    # 20° is not a supported angle for any function
    assert is_supported_angle(20, "sin") is False
    assert is_supported_angle(20, "cos") is False
    assert is_supported_angle(20, "tan") is False


def test_is_supported_angle_tan_undefined():
    """Test is_supported_angle for tan at undefined angles (90, 270)."""
    from base60lab.trigonometry import is_supported_angle

    # 90° and 270° are in SUPPORTED_TANGENT_ANGLES list but tan is undefined
    # The function checks list membership, not actual computability
    assert is_supported_angle(90, "tan") is True
    assert is_supported_angle(270, "tan") is True


# =============================================================================
# DMS validation edge cases
# =============================================================================

def test_dms_validation_comprehensive():
    """Test DMS validation with various invalid inputs."""
    from base60lab.trigonometry import sin_dms, cos_dms, tan_dms

    # Negative minutes
    with pytest.raises(ValueError, match="minutes must be in \\[0, 60\\)"):
        sin_dms(30, -1, 0)

    # Minutes >= 60
    with pytest.raises(ValueError, match="minutes must be in \\[0, 60\\)"):
        sin_dms(30, 60, 0)

    # Negative seconds
    with pytest.raises(ValueError, match="seconds must be in \\[0, 60\\)"):
        sin_dms(30, 0, -1)

    # Seconds >= 60
    with pytest.raises(ValueError, match="seconds must be in \\[0, 60\\)"):
        sin_dms(30, 0, 60)

    # Test all three functions
    with pytest.raises(ValueError):
        cos_dms(30, -1, 0)
    with pytest.raises(ValueError):
        tan_dms(30, 60, 0)


# =============================================================================
# degrees_to_dms with float (line 560-561)
# =============================================================================

def test_degrees_to_dms_float_input():
    """Test degrees_to_dms with float input."""
    from base60lab.trigonometry import degrees_to_dms

    result = degrees_to_dms(30.5)
    assert result == (30, 30, 0)

    result = degrees_to_dms(45.25)
    assert result == (45, 15, 0)


def test_degrees_to_dms_negative_float():
    """Test degrees_to_dms with negative float."""
    from base60lab.trigonometry import degrees_to_dms

    result = degrees_to_dms(-30.5)
    assert result == (-30, 30, 0)


# =============================================================================
# Conversion utilities with Rational
# =============================================================================

def test_degrees_to_turns_rational():
    """Test degrees_to_turns with Rational input."""
    from base60lab.trigonometry import degrees_to_turns
    from base60lab.core.rational import Rational

    result = degrees_to_turns(Rational(90))
    assert result == Rational(1, 4)


def test_turns_to_degrees_rational():
    """Test turns_to_degrees with Rational input."""
    from base60lab.trigonometry import turns_to_degrees
    from base60lab.core.rational import Rational

    result = turns_to_degrees(Rational(1, 6))
    assert result == Rational(60)


def test_degrees_to_dozenal_rational():
    """Test degrees_to_dozenal with Rational input."""
    from base60lab.trigonometry import degrees_to_dozenal
    from base60lab.core.rational import Rational

    result = degrees_to_dozenal(Rational(90))
    assert result == Rational(1, 4)


def test_dozenal_to_degrees_rational():
    """Test dozenal_to_degrees with Rational input."""
    from base60lab.trigonometry import dozenal_to_degrees
    from base60lab.core.rational import Rational

    result = dozenal_to_degrees(Rational(1, 3))
    assert result == Rational(120)


def test_dms_to_degrees():
    """Test dms_to_degrees function."""
    from base60lab.trigonometry import dms_to_degrees
    from base60lab.core.rational import Rational

    result = dms_to_degrees(30, 30, 0)
    assert result == Rational(61, 2)  # 30.5°


# =============================================================================
# Edge cases for public API with unsupported angles
# =============================================================================

def test_sin_degrees_unsupported_various():
    """Test sin_degrees raises for various unsupported angles."""
    from base60lab.trigonometry import sin_degrees

    for angle in [1, 2, 5, 10, 15, 20, 25, 35, 40, 50, 55]:
        with pytest.raises(ValueError):
            sin_degrees(angle)


def test_cos_degrees_unsupported_various():
    """Test cos_degrees raises for various unsupported angles."""
    from base60lab.trigonometry import cos_degrees

    for angle in [1, 2, 5, 10, 15, 20, 25, 35, 40, 50, 55]:
        with pytest.raises(ValueError):
            cos_degrees(angle)


def test_tan_degrees_unsupported_various():
    """Test tan_degrees raises for various unsupported angles."""
    from base60lab.trigonometry import tan_degrees

    for angle in [1, 2, 5, 10, 15, 20, 25, 35, 40, 50, 55]:
        with pytest.raises(ValueError):
            tan_degrees(angle)


def test_sin_turns_unsupported():
    """Test sin_turns with unsupported turn values."""
    from base60lab.trigonometry import sin_turns
    from base60lab.core.rational import Rational

    # 1/24 turn = 15° (not supported)
    with pytest.raises(ValueError):
        sin_turns(Rational(1, 24))


def test_cos_turns_unsupported():
    """Test cos_turns with unsupported turn values."""
    from base60lab.trigonometry import cos_turns
    from base60lab.core.rational import Rational

    with pytest.raises(ValueError):
        cos_turns(Rational(1, 24))


def test_tan_turns_unsupported():
    """Test tan_turns with unsupported turn values."""
    from base60lab.trigonometry import tan_turns
    from base60lab.core.rational import Rational

    with pytest.raises(ValueError):
        tan_turns(Rational(1, 24))


def test_sin_dozenal_unsupported():
    """Test sin_dozenal with unsupported dozenal values."""
    from base60lab.trigonometry import sin_dozenal
    from base60lab.core.rational import Rational

    # 1/24 dozenal turn = 15° (not supported)
    with pytest.raises(ValueError):
        sin_dozenal(Rational(1, 24))


def test_cos_dozenal_unsupported():
    """Test cos_dozenal with unsupported dozenal values."""
    from base60lab.trigonometry import cos_dozenal
    from base60lab.core.rational import Rational

    with pytest.raises(ValueError):
        cos_dozenal(Rational(1, 24))


def test_tan_dozenal_unsupported():
    """Test tan_dozenal with unsupported dozenal values."""
    from base60lab.trigonometry import tan_dozenal
    from base60lab.core.rational import Rational

    with pytest.raises(ValueError):
        tan_dozenal(Rational(1, 24))
def test_trigvalue_mul_not_implemented():
    """Test TrigValue.__mul__ returns NotImplemented for unsupported types."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1), 2)
    result = v.__mul__("not supported")
    assert result is NotImplemented


def test_trigvalue_div_not_implemented():
    """Test TrigValue.__truediv__ returns NotImplemented for unsupported types."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    v = TrigValue(Rational(1), 2)
    result = v.__truediv__("not supported")
    assert result is NotImplemented


def test_trigvalue_normalized_square_factors():
    """Test TrigValue._normalized handles square factors (lines 150-153)."""
    from base60lab.trigonometry import TrigValue
    from base60lab.core.rational import Rational

    # √18 = 3√2 (has square factor 9)
    v = TrigValue(Rational(1), 18)
    norm = v._normalized()
    assert norm.coeff == Rational(3)
    assert norm.radicand == 2

    # √50 = 5√2 (has square factor 25)
    v = TrigValue(Rational(1), 50)
    norm = v._normalized()
    assert norm.coeff == Rational(5)
    assert norm.radicand == 2

    # 2√72 = 12√2 (has square factor 36)
    v = TrigValue(Rational(2), 72)
    norm = v._normalized()
    assert norm.coeff == Rational(12)
    assert norm.radicand == 2


def test_sin_dozenal_int_input():
    """Test sin_dozenal with int input (covers line 444)."""
    from base60lab.trigonometry import sin_dozenal
    from base60lab.core.rational import Rational

    # int input is not Rational, so goes to elif branch
    result = sin_dozenal(1)  # 1 turn = 360° = 0°
    assert result.to_rational() == Rational(0)

    result = sin_dozenal(0)  # 0 turn = 0°
    assert result.to_rational() == Rational(0)


def test_cos_dozenal_int_input():
    """Test cos_dozenal with int input (covers line 455)."""
    from base60lab.trigonometry import cos_dozenal
    from base60lab.core.rational import Rational

    result = cos_dozenal(1)  # 360°
    assert result.to_rational() == Rational(1)

    result = cos_dozenal(0)  # 0°
    assert result.to_rational() == Rational(1)


def test_tan_dozenal_int_input():
    """Test tan_dozenal with int input (covers line 466)."""
    from base60lab.trigonometry import tan_dozenal
    from base60lab.core.rational import Rational

    result = tan_dozenal(1)  # 360° = 0°
    assert result.to_rational() == Rational(0)

    result = tan_dozenal(0)  # 0°
    assert result.to_rational() == Rational(0)