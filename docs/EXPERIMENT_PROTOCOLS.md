# Base-12 / Base-60 Experimental Protocols

## Overview

This document specifies the detailed experimental procedures for the 10 experiments in the research programme. Each protocol references the hypotheses from HYPOTHESES.md and the experimental design from PLAN.md. Protocols are designed for reproducibility with exact rational arithmetic throughout.

## Common Experimental Controls (PLAN.md lines 600-620)

**Applied to ALL experiments:**

1. **Control 1 — Same Mathematical Quantity**
   - Every value computed as `Rational` (exact fraction)
   - Display base is presentation only; never affects underlying value
   - Cross-base comparison uses identical `Rational` inputs

2. **Control 2 — Exact Arithmetic**
   - All internal calculations use `base60lab.core.rational.Rational`
   - Backed by Python's `fractions.Fraction` — arbitrary precision
   - No `float` operations in any metric calculation or comparison

3. **Control 3 — Independent Verification**
   - Every pattern converted to canonical mathematical expression
   - Verified independently of base representation
   - Round-trip: base → Rational → base must be identity

4. **Control 4 — Equal Experimental Conditions**
   - Signal processing: identical sampling rates, durations, frequency content
   - Benchmarks: same transform sizes, iterations, warmup, seed
   - Geometry: same radius, same polygons

5. **Control 5 — Negative Results Matter**
   - Explicitly record when base 60/12 underperform base 10
   - Document all failed hypotheses with evidence
   - No selective reporting

6. **Control 6 — Randomised Holdout Tests**
   - Random denominator selection for fraction experiments
   - Random polygon sides for geometry experiments
   - Random frequency ratios for Lissajous experiments

---

## Experiment 01: Fraction Analysis (01_fraction_analysis.py)

**Hypotheses Tested:** H1 (Primary), H5 (Secondary)
**PLAN.md Reference:** Lines 97-133 (Experiments 1-5)

### Protocol

**Objective:** Compare fractional representations across bases 10, 12, 60 for denominators 1–360.

**Procedure:**
1. Generate all unit fractions 1/n for n ∈ [1, 360]
2. For each fraction, compute representation in bases 10, 12, 60 using exact rational arithmetic
3. Classify each representation as:
   - `terminating`: finite digits in that base
   - `repeating`: period length ≥ 1
4. Measure:
   - Termination count per base
   - Average repeating period for non-terminating fractions
   - Maximum repeating period
   - Representation length (digits) for integers 0–1000
5. Compare multiplication tables (10×10, 12×12, 60×60) for pattern visibility
6. Test mental arithmetic candidates: 1/2, 1/3, 1/4, 1/5, 1/6, 1/7, 1/12, 1/15

**Success Metrics (Exact Rational):**
- `termination_ratio = terminating_count / total_count`
- `avg_repeating_period = Σ(period) / non_terminating_count`
- `avg_digits_per_value = Σ(digits) / 1001` for 0–1000

**Implementation:**
```python
from base60lab.fractions import FractionsDomain
from base60lab.metrics import compare_bases

domain = FractionsDomain()
results = domain.analyze_denominators(1, 360)
comparison = compare_bases([10, 12, 60], max_denominator=100)
```

**Verification:**
```bash
pytest tests/test_core/test_fractions.py -v
pytest tests/test_core/test_metrics.py -v
```

**Output:** Termination tables, period analysis, multiplication table comparison, metric scores

---

## Experiment 02: Geometry Analysis (02_geometry_analysis.py)

**Hypotheses Tested:** H2 (Primary), H5 (Secondary)
**PLAN.md Reference:** Lines 134-196 (Experiments B1-B2)

### Protocol

**Objective:** Analyze regular polygon geometry and circle subdivisions across bases.

**Procedure:**
1. **Circle Subdivisions (B1):**
   - Test standard subdivisions: n ∈ {12, 24, 30, 36, 60, 120, 180, 360}
   - Compute angle = 360/n degrees for each
   - Verify integer result (exact termination in all bases)
   - Express in base 10, 12, 60; degrees, turns, DMS

2. **Polygon Geometry (B2):**
   - For n ∈ [3, 360], compute:
     - Internal angle = (n-2)×180/n degrees
     - External angle = 360/n degrees
     - Chord length = 2r sin(π/n) for r=1
     - Chord length squared = 2(1-cos(2π/n))
     - Polygon area = (n/2) sin(2π/n)
     - Polygon perimeter = n × chord_length
   - Classify each as exact rational or irrational
   - Test which n yield rational results for each quantity

