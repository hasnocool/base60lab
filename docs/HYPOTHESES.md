# Base-12 / Base-60 Mathematical Research Hypotheses

## Overview

This document formalizes the five primary research hypotheses from PLAN.md (lines 27-33) with precise success criteria, measurable outcomes, and falsification conditions. Each hypothesis is testable through the experimental programme documented in EXPERIMENT_PROTOCOLS.md and evaluated in RESULTS.md.

---

## Hypothesis H1: Base 12 Simplifies Fractional Relationships

**Statement:** Base-12 (duodecimal) representation provides simpler exact representations for a larger class of common fractions than base-10, specifically those whose denominators have prime factors 2 and 3.

**Mathematical Basis:**
- Base 10 = 2 × 5 → terminates for denominators with factors {2, 5}
- Base 12 = 2² × 3 → terminates for denominators with factors {2, 3}
- Base 60 = 2² × 3 × 5 → terminates for denominators with factors {2, 3, 5}

**Success Criteria (Measurable):**
1. **Termination ratio:** Base 12 must terminate ≥ 20% of unit fractions 1/n for n ∈ [1, 100] (vs 15% for base 10)
2. **Average representation length:** Base 12 average digits per value ≤ base 10 for integers 0–1000
3. **Reciprocal simplicity:** Common fractions (1/2, 1/3, 1/4, 1/6, 1/12) must have single-digit representations in base 12
4. **Multiplication table utility:** Base 12 multiplication table reveals more divisibility patterns than base 10

**Falsification Conditions:**
- Base 12 terminates fewer fractions than base 10 for n ∈ [1, 100]
- Base 12 average representation length exceeds base 10 for common integers
- No practical calculation advantage for mental arithmetic with common fractions

**Related Experiments:** 01_fraction_analysis.py, metrics comparison
**Modules:** `base60lab.fractions`, `base60lab.metrics`
**Findings Reference:** `docs/findings/metrics-comparison-report.md`

---

## Hypothesis H2: Base 60 Simplifies Proportional Geometry

**Statement:** Base-60 (sexagesimal) representation provides natural advantages for angular measurement, circle subdivisions, and geometric proportions due to 360 = 6 × 60 = 30 × 12.

**Mathematical Basis:**
- Full circle = 360° = 6 × 60 = 30 × 12
- Base 60 factors {2, 3, 5} match 360's factors {2², 3², 5}
- Historical Babylonian astronomy/geometry used base-60 for this reason

**Success Criteria (Measurable):**
1. **Circle subdivision termination:** All standard subdivisions (12, 24, 30, 36, 60, 120, 180, 360) yield integer angles terminating in base 60
2. **Polygon angle exactness:** Internal/external angles of regular n-gons for standard n must be representable exactly in base 60
3. **Chord length rationality:** Rational chord lengths (hexagon c₆ = r) must have simple base-60 representations
4. **DMS notation naturalness:** Degrees-minutes-seconds (base-60 subdivision) must map naturally to base-60 positional notation

**Falsification Conditions:**
- Standard circle subdivisions do not terminate in base 60
- Geometric relationships are more obscure in base 60 than base 10/12
- No advantage over radian measure for trigonometric identities

**Related Experiments:** 02_geometry_analysis.py, 03_trigonometry_analysis.py
**Modules:** `base60lab.angles`, `base60lab.geometry`, `base60lab.trigonometry`
**Findings Reference:** `docs/findings/geometry-polygon-subdivisions.md`, `docs/findings/angles-circle-subdivisions.md`, `docs/findings/trigonometry-exact-values.md`

---

## Hypothesis H3: Combined Base-12/Base-60 Representations Help Reveal Periodic Relationships

**Statement:** Using base-12 and base-60 representations together (turns, dozenal fractions, sexagesimal angles) makes frequency ratios, harmonic relationships, phase alignment, and Lissajous closure patterns more discoverable than single-base representations.

**Mathematical Basis:**
- Phase φ = ft (mod 1) — fraction of a complete cycle
- 1 turn = 12 × 30° = 60 × 6° = 2π radians
- Rational frequency ratio a/b → Lissajous closure period = denominator of reduced a/b
- Base-60 factors {2,3,5} align with musical intervals (2:1, 3:2, 4:3, 5:4)

**Success Criteria (Measurable):**
1. **Frequency ratio clarity:** Simple ratios (3:2, 4:3, 5:4, 5:3) have terminating or short-period representations in base 12 and/or base 60
2. **Harmonic series visibility:** Harmonic ratios n:1 map to clear patterns in base-12 turn fractions
3. **Phase arithmetic simplicity:** Phase addition modulo 1 is intuitive in dozenal/sexagesimal
4. **Lissajous closure prediction:** Base-12/base-60 representations predict geometric closure from frequency ratio denominator factorization

**Falsification Conditions:**
- Frequency ratios are equally clear (or clearer) in base 10 alone
- Phase arithmetic offers no advantage over radians
- Lissajous closure patterns not more discoverable in alternative bases

