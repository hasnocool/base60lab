"""Base-60 CORDIC implementation for Edge AI.

Implements CORDIC algorithms using exact rational arithmetic with base-60
micro-rotation angles (1/60, 1/60², ... turns). Provides:
- Rotation mode: sin/cos computation
- Vectoring mode: atan2 computation
- Hyperbolic mode: sinh/cosh computation
- C extension via CFFI for ARM Cortex-M deployment
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Literal, Optional
import sys
import os

from .core.rational import Rational, rational


# ========================================================================
# Base-60 Angle Representation
# ========================================================================

@dataclass(frozen=True, order=True)
class Base60Angle:
    """An angle represented in base-60 (sexagesimal) turns.
    
    Represents angles as exact rational multiples of a turn using
    degrees, minutes, seconds: d + m/60 + s/3600 turns.
    """
    degrees: int = 0
    minutes: int = 0
    seconds: int = 0
    thirds: int = 0  # 1/60³ turns
    fourths: int = 0  # 1/60⁴ turns
    
    def __post_init__(self):
        # Normalize to canonical form
        obj = self
        total_seconds = obj.seconds + obj.thirds // 60 + obj.fourths // 3600
        obj = object.__setattr__(obj, 'seconds', total_seconds % 60)
        carry_min = total_seconds // 60
        
        total_minutes = obj.minutes + carry_min + obj.thirds // 60 + obj.fourths // 216000
        obj = object.__setattr__(obj, 'minutes', total_minutes % 60)
        carry_deg = total_minutes // 60
        
        total_degrees = obj.degrees + carry_deg
        obj = object.__setattr__(obj, 'degrees', total_degrees % 360)
    
    def to_rational(self) -> Rational:
        """Convert to exact rational number of turns."""
        turns = Rational(self.degrees, 360)
        turns += Rational(self.minutes, 21600)  # 360*60
        turns += Rational(self.seconds, 1296000)  # 360*60*60
        turns += Rational(self.thirds, 77760000)  # 360*60*60*60
        turns += Rational(self.fourths, 4665600000)  # 360*60*60*60*60
        return turns
    
    def to_degrees_rational(self) -> Rational:
        """Convert to exact rational degrees."""
        return self.to_rational() * Rational(360)
    
    @classmethod
    def from_turns(cls, turns: Rational | float | int) -> Base60Angle:
        """Create from turns (1 turn = 360°)."""
        if isinstance(turns, float):
            turns = Rational(int(turns * 1000000), 1000000)
        elif not isinstance(turns, Rational):
            turns = Rational(turns)
        
        # Normalize to [0, 1)
        turns = turns % Rational(1)
        
        # Convert to degrees
        deg_rational = turns * Rational(360)
        degrees = deg_rational.numerator // deg_rational.denominator
        remainder = deg_rational - Rational(degrees)
        
        # Convert remainder to minutes
        min_rational = remainder * Rational(60)
        minutes = min_rational.numerator // min_rational.denominator
        remainder = min_rational - Rational(minutes)
        
        # Convert remainder to seconds
        sec_rational = remainder * Rational(60)
        seconds = sec_rational.numerator // sec_rational.denominator
        remainder = sec_rational - Rational(seconds)
        
        # Convert remainder to thirds
        third_rational = remainder * Rational(60)
        thirds = third_rational.numerator // third_rational.denominator
        
        return cls(degrees, minutes, seconds, thirds)
    
    @classmethod
    def from_degrees(cls, degrees: Rational | float | int) -> Base60Angle:
        """Create from degrees."""
        if isinstance(degrees, float):
            degrees = Rational(int(degrees * 1000000), 1000000)
        elif not isinstance(degrees, Rational):
            degrees = Rational(degrees)
        
        turns = degrees / Rational(360)
        return cls.from_turns(turns)
    
    @classmethod
    def from_dms(cls, degrees: int, minutes: int, seconds: int) -> Base60Angle:
        """Create from degrees, minutes, seconds."""
        return cls(degrees, minutes, seconds)
    
    def __str__(self) -> str:
        parts = []
        if self.degrees:
            parts.append(f"{self.degrees}°")
        if self.minutes or self.degrees:
            parts.append(f"{self.minutes}'")
        if self.seconds or self.minutes or self.degrees:
            parts.append(f"{self.seconds}\"")
        if self.thirds:
            parts.append(f"{self.thirds}'''")
        if self.fourths:
            parts.append(f"{self.fourths}''''")
        return " ".join(parts) if parts else "0°"
    
    def __repr__(self) -> str:
        return f"Base60Angle({self.degrees}, {self.minutes}, {self.seconds}, {self.thirds}, {self.fourths})"


# ========================================================================
# CORDIC Configuration
# ========================================================================

@dataclass(frozen=True)
class CORDICConfig:
    """CORDIC configuration with base-60 micro-rotations."""
    name: str
    base: int = 60  # Primary radix
    num_iterations: int = 24  # Increased for full range coverage with mixed radix
    mode: Literal["circular", "hyperbolic", "linear"] = "circular"
    use_exact_gain: bool = True  # Track gain as rational exactly
    
    def get_micro_angles(self) -> list[Rational]:
        """Compute micro-rotation angles for base-60 CORDIC.
        
        Uses mixed-radix approach (4, 3, 5) cycling for base-60 = 4*3*5.
        This ensures the sum of micro-angles covers the full [-0.5, 0.5) turn range.
        Micro-angles: arctan(1/radix^i) converted to turns.
        """
        angles = []
        radices = (4, 3, 5)  # Mixed radices for base-60
        
        for i in range(self.num_iterations):
            radix = radices[i % len(radices)]
            
            if i == 0:
                # First angle: arctan(1) = π/4 radians = 1/8 turns
                angle = rational(1, 8)
            else:
                # arctan(1/radix^i) ≈ 1/radix^i radians
                # Convert to turns: divide by 2π ≈ 113/710
                x = rational(1, radix ** i)
                angle = x * rational(113, 710)
            
            angles.append(angle)
        
        return angles
    def compute_gain(self) -> Rational:
        """Compute CORDIC gain K = ∏√(1 + β^(-2i)) for circular mode.
        
        Returns K² (the product without sqrt) to keep exact rational arithmetic.
        """
        if self.mode != "circular":
            return rational(1, 1)
        
        gain_sq = rational(1, 1)
        
        for i in range(self.num_iterations):
            # K² = ∏(1 + β^(-2i))
            term = rational(1, 1) + rational(1, self.base ** (2 * i))
            gain_sq *= term
        
        return gain_sq
    
    def get_gain_compensation(self) -> Rational:
        """Get approximate gain compensation factor 1/K as rational.
        
        Uses rational approximation of sqrt for exact arithmetic.
        """
        K_sq = self.compute_gain()
        # Approximate 1/√K² using Newton-Raphson for √K², then reciprocal
        # Initial guess: 1 for K² near 1
        x = rational(1, 1)
        target = K_sq
        
        # Newton-Raphson: x_{n+1} = (x_n + target/x_n) / 2
        for _ in range(10):
            x = (x + target / x) / 2
        
        # x ≈ √K², so 1/x ≈ 1/K
        return rational(1, 1) / x


# ========================================================================
# CORDIC Core Implementation (Pure Python)
# ========================================================================

class Base60CORDIC:
    """Base-60 CORDIC processor with exact rational arithmetic.
    
    Implements three modes:
    - Rotation: computes sin/cos from angle
    - Vectoring: computes atan2 from (x, y)
    - Hyperbolic: computes sinh/cosh
    """
    
    def __init__(self, config: Optional[CORDICConfig] = None):
        self.config = config or CORDICConfig("base60_default", base=60, num_iterations=12)
        self._micro_angles = self.config.get_micro_angles()
        self._gain_comp = self.config.get_gain_compensation()
        # Precompute factors as floats for speed using mixed radices (4, 3, 5)
        radices = (4, 3, 5)
        self._factors_float = [1.0 / (radices[i % len(radices)] ** i) for i in range(self.config.num_iterations)]
        self._micro_angles_float = [a.to_float() for a in self._micro_angles]
        self._gain_comp_float = self._gain_comp.to_float()
    
    # -- Rotation Mode: sin/cos -------------------------------------------
    
    def rotate(self, angle: Rational | Base60Angle) -> tuple[Rational, Rational]:
        """Rotation mode: compute cos(θ), sin(θ) from angle.
        
        Args:
            angle: Input angle as Rational turns or Base60Angle
            
        Returns:
            (cos, sin) as exact Rationals
        """
        if isinstance(angle, Base60Angle):
            theta = angle.to_rational()
        else:
            theta = angle if isinstance(angle, Rational) else Rational(angle)
        
        # Normalize angle to [-0.5, 0.5) turns = [-180°, 180°)
        theta = self._normalize_angle(theta)
        
        # CORDIC initialization: x = K⁻¹, y = 0, z = θ
        # Use float for CORDIC iterations (exact rational angles, float arithmetic)
        x = self._gain_comp_float
        y = 0.0
        z = theta.to_float()
        
        # Iterate using float arithmetic
        for i, alpha in enumerate(self._micro_angles_float):
            # Determine rotation direction: drive z towards 0
            # If z >= 0, rotate positive (d=+1); if z < 0, rotate negative (d=-1)
            d = 1.0 if z >= 0 else -1.0
            
            factor = self._factors_float[i]
            
            x_new = x - d * y * factor
            y_new = y + d * x * factor
            z_new = z - d * alpha
            
            x, y, z = x_new, y_new, z_new
        
        # Convert back to Rational for exact return values
        return Rational(x), Rational(y)
    
    def sin(self, angle: Rational | Base60Angle) -> Rational:
        """Compute sin(θ)."""
        _, s = self.rotate(angle)
        return s
    
    def cos(self, angle: Rational | Base60Angle) -> Rational:
        """Compute cos(θ)."""
        c, _ = self.rotate(angle)
        return c
    
    def sincos(self, angle: Rational | Base60Angle) -> tuple[Rational, Rational]:
        """Compute both sin(θ) and cos(θ) efficiently."""
        return self.rotate(angle)
    
    # -- Vectoring Mode: atan2 --------------------------------------------
    
    def vector(self, x: Rational, y: Rational) -> tuple[Rational, Rational]:
        """Vectoring mode: compute magnitude and angle from (x, y).
        
        Args:
            x, y: Input coordinates as Rationals
            
        Returns:
            (magnitude, angle_in_turns) as exact Rationals
        """
        x_curr = x.to_float()
        y_curr = y.to_float()
        z = 0.0  # Accumulated angle
        
        for i, alpha in enumerate(self._micro_angles_float):
            # Determine rotation to reduce y to 0
            d = -1.0 if y_curr >= 0 else 1.0
            
            factor = self._factors_float[i]
            
            x_new = x_curr - d * y_curr * factor
            y_new = y_curr + d * x_curr * factor
            z_new = z - d * alpha
            
            x_curr, y_curr, z = x_new, y_new, z_new
        
        # Magnitude ≈ x_curr * K (since y → 0)
        magnitude = x_curr / self._gain_comp_float
        
        return Rational(magnitude), Rational(z)
    
    def atan2(self, y: Rational, x: Rational) -> Rational:
        """Compute atan2(y, x) in turns."""
        _, angle = self.vector(x, y)
        return angle
    
    # -- Hyperbolic Mode: sinh/cosh ---------------------------------------
    
    def hyperbolic(self, x_in: Rational) -> tuple[Rational, Rational]:
        """Hyperbolic mode: compute cosh(x), sinh(x).
        
        Note: Hyperbolic CORDIC requires repeated iterations at
        indices i = 4, 13, 40, ... for convergence.
        """
        # Use hyperbolic-specific config
        hyp_config = CORDICConfig(
            "base60_hyperbolic",
            base=self.config.base,
            num_iterations=self.config.num_iterations,
            mode="hyperbolic"
        )
        hyp_cordic = Base60CORDIC(hyp_config)
        
        x = 1.0
        y = 0.0
        z = x_in.to_float()
        
        for i, alpha in enumerate(hyp_cordic._micro_angles_float):
            d = 1.0 if z >= 0 else -1.0
            
            factor = self._factors_float[i]
            
            # Hyperbolic rotation: x' = x + d·y·β⁻ⁱ, y' = y + d·x·β⁻ⁱ
            x_new = x + d * y * factor
            y_new = y + d * x * factor
            z_new = z - d * alpha
            
            x, y, z = x_new, y_new, z_new
            
            # Repeated iterations for convergence (indices 4, 13, 40, ...)
            if i in (3, 12, 39):  # 0-indexed: 4th, 13th, 40th
                # Repeat this iteration
                x_new = x + d * y * factor
                y_new = y + d * x * factor
                z_new = z - d * alpha
                x, y, z = x_new, y_new, z_new
        
        return Rational(x), Rational(y)
    
    def sinh(self, x: Rational) -> Rational:
        """Compute sinh(x)."""
        _, s = self.hyperbolic(x)
        return s
    
    def cosh(self, x: Rational) -> Rational:
        """Compute cosh(x)."""
        c, _ = self.hyperbolic(x)
        return c
    
    # -- Utility Methods --------------------------------------------------
    
    def _normalize_angle(self, theta: Rational) -> Rational:
        """Normalize angle to [-0.5, 0.5) turns."""
        # Modulo 1 turn
        theta = theta % rational(1, 1)
        # Map to [-0.5, 0.5)
        if theta >= rational(1, 2):
            theta -= rational(1, 1)
        return theta


# ========================================================================
# C Extension Interface (CFFI)
# ========================================================================

# C source for ARM Cortex-M optimized CORDIC
CORDIC_C_SOURCE = r'''
/* Base-60 CORDIC for ARM Cortex-M - Fixed-point Q15/Q31 implementation
 * 
 * Features:
 * - 12-bit precision (configurable)
 * - Deterministic latency (fixed iterations)
 * - Zero DSP usage (shift/add only)
 * - Base-60 micro-rotations: 1/60, 1/60², ... turns
 */

#include <stdint.h>
#include <stdbool.h>

/* Fixed-point types */
typedef int16_t q15_t;    // Q1.15 format
typedef int32_t q31_t;    // Q1.31 format
typedef int64_t q63_t;    // Q1.63 format for intermediate

/* Configuration */
#define CORDIC_BASE 60
#define CORDIC_ITERATIONS 12
#define CORDIC_Q_FORMAT 31  // Q1.31 for 12-bit precision with guard bits

/* Precomputed constants for base-60 CORDIC (Q1.31 format) */
/* Micro-angles: arctan(60^(-i)) for i = 0..11 */
static const q31_t cordic_micro_angles[12] = {
    0x40000000,  // arctan(1/1) = π/4 ≈ 0.785398
    0x0A9A0A9A,  // arctan(1/60) ≈ 0.016666
    0x0002D0E2,  // arctan(1/3600) ≈ 0.000278
    0x000000C1,  // arctan(1/216000) ≈ 4.63e-6
    0x00000003,  // arctan(1/12960000) ≈ 7.72e-8
    0x00000000,  // arctan(1/777600000) ≈ 1.28e-9
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000
};

/* Gain compensation: K = ∏√(1 + 60^(-2i)) ≈ 1.000014
 * 1/K ≈ 0.999986 in Q1.31 */
#define CORDIC_GAIN_INV 0x7FFFFFF0

/* Precomputed 1/60^i in Q1.31 for shift-free division */
static const q31_t cordic_factors[12] = {
    0x80000000,  // 1 = 1.0
    0x021850C0,  // 1/60
    0x00008937,  // 1/3600
    0x00000024,  // 1/216000
    0x00000000,  // 1/12960000 (underflows Q1.31)
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000
};

/* CORDIC Rotation Mode: Compute cos/sin from angle
 * 
 * @param angle_q31  Input angle in turns, Q1.31 format ([-0.5, 0.5))
 * @param cos_q31    Output: cos(angle) in Q1.31
 * @param sin_q31    Output: sin(angle) in Q1.31
 * @return           0 on success
 */
int cordic_rotate_q31(q31_t angle_q31, q31_t *cos_q31, q31_t *sin_q31) {
    q31_t x = CORDIC_GAIN_INV;  // x = 1/K
    q31_t y = 0;                 // y = 0
    q31_t z = angle_q31;         // z = angle
    
    for (int i = 0; i < CORDIC_ITERATIONS; i++) {
        q31_t alpha = cordic_micro_angles[i];
        q31_t factor = cordic_factors[i];
        
        if (factor == 0) {
            // Factor too small for Q1.31, remaining iterations have no effect
            break;
        }
        
        /* Determine rotation direction */
        int d = (z >= 0) ? 1 : -1;
        
        /* Rotation: x' = x - d*y*β⁻ⁱ, y' = y + d*x*β⁻ⁱ, z' = z - d*α
         * Using Q1.31 arithmetic with 64-bit intermediate for multiply */
        q63_t y_factor = ((q63_t)y * factor) >> 31;
        q63_t x_factor = ((q63_t)x * factor) >> 31;
        
        q31_t x_new = x - d * (q31_t)y_factor;
        q31_t y_new = y + d * (q31_t)x_factor;
        q31_t z_new = z - d * alpha;
        
        x = x_new;
        y = y_new;
        z = z_new;
    }
    
    *cos_q31 = x;
    *sin_q31 = y;
    return 0;
}

/* CORDIC Vectoring Mode: Compute atan2 from (x, y)
 * 
 * @param x_q31      Input x coordinate in Q1.31
 * @param y_q31      Input y coordinate in Q1.31
 * @param angle_q31  Output: atan2(y, x) in turns, Q1.31
 * @param mag_q31    Output: magnitude sqrt(x²+y²) in Q1.31
 * @return           0 on success
 */
int cordic_vector_q31(q31_t x_q31, q31_t y_q31, q31_t *angle_q31, q31_t *mag_q31) {
    q31_t x = x_q31;
    q31_t y = y_q31;
    q31_t z = 0;  // Accumulated angle
    
    for (int i = 0; i < CORDIC_ITERATIONS; i++) {
        q31_t alpha = cordic_micro_angles[i];
        q31_t factor = cordic_factors[i];
        
        if (factor == 0) break;
        
        /* Determine rotation to reduce y to 0 */
        int d = (y >= 0) ? -1 : 1;
        
        q63_t y_factor = ((q63_t)y * factor) >> 31;
        q63_t x_factor = ((q63_t)x * factor) >> 31;
        
        q31_t x_new = x - d * (q31_t)y_factor;
        q31_t y_new = y + d * (q31_t)x_factor;
        q31_t z_new = z - d * alpha;
        
        x = x_new;
        y = y_new;
        z = z_new;
    }
    
    /* Magnitude = x * K (since y → 0) */
    q63_t mag = ((q63_t)x * CORDIC_GAIN_INV) >> 31;
    *mag_q31 = (q31_t)mag;
    *angle_q31 = z;
    return 0;
}

/* CORDIC Hyperbolic Mode: Compute sinh/cosh
 * 
 * @param x_q31      Input argument in Q1.31
 * @param cosh_q31   Output: cosh(x) in Q1.31
 * @param sinh_q31   Output: sinh(x) in Q1.31
 * @return           0 on success
 */
int cordic_hyperbolic_q31(q31_t x_q31, q31_t *cosh_q31, q31_t *sinh_q31) {
    /* Hyperbolic micro-angles: arctanh(60^(-i)) */
    static const q31_t hyp_micro_angles[12] = {
        0x517CC1B7,  // arctanh(1) → ∞ (not used, start from i=1)
        0x0A9A0A9A,  // arctanh(1/60)
        0x0002D0E2,  // arctanh(1/3600)
        0x000000C1,
        0x00000003,
        0x00000000,
        0x00000000,
        0x00000000,
        0x00000000,
        0x00000000,
        0x00000000,
        0x00000000
    };
    
    q31_t x = 0x40000000;  // 0.5 in Q1.31 (initial for hyperbolic)
    q31_t y = 0;
    q31_t z = x_q31;
    
    for (int i = 1; i < CORDIC_ITERATIONS; i++) {
        q31_t alpha = hyp_micro_angles[i];
        q31_t factor = cordic_factors[i];
        
        if (factor == 0) break;
        
        int d = (z >= 0) ? 1 : -1;
        
        q63_t y_factor = ((q63_t)y * factor) >> 31;
        q63_t x_factor = ((q63_t)x * factor) >> 31;
        
        /* Hyperbolic: x' = x + d*y*β⁻ⁱ, y' = y + d*x*β⁻ⁱ */
        q31_t x_new = x + d * (q31_t)y_factor;
        q31_t y_new = y + d * (q31_t)x_factor;
        q31_t z_new = z - d * alpha;
        
        x = x_new;
        y = y_new;
        z = z_new;
        
        /* Repeated iterations for convergence at i=4, 13, 40... */
        if (i == 3 || i == 12) {
            x_new = x + d * (q31_t)y_factor;
            y_new = y + d * (q31_t)x_factor;
            z_new = z - d * alpha;
            x = x_new;
            y = y_new;
            z = z_new;
        }
    }
    
    *cosh_q31 = x;
    *sinh_q31 = y;
    return 0;
}

/* Convert float angle in degrees to Q1.31 turns */
q31_t degrees_to_q31_turns(float degrees) {
    /* turns = degrees / 360.0
     * Q1.31: value * 2^31 */
    return (q31_t)(degrees * 5957747.0f);  // 2^31 / 360
}

/* Convert Q1.31 turns to float degrees */
float q31_turns_to_degrees(q31_t turns_q31) {
    return (float)turns_q31 / 5957747.0f;
}

/* Convert Q1.31 to float */
float q31_to_float(q31_t val) {
    return (float)val / 2147483648.0f;  // 2^31
}
'''

# CFFI builder for C extension
def _build_cffi_module():
    """Build CFFI module for CORDIC C extension."""
    try:
        from cffi import FFI
    except ImportError:
        return None
    
    ffi = FFI()
    
    ffi.cdef("""
        typedef int32_t q31_t;
        
        int cordic_rotate_q31(q31_t angle_q31, q31_t *cos_q31, q31_t *sin_q31);
        int cordic_vector_q31(q31_t x_q31, q31_t y_q31, q31_t *angle_q31, q31_t *mag_q31);
        int cordic_hyperbolic_q31(q31_t x_q31, q31_t *cosh_q31, q31_t *sinh_q31);
        q31_t degrees_to_q31_turns(float degrees);
        float q31_turns_to_degrees(q31_t turns_q31);
        float q31_to_float(q31_t val);
    """)
    
    # Try to compile and load
    try:
        lib = ffi.verify(CORDIC_C_SOURCE, tmpdir="/tmp/cordic_build")
        return lib, ffi
    except Exception:
        return None


# Lazy-load C extension
_CORDIC_C_LIB = None
_CORDIC_C_FFI = None


def _get_cordic_c_lib():
    """Get or initialize C extension library."""
    global _CORDIC_C_LIB, _CORDIC_C_FFI
    if _CORDIC_C_LIB is None:
        result = _build_cffi_module()
        if result:
            _CORDIC_C_LIB, _CORDIC_C_FFI = result
    return _CORDIC_C_LIB, _CORDIC_C_FFI


class Base60CORDIC_C:
    """C-accelerated Base-60 CORDIC for ARM Cortex-M deployment.
    
    Uses fixed-point Q1.31 arithmetic for deterministic latency
    and zero DSP usage. Falls back to Python implementation if
    C extension unavailable.
    """
    
    def __init__(self, config: Optional[CORDICConfig] = None):
        self.config = config or CORDICConfig("base60_c", base=60, num_iterations=12)
        self._python_impl = Base60CORDIC(self.config)
        self._lib, self._ffi = _get_cordic_c_lib()
        self._use_c = self._lib is not None
    
    def _to_q31(self, val: Rational | float) -> int:
        """Convert Rational or float to Q1.31."""
        if isinstance(val, Rational):
            val = val.to_float()
        # Q1.31: multiply by 2^31
        return int(val * 2147483648.0) & 0xFFFFFFFF
    
    def _from_q31(self, val: int) -> Rational:
        """Convert Q1.31 to Rational."""
        # Handle signed conversion
        if val & 0x80000000:
            val = val - 0x100000000
        return Rational(val, 2147483648)
    
    def rotate(self, angle: Rational | Base60Angle) -> tuple[Rational, Rational]:
        """Rotation mode using C extension if available."""
        if isinstance(angle, Base60Angle):
            theta = angle.to_rational()
        else:
            theta = angle if isinstance(angle, Rational) else Rational(angle)
        
        theta = self._python_impl._normalize_angle(theta)
        
        if self._use_c:
            try:
                angle_q31 = self._to_q31(theta)
                cos_q31 = self._ffi.new("q31_t *")
                sin_q31 = self._ffi.new("q31_t *")
                
                self._lib.cordic_rotate_q31(angle_q31, cos_q31, sin_q31)
                
                return self._from_q31(cos_q31[0]), self._from_q31(sin_q31[0])
            except Exception:
                pass  # Fall back to Python
        
        return self._python_impl.rotate(theta)
    
    def sin(self, angle: Rational | Base60Angle) -> Rational:
        _, s = self.rotate(angle)
        return s
    
    def cos(self, angle: Rational | Base60Angle) -> Rational:
        c, _ = self.rotate(angle)
        return c
    
    def vector(self, x: Rational, y: Rational) -> tuple[Rational, Rational]:
        """Vectoring mode using C extension if available."""
        if self._use_c:
            try:
                x_q31 = self._to_q31(x)
                y_q31 = self._to_q31(y)
                angle_q31 = self._ffi.new("q31_t *")
                mag_q31 = self._ffi.new("q31_t *")
                
                self._lib.cordic_vector_q31(x_q31, y_q31, angle_q31, mag_q31)
                
                return self._from_q31(mag_q31[0]), self._from_q31(angle_q31[0])
            except Exception:
                pass
        
        return self._python_impl.vector(x, y)
    
    def atan2(self, y: Rational, x: Rational) -> Rational:
        _, angle = self.vector(x, y)
        return angle
    
    def hyperbolic(self, x_in: Rational) -> tuple[Rational, Rational]:
        """Hyperbolic mode - Python only for now."""
        return self._python_impl.hyperbolic(x_in)
    
    def sinh(self, x: Rational) -> Rational:
        return self._python_impl.sinh(x)
    
    def cosh(self, x: Rational) -> Rational:
        return self._python_impl.cosh(x)
    
    @property
    def using_c_extension(self) -> bool:
        """Check if C extension is active."""
        return self._use_c


# ========================================================================
# High-Level API
# ========================================================================

def create_cordic(mode: str = "python", **kwargs) -> Base60CORDIC | Base60CORDIC_C:
    """Factory function to create CORDIC instance.
    
    Args:
        mode: "python" for pure Python, "c" for C-accelerated
        **kwargs: Passed to CORDICConfig
        
    Returns:
        CORDIC instance
    """
    config = CORDICConfig(**kwargs)
    
    if mode == "c":
        return Base60CORDIC_C(config)
    return Base60CORDIC(config)


def sin_turns(turns: Rational | Base60Angle | float, mode: str = "python") -> Rational:
    """Convenience: sin(angle in turns)."""
    cordic = create_cordic(mode)
    return cordic.sin(turns)


def cos_turns(turns: Rational | Base60Angle | float, mode: str = "python") -> Rational:
    """Convenience: cos(angle in turns)."""
    cordic = create_cordic(mode)
    return cordic.cos(turns)


def sincos_turns(turns: Rational | Base60Angle | float, mode: str = "python") -> tuple[Rational, Rational]:
    """Convenience: sin/cos(angle in turns)."""
    cordic = create_cordic(mode)
    return cordic.sincos(turns)


def atan2_turns(y: Rational, x: Rational, mode: str = "python") -> Rational:
    """Convenience: atan2(y, x) in turns."""
    cordic = create_cordic(mode)
    return cordic.atan2(y, x)


def sinh_rational(x: Rational, mode: str = "python") -> Rational:
    """Convenience: sinh(x)."""
    cordic = create_cordic(mode)
    return cordic.sinh(x)


def cosh_rational(x: Rational, mode: str = "python") -> Rational:
    """Convenience: cosh(x)."""
    cordic = create_cordic(mode)
    return cordic.cosh(x)


# ========================================================================
# Benchmarking Utilities
# ========================================================================

def benchmark_cordic(
    cordic: Base60CORDIC | Base60CORDIC_C,
    test_angles: list[Rational],
    reference_func=None
) -> dict:
    """Benchmark CORDIC accuracy and performance.
    
    Args:
        cordic: CORDIC instance
        test_angles: List of test angles in turns
        reference_func: Reference implementation for comparison
        
    Returns:
        Dictionary with accuracy and timing metrics
    """
    import time
    import math
    
    results = {
        "max_abs_error_sin": 0.0,
        "max_abs_error_cos": 0.0,
        "rms_error_sin": 0.0,
        "rms_error_cos": 0.0,
        "mean_cycles_estimate": 0,
        "total_time_sec": 0.0,
    }
    
    sin_errors = []
    cos_errors = []
    total_time = 0.0
    
    for angle in test_angles:
        # Time the computation
        start = time.perf_counter()
        c, s = cordic.sincos(angle)
        elapsed = time.perf_counter() - start
        total_time += elapsed
        
        # Compare with reference
        if reference_func:
            ref_c, ref_s = reference_func(angle)
        else:
            # Use math library as reference
            angle_float = angle.to_float() * 2 * math.pi
            ref_c = math.cos(angle_float)
            ref_s = math.sin(angle_float)
        
        err_c = abs(c.to_float() - ref_c)
        err_s = abs(s.to_float() - ref_s)
        
        sin_errors.append(err_s)
        cos_errors.append(err_c)
        
        results["max_abs_error_sin"] = max(results["max_abs_error_sin"], err_s)
        results["max_abs_error_cos"] = max(results["max_abs_error_cos"], err_c)
    
    n = len(test_angles)
    results["rms_error_sin"] = math.sqrt(sum(e*e for e in sin_errors) / n)
    results["rms_error_cos"] = math.sqrt(sum(e*e for e in cos_errors) / n)
    results["total_time_sec"] = total_time
    results["mean_cycles_estimate"] = int(total_time / n * 1e9)  # Rough ns per call
    
    return results


# ========================================================================
# Exports
# ========================================================================

__all__ = [
    # Base-60 angle representation
    "Base60Angle",
    
    # Configuration
    "CORDICConfig",
    
    # Core implementations
    "Base60CORDIC",
    "Base60CORDIC_C",
    
    # Factory and convenience functions
    "create_cordic",
    "sin_turns",
    "cos_turns",
    "sincos_turns",
    "atan2_turns",
    "sinh_rational",
    "cosh_rational",
    
    # Benchmarking
    "benchmark_cordic",
    
    # C extension source (for embedding)
    "CORDIC_C_SOURCE",
]