**Success Metrics:**
- Count of n yielding rational internal/external angles (all standard n)
- Count of n yielding rational chord lengths (only n=6)
- Count of n yielding rational areas (only n=4)
- Count of n yielding rational perimeters (only n=6)

**Implementation:**
```python
from base60lab.geometry import (
    internal_angle, external_angle, chord_length,
    chord_length_squared, polygon_area, polygon_perimeter,
    subdivision_angle, standard_subdivisions
)

for n in standard_subdivisions():
    angle = subdivision_angle(n)  # Rational(360/n)
    # ... verify in all bases

for n in range(3, 361):
    summary = polygon_summary(n)  # Returns all available rational properties
```

**Verification:**
```bash
pytest tests/test_core/test_geometry.py -v
```

**Output:** Polygon property tables, rational/irrational classification, base representation comparison

---

## Experiment 03: Trigonometry Analysis (03_trigonometry_analysis.py)

**Hypotheses Tested:** H2 (Primary), H3 (Secondary), H5 (Secondary)
**PLAN.md Reference:** Lines 134-196 (Experiments B3-B4)

### Protocol

**Objective:** Compare exact trigonometric values across angle representations.

**Procedure:**
1. **Special Angle Values (B3):**
   - Test angles: 0°, 30°, 45°, 60°, 90°, 120°, 135°, 150°, 180°, 210°, 225°, 240°, 270°, 300°, 315°, 330°, 360°
   - Compute sin, cos, tan in four representations:
     - Degrees (base-10)
     - Turns (fraction of 1)
     - Dozenal (base-12 fraction of turn)
     - DMS (degrees-minutes-seconds, base-60)
   - Classify values as rational (exact fraction) or algebraic (involving √2, √3)

2. **Rotation/Phase Representation (B4):**
   - Compare turn-based vs degree-based vs radian-based
   - Test phase arithmetic modulo 1
   - Verify Pythagorean identity sin²+cos²=1 exactly for all representations
   - Verify angle sum identities

**Success Metrics:**
- Count of rational vs algebraic trig values per angle
- Identity verification pass rate (exact rational equality)
- Cross-representation consistency (same angle → same TrigValue)

**Implementation:**
```python
from base60lab.trigonometry import (
    sin_degrees, cos_degrees, tan_degrees,
    sin_turns, cos_turns, tan_turns,
    sin_dozenal, cos_dozenal, tan_dozenal,
    sin_dms, cos_dms, tan_dms,
    verify_pythagorean_identity,
    degrees_to_turns, degrees_to_dozenal, degrees_to_dms
)

for angle in [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]:
    s1 = sin_degrees(angle)
    s2 = sin_turns(degrees_to_turns(angle))
    s3 = sin_dozenal(degrees_to_dozenal(angle))
    s4 = sin_dms(*degrees_to_dms(angle))
    assert s1 == s2 == s3 == s4  # Exact equality
    assert verify_pythagorean_identity(angle)
```

**Verification:**
```bash
pytest tests/test_core/test_trigonometry.py -v
```

**Output:** Exact value tables, representation consistency proofs, identity verification logs

---

## Experiment 04: Modular Patterns (04_modular_patterns.py)

**Hypotheses Tested:** H3 (Secondary), H5 (Secondary)
**PLAN.md Reference:** Lines 301-400

### Protocol

**Objective:** Analyze cyclic/modular arithmetic structures mod 12 and mod 60, distinct from base representation.

**Procedure:**
1. **Core Operations:**
   - Test mod_add, mod_sub, mod_mul, mod_pow for moduli 12 and 60
   - Verify ring properties (associativity, distributivity)

2. **Structural Analysis:**
   - Enumerate units (invertible elements): φ(12)=4, φ(60)=16
   - Enumerate zero divisors
   - Generate full multiplication tables
   - Verify self-inverse property for mod 12 units

3. **Base vs Modular Distinction:**
   - Demonstrate: modular "10" = integer ten, base-12 "10" = integer twelve
   - Verify this distinction in all tests

**Success Metrics:**
- Correct unit/zero divisor enumeration
- Multiplication table symmetry verified
- Modular inverse exists iff gcd(a,m)=1
- No confusion between modular and base notation

