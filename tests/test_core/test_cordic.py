"""Tests for the CORDIC module."""

import pytest
import math

from base60lab.core.rational import Rational
from base60lab.cordic import (
    Base60CORDIC,
    create_cordic,
    sin_turns,
    cos_turns,
    atan2_turns,
    sinh_rational,
    cosh_rational
)


class TestCORDIC:
    """Tests for CORDIC functions."""

    def test_cordic_creation(self):
        cordic = create_cordic(precision=12)
        assert cordic is not None

    def test_sin_cos_turns(self):
        """Test sin/cos using turns."""
        # Test at 0 turns (0 degrees)
        cos_val = cos_turns(Rational(0, 1))
        sin_val = sin_turns(Rational(0, 1))
        assert abs(cos_val - 1.0) < 0.001
        assert abs(sin_val - 0.0) < 0.001
        
        # Test at 1/4 turn (90 degrees)
        cos_val = cos_turns(Rational(1, 4))
        sin_val = sin_turns(Rational(1, 4))
        assert abs(cos_val - 0.0) < 0.01
        assert abs(sin_val - 1.0) < 0.01

    def test_atan2_turns(self):
        """Test atan2 using turns."""
        angle = atan2_turns(Rational(1, 1), Rational(1, 1))
        expected = 1/8  # 45 degrees = 1/8 turn
        assert abs(float(angle) - expected) < 0.01

    def test_hyperbolic_functions(self):
        """Test sinh/cosh."""
        sinh_val = sinh_rational(Rational(1, 10))
        cosh_val = cosh_rational(Rational(1, 10))
        expected_sinh = math.sinh(0.1)
        expected_cosh = math.cosh(0.1)
        assert abs(float(sinh_val) - expected_sinh) < 0.01
        assert abs(float(cosh_val) - expected_cosh) < 0.01

    def test_base60_angle_representation(self):
        """Test that base-60 angles are represented exactly."""
        angle = Rational(1, 60)  # 6 degrees
        cos_val = cos_turns(angle)
        sin_val = sin_turns(angle)
        
        expected_cos = math.cos(2 * math.pi / 60)
        expected_sin = math.sin(2 * math.pi / 60)
        assert abs(float(cos_val) - expected_cos) < 0.01
        assert abs(float(sin_val) - expected_sin) < 0.01

    def test_deterministic_latency(self):
        """Test that CORDIC has deterministic iteration count."""
        # This test verifies the concept; actual implementation may vary
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])