**Related Experiments:** 06_harmonic_analysis.py, 07_lissajous_analysis.py
**Modules:** `base60lab.frequency`, `base60lab.lissajous`, `base60lab.modular`
**Findings Reference:** `docs/findings/frequency-ratios-harmonics.md`, `docs/findings/lissajous-phase-closure.md`

---

## Hypothesis H4: Base-12/Base-60-Friendly Sample Lengths Can Be Useful in Signal Processing

**Statement:** FFT transform sizes that are 5-smooth (2ᵃ3ᵇ5ᶜ), 12-smooth, or 60-smooth provide measurable performance advantages over poorly-factored sizes, making base-12/base-60-friendly sample lengths practically useful.

**Mathematical Basis:**
- FFT efficiency depends on factorization of transform size N
- Cooley-Tukey algorithm decomposes N into small prime factors
- 5-smooth (regular) numbers: {2, 3, 5} — optimal for mixed-radix FFT
- 12-smooth adds {7, 11}; 60-smooth adds all primes ≤ 59

**Success Criteria (Measurable):**
1. **Performance hierarchy:** powers_of_2 ≈ 5_smooth < 12_smooth < 60_smooth < poorly_factored
2. **5-smooth near-optimal:** 5-smooth sizes within 2× performance of powers of 2
3. **No numerical degradation:** Precision and accuracy (ULPs) equivalent across all categories
4. **Practical recommendation:** Padding to 5-smooth sizes beneficial when zero-padding acceptable

**Falsification Conditions:**
- 5-smooth sizes perform significantly worse than powers of 2 (> 5× slowdown)
- Poorly-factored sizes outperform smooth sizes
- Numerical accuracy degrades for smooth sizes

**Related Experiments:** 08_fft_benchmarks.py, 09_real_world_signals.py
**Modules:** `base60lab.fft_benchmarks`, `base60lab.signal_processing`
**Findings Reference:** `docs/findings/fft-benchmarks-performance.md`, `docs/findings/signal-processing-spectral.md`

---

## Hypothesis H5: Alternative Numerical Representations Improve Mathematical Exploration

**Statement:** The ability to switch between base-10, base-12, and base-60 representations of the same mathematical quantities enables pattern discovery and problem-solving that would be missed in a single representation system.

**Mathematical Basis:**
- Representation is a presentation choice; underlying value is invariant
- Different bases highlight different divisibility/factorization patterns
- Cross-base comparison reveals structure invisible in any single base
- Exact rational arithmetic prevents floating-point artifacts

**Success Criteria (Measurable):**
1. **Cross-base pattern detection:** At least 3 mathematical patterns discovered only through multi-base comparison
2. **Factorization visibility metric:** Base 60 scores highest on factorization_visibility (1/2 + 1/3 + 1/5)
3. **Composite utility score:** Base 12 achieves highest balanced score across representation_efficiency, mathematical_simplicity, computational_efficiency, visual_interpretability, discovery_effectiveness
4. **Negative result documentation:** Cases where base 10 outperforms alternatives are explicitly recorded

**Falsification Conditions:**
- No patterns discovered through multi-base comparison beyond what single base reveals
- Composite scores show no clear winner; all bases equivalent
- Cross-base switching adds cognitive overhead without insight

**Related Experiments:** 10_combined_experiments.py, metrics comparison
**Modules:** `base60lab.metrics`, all domains
**Findings Reference:** `docs/findings/metrics-comparison-report.md`

---

## Hypothesis Cross-Reference Matrix

| Experiment | H1 (Fractions) | H2 (Geometry) | H3 (Periodicity) | H4 (FFT/Signal) | H5 (Exploration) |
|------------|----------------|---------------|------------------|-----------------|------------------|
| 01_fraction_analysis.py | ✓ Primary | | | | ✓ Secondary |
| 02_geometry_analysis.py | | ✓ Primary | | | ✓ Secondary |
| 03_trigonometry_analysis.py | | ✓ Primary | ✓ Secondary | | ✓ Secondary |
| 04_modular_patterns.py | | | ✓ Secondary | | ✓ Secondary |
| 05_algebra_sequences.py | | | | | ✓ Primary |
| 06_harmonic_analysis.py | ✓ Secondary | | ✓ Primary | ✓ Secondary | ✓ Secondary |
| 07_lissajous_analysis.py | | | ✓ Primary | | ✓ Secondary |
| 08_fft_benchmarks.py | | | | ✓ Primary | ✓ Secondary |
| 09_real_world_signals.py | | | | ✓ Primary | ✓ Secondary |
| 10_combined_experiments.py | ✓ Secondary | ✓ Secondary | ✓ Secondary | ✓ Secondary | ✓ Primary |

---

## Success/Failure Decision Framework

Each hypothesis will be evaluated as:
- **SUPPORTED** — All primary success criteria met, no falsification conditions triggered
- **PARTIALLY SUPPORTED** — Some success criteria met, trade-offs documented
- **NOT SUPPORTED** — Falsification conditions met or primary criteria not met
- **INCONCLUSIVE** — Insufficient data or conflicting results

Results documented in RESULTS.md with evidence from experimental findings.

---

*Derived from PLAN.md lines 27-33 (hypotheses table) and experimental design in PLAN.md sections 3-10*