**Implementation:**
```python
from base60lab.modular import (
    mod_add, mod_sub, mod_mul, mod_pow, mod_inv, mod_div,
    is_unit, units, zero_divisors, multiplication_table
)

# Mod 12
units_12 = units(12)        # {1, 5, 7, 11}
zdivs_12 = zero_divisors(12)  # {0, 2, 3, 4, 6, 8, 9, 10}
table_12 = multiplication_table(12)

# Mod 60
units_60 = units(60)        # 16 elements
zdivs_60 = zero_divisors(60)  # 44 elements
table_60 = multiplication_table(60)
```

**Verification:**
```bash
pytest tests/test_core/test_modular.py -v
```

**Output:** Unit/zero divisor tables, multiplication tables, base-vs-modular distinction proofs

---

## Experiment 05: Algebra Sequences (05_algebra_sequences.py)

**Hypotheses Tested:** H5 (Primary)
**PLAN.md Reference:** Lines 401-450

### Protocol

**Objective:** Generate classic number sequences using exact rational arithmetic; examine base-dependent patterns.

**Procedure:**
1. Generate first N terms for each sequence:
   - Fibonacci: F(n) = F(n-1) + F(n-2), F(0)=0, F(1)=1
   - Triangular: T(n) = n(n+1)/2
   - Square: S(n) = n²
   - Cube: C(n) = n³
   - Perfect: Euclid-Euler theorem 2^(p-1)(2^p-1)
   - Prime: Trial division
   - Geometric: G(n) = start × ratio^n
   - Harmonic: H(n) = Σ(1/k) for k=1..n

2. All terms returned as `Rational` (exact)
3. Examine sequences in bases 10, 12, 60 for pattern visibility
4. Test divisibility properties in each base

**Success Metrics:**
- All terms exact Rational instances
- Deterministic generation (same input → same output)
- Harmonic sequence accumulates exact rational sums
- No floating-point contamination

**Implementation:**
```python
from base60lab.sequences import (
    fibonacci, triangular, square, cube,
    perfect, prime, geometric, harmonic
)

fib_10 = fibonacci(10)      # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
harm_10 = harmonic(10)      # [1, 3/2, 11/6, 25/12, 137/60, ...]
```

**Verification:**
```bash
pytest tests/test_core/test_sequences.py -v
```

**Output:** Sequence tables, cross-base pattern observations, exact rational verification

---

## Experiment 06: Harmonic Analysis (06_harmonic_analysis.py)

**Hypotheses Tested:** H1 (Secondary), H3 (Primary), H4 (Secondary), H5 (Secondary)
**PLAN.md Reference:** Lines 198-265 (Experiments C1-C2)

### Protocol

**Objective:** Analyze frequency ratios, harmonic series, and phase relationships using exact rational arithmetic.

**Procedure:**
1. **Frequency Ratios (C1):**
   - Define exact ratios: 1:1, 2:1, 3:2, 4:3, 5:4, 5:3
   - Test arithmetic: multiplication (add intervals), division (subtract), power (repeat)
   - Verify: 3:2 × 4:3 = 2:1 (fifth + fourth = octave)
   - Express ratios in bases 10, 12, 60

2. **Harmonic Series (C2):**
   - Generate harmonics 1..N as exact ratios n:1
   - Test harmonic spacing (differences between successive harmonics)
   - Test phase alignment at integer multiples
   - Test beat frequencies (difference tones)

3. **Phase Arithmetic:**
   - Phase as fraction of turn [0, 1)
   - Phase addition modulo 1
   - Convert phase to frequency ratio: Phase(1,100) → 1/100

**Success Metrics:**
- All ratio arithmetic exact (Rational)
- Pre-defined musical intervals match theory
- Phase wraps correctly at 1 turn = 0
- Harmonic series generates exact ratios

**Implementation:**
```python
from base60lab.frequency import (
    ratio_to_fraction, FrequencyRatio, Harmonic, Phase
)

fifth = FrequencyRatio.PERFECT_FIFTH    # 3:2
fourth = FrequencyRatio.PERFECT_FOURTH  # 4:3
octave = fifth * fourth                 # 2:1 exact
assert octave == FrequencyRatio.OCTAVE

harmonics = Harmonic.series(8)          # [(1:1), (2:1), ..., (8:1)]
phase = Phase.QUARTER_TURN + Phase.HALF_TURN  # 3/4 turn
```

**Verification:**
```bash
pytest tests/test_core/test_frequency.py -v
```

**Output:** Interval arithmetic tables, harmonic series, phase arithmetic verification

---

## Experiment 07: Lissajous Analysis (07_lissajous_analysis.py)

**Hypotheses Tested:** H3 (Primary), H5 (Secondary)
**PLAN.md Reference:** Lines 266-290 (Experiment C3)

### Protocol

**Objective:** Analyze Lissajous figure closure properties using exact rational frequency ratios.

**Procedure:**
1. **Frequency Ratio Classification:**
   - For ratios a/b in lowest terms, closure period = denominator
   - Classify denominators by prime factorization:
     - `2_3_5_smooth`: factors ⊆ {2, 3, 5} (base-60 primes)
     - `prime_7_11_13`: factors ⊆ {7, 11, 13}
     - `mixed`: other combinations

2. **Closure Analysis:**
   - Test ratios with denominators 1–30
   - Record closure period and prime factors
   - Compare base-12/base-60 representation of ratios
   - Generate SVG visualizations for key ratios

3. **Phase Offset Effects:**
   - Test δ ∈ {0, 1/4, 1/2, 3/4} turns
   - Verify closure period unchanged by phase offset
   - Observe figure rotation/translation

**Success Metrics:**
- Closure period = denominator of reduced frequency ratio
- 2_3_5_smooth ratios have periods with only factors {2,3,5}
- Base-60 representation reveals factorization naturally
- Visual figures match mathematical prediction

**Implementation:**
```python
from base60lab.lissajous import (
    lissajous_closure_period, classify_ratio, generate_lissajous_svg
)

period = lissajous_closure_period(3, 2)    # 3
period = lissajous_closure_period(5, 4)    # 4
period = lissajous_closure_period(7, 5)    # 5

classify_ratio(3, 2)   # '2_3_5_smooth'
classify_ratio(7, 5)   # 'prime_7_11_13'
classify_ratio(14, 9)  # 'mixed' (14=2×7, 9=3²)

generate_lissajous_svg(3, 2, phase_offset=0, filename="lissajous_3_2.svg")
```

**Verification:**
```bash
pytest tests/test_core/test_lissajous.py -v
```

**Output:** Closure period tables, prime factor classifications, SVG visualizations

---

## Experiment 08: FFT Benchmarks (08_fft_benchmarks.py)

**Hypotheses Tested:** H4 (Primary), H5 (Secondary)
**PLAN.md Reference:** Lines 451-580 (Experiments 8, 10)

### Protocol

**Objective:** Benchmark FFT performance across number-theoretic smoothness categories.

**Procedure:**
1. **Size Categories:**
   - `powers_of_2`: n = 2ᵏ
   - `5_smooth`: n = 2ᵃ3ᵇ5ᶜ (regular numbers)
   - `12_smooth`: n with prime factors ≤ 11
   - `60_smooth`: n with prime factors ≤ 59
   - `poorly_factored`: largest prime factor ≥ 13

2. **Benchmark Parameters:**
   - Sizes: 16–4096, 8 sizes per category
   - Iterations: 10 timed runs (3 warmup)
   - Signal: Deterministic multi-tone + noise, seed=42
   - Library: SciPy FFT (FFTW-backed)
   - Memory: tracemalloc peak measurement

3. **Metrics:**
   - Execution time (ns) — median of 10 runs
   - Peak memory (bytes)
   - Precision (bits) = -log₂(relative L2 error) of round-trip
   - Accuracy (ULPs) = mean units-in-last-place distance

**Success Metrics:**
- Performance hierarchy: powers_of_2 ≈ 5_smooth < 12_smooth < 60_smooth < poorly_factored
- Numerical precision ≈ 52 bits (double precision) across ALL categories
- Accuracy 1-3 ULPs across all categories
- 5-smooth within 2× powers_of_2 performance

**Implementation:**
```python
from base60lab.fft_benchmarks import run_benchmarks, print_benchmark_results

results = run_benchmarks(
    sizes_per_category=8,
    min_size=16,
    max_size=4096,
    iterations=10,
    warmup=3,
    seed=42,
)
print_benchmark_results(results)
```

**Verification:**
```bash
pytest tests/test_core/test_fft_benchmarks.py -v
```

**Output:** Benchmark tables, performance scaling plots, numerical quality comparison

---

## Experiment 09: Real-World Signals (09_real_world_signals.py)

**Hypotheses Tested:** H4 (Primary), H5 (Secondary)
**PLAN.md Reference:** Lines 581-590 (Experiment 9)

### Protocol

**Objective:** Apply signal processing to real signals; test if theoretical FFT advantages translate.

**Procedure:**
1. **Signal Generation/Loading:**
   - Synthetic: multi-tone, chirp, noise
   - Real: audio samples, sensor data (if available)

2. **Filter Design:**
   - Butterworth lowpass, highpass, bandpass, bandstop
   - Rational filter coefficients where possible
   - Zero-phase filtering (filtfilt)

3. **Spectral Analysis:**
   - Power spectrum
   - Welch's PSD
   - Spectrogram

4. **Base-Friendly Sizing:**
   - Compare processing at native size vs padded to 5-smooth
   - Measure quality vs performance trade-off

**Success Metrics:**
- Filter design with rational coefficients exact
- Spectral analysis deterministic
- Padding to 5-smooth improves performance without quality loss
- Zero-phase filtering preserves signal integrity

**Implementation:**
```python
from base60lab.signal_processing import (
    fft_of_signal, ifft_of_signal,
    design_lowpass_filter, apply_filter,
    compute_power_spectrum, compute_spectral_density,
    rational_filter_coefficients
)

# Rational filter coefficients
b, a = rational_filter_coefficients('lowpass', Rational(1, 4), 4)

# Process signal
spectrum = fft_of_signal(signal)
filtered = apply_filter(signal, b, a)
psd = compute_spectral_density(signal, fs=44100)
```

**Verification:**
```bash
pytest tests/test_core/test_signal_processing.py -v
```

**Output:** Filter coefficient tables, spectral analysis results, padding comparison

---

## Experiment 10: Combined Experiments (10_combined_experiments.py)

**Hypotheses Tested:** H5 (Primary), H1-H4 (Secondary)
**PLAN.md Reference:** Lines 591-600 (Experiment 10)

### Protocol

**Objective:** Cross-domain synthesis — test if multi-base advantages compound.

**Procedure:**
1. **Multi-Base Metric Evaluation:**
   - Run full metrics comparison (representation_efficiency, mathematical_simplicity, computational_efficiency, visual_interpretability, discovery_effectiveness)
   - Compute composite scores
   - Rank bases per category and overall

2. **Cross-Domain Pattern Discovery:**
   - Identify patterns visible only through multi-base comparison
   - Example: 2_3_5_smooth Lissajous ratios ↔ 5-smooth FFT sizes ↔ base-60 fractions
   - Document at least 3 cross-domain insights

3. **Trade-off Analysis:**
   - Explicitly document where each base wins/loses
   - No single base optimal for all tasks
   - Recommend context-dependent base selection

**Success Metrics:**
- Base 12 highest composite score (balanced utility)
- Base 60 highest discovery_effectiveness
- Base 10 highest visual_interpretability and computational_efficiency
- At least 3 cross-domain patterns documented

**Implementation:**
```python
from base60lab.metrics import (
    compare_bases, representation_efficiency,
    mathematical_simplicity, computational_efficiency,
    visual_interpretability, discovery_effectiveness,
    composite_score
)

comparison = compare_bases([10, 12, 60], max_denominator=100, max_value=1000)
# Returns dict with all metrics and rankings
```

**Verification:**
```bash
pytest tests/test_core/test_metrics.py -v
```

**Output:** Full metrics report, cross-domain pattern catalog, base selection guidelines

---

## Execution Order and Dependencies

```
01_fraction_analysis.py     → Independent (foundational)
02_geometry_analysis.py     → Independent (foundational)
03_trigonometry_analysis.py → Depends on 02 (angles)
04_modular_patterns.py      → Independent
05_algebra_sequences.py     → Independent
06_harmonic_analysis.py     → Depends on 01, 04 (fractions, modular)
07_lissajous_analysis.py    → Depends on 06 (frequency ratios)
08_fft_benchmarks.py        → Independent (performance)
09_real_world_signals.py    → Depends on 08 (signal processing)
10_combined_experiments.py  → Depends on ALL (synthesis)
```

## Running All Experiments

```bash
# Run all tests
pytest tests/ -v

# Run experiments in order
python experiments/01_fraction_analysis.py
python experiments/02_geometry_analysis.py
python experiments/03_trigonometry_analysis.py
python experiments/04_modular_patterns.py
python experiments/05_algebra_sequences.py
python experiments/06_harmonic_analysis.py
python experiments/07_lissajous_analysis.py
python experiments/08_fft_benchmarks.py
python experiments/09_real_world_signals.py
python experiments/10_combined_experiments.py
```

## Reproducibility Requirements

- Python 3.12+
- Exact package versions in `pyproject.toml`
- Fixed random seeds (42)
- Deterministic algorithms only
- All outputs reproducible bit-for-bit
- Evidence stored in `docs/findings/` and `results/`

---

*Protocols derived from PLAN.md experimental design (sections 3-10) and implemented modules in src/base60lab/*