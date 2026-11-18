# Base-12 / Base-60 Mathematical Research Programme

## Research Plan Overview

This document outlines the experimental research programme investigating whether base-12 and base-60 representations provide practical advantages for understanding, calculating, visualising, and discovering relationships in fractions, geometry, trigonometry, frequency analysis, and digital signal processing.

## Central Research Hypotheses (from PLAN.md lines 27-33)

| ID  | Hypothesis                                                              | What We're Testing                          |
|-----|-------------------------------------------------------------------------|---------------------------------------------|
| H1  | Base 12 simplifies fractional relationships                             | Exact fractions, reciprocals and division   |
| H2  | Base 60 simplifies proportional geometry                                | Angles, rotations and cyclic geometry       |
| H3  | Combined base-12/base-60 representations help reveal periodic relationships | Frequency ratios, harmonics and phase       |
| H4  | Base-12/base-60-friendly sample lengths can be useful in signal processing | FFT factorisation and performance           |
| H5  | Alternative numerical representations improve mathematical exploration   | Pattern discovery and problem-solving       |

These hypotheses do not assume positive answers. We may find that base 60 is superior for one mathematical task, base 12 for another, and decimal remains better for something else — that would still be a valuable result.

## Experimental Programme

### Experiment A: Fractions, Division and Reciprocals
**Reference:** PLAN.md lines 97-133 (Experiments 1-5)

**Question:** Does base 12 or base 60 provide a more useful mathematical language for fractional relationships?

**Methodology:**
1. Generate reciprocals for denominators 1–360
2. Count terminating representations in each base
3. Measure the repeating period of non-terminating representations
4. Compare multiplication and division tables
5. Examine which ratios produce the simplest expressions in each system

**Success Measurement:** Number of terminating fractions, representation length, and complexity of recurring sequences.

**Modules:** `base60lab.fractions`, `base60lab.metrics`

### Experiment B: Geometry, Circles and Trigonometry
**Reference:** PLAN.md lines 134-196 (Experiments B1-B4)

**Question:** Do different angular representations make geometric calculations easier?

**Tests:**
- **B1. Circle subdivisions:** Compare 12, 24, 30, 36, 60, 120, 180, 360 divisions
- **B2. Polygon geometry:** Regular polygons, internal/external angles, symmetry, chord lengths
- **B3. Trigonometric values:** sin(30°), sin(45°), sin(60°) and non-12-part angles
- **B4. Rotation and phase:** Turn-based, dozenal, and sexagesimal representations vs decimal degrees

**Modules:** `base60lab.angles`, `base60lab.geometry`, `base60lab.trigonometry`

### Experiment C: Frequency, Harmonics and Vibration
**Reference:** PLAN.md lines 198-300 (Experiments C1-C4)

**Question:** Do base-12 and base-60 representations help recognise relationships between frequency ratios, phase, and geometric closure?

**Sub-experiments:**
- **C1. Frequency ratios:** 1:1, 2:1, 3:2, 4:3, 5:4, 5:3 relationships
- **C2. Harmonic relationships:** Waveforms with fundamentals and harmonics, phase alignment, beat frequencies
- **C3. Lissajous figures:** x(t)=sin(2πf₁t), y(t)=sin(2πf₂t+δ) — rational frequency ratios and closure
- **C4. Musical tuning:** Twelve-tone equal temperament (2^(1/12)) — distinction from base-12 number system

**Modules:** `base60lab.frequency`, `base60lab.lissajous`, `base60lab.signal_processing`

### Experiment D: Modular Arithmetic and Cyclic Patterns
**Reference:** PLAN.md lines 301-400 (Experiment 4)

**Question:** How do modular arithmetic structures (mod 12, mod 60) relate to base representations?

**Focus:** Distinction between modular arithmetic (equivalence classes) and positional base notation.

**Modules:** `base60lab.modular`

### Experiment E: Number Sequences and Algebra
**Reference:** PLAN.md lines 401-450 (Experiment 5)

**Question:** Do alternative bases reveal patterns in classic number sequences?

**Sequences:** Fibonacci, triangular, square, cube, perfect, prime, geometric, harmonic

**Modules:** `base60lab.sequences`

### Experiment F: Signal Processing and FFT Benchmarks
**Reference:** PLAN.md lines 451-580 (Experiments 8, 10)

**Question:** Do base-12/base-60-friendly sample lengths (5-smooth, 12-smooth, 60-smooth) provide FFT performance advantages?

**Methodology:** Benchmark FFT across categories: powers_of_2, 5_smooth, 12_smooth, 60_smooth, poorly_factored

**Modules:** `base60lab.fft_benchmarks`, `base60lab.signal_processing`

### Experiment G: Real-World Signal Analysis
**Reference:** PLAN.md lines 581-590 (Experiment 9)

**Question:** Do the theoretical advantages translate to practical signal processing?

**Modules:** `base60lab.signal_processing`

### Experiment H: Combined Experiments
**Reference:** PLAN.md lines 591-600 (Experiment 10)

**Question:** Cross-domain synthesis — do advantages compound when multiple domains are considered together?

## Experimental Controls (PLAN.md lines 600-620)

1. **Same mathematical quantity** — A value of 75 must remain 75 regardless of representation
2. **Exact arithmetic** — Use rational numbers and symbolic expressions; avoid floating-point rounding
3. **Independent verification** — Every pattern converted to canonical expression and independently verified
4. **Equal experimental conditions** — Preserve sampling rates, measurement durations, frequency content
5. **Negative results matter** — Record when base 60 performs worse than base 10
6. **Randomised holdout tests** — Prevent selection bias

## Software Architecture (PLAN.md lines 622-694)

```
base12-base60-laboratory/
├── docs/
│   ├── RESEARCH_PLAN.md      (this file)
│   ├── HYPOTHESES.md
│   ├── EXPERIMENT_PROTOCOLS.md
│   └── RESULTS.md
├── src/base60lab/
│   ├── core/                 (Rational, BaseNumber, Expression, Notation, Function, UnknownsRegistry)
│   ├── engines/              (Base10Engine, Base12Engine, Base60Engine)
│   ├── domains/              (fractions, angles, geometry, trigonometry, modular, sequences, frequency, lissajous, signal_processing)
│   ├── fft_benchmarks.py
│   └── metrics.py
├── experiments/
│   ├── 01_fraction_analysis.py
│   ├── 02_geometry_analysis.py
│   ├── 03_trigonometry_analysis.py
│   ├── 04_modular_patterns.py
│   ├── 05_algebra_sequences.py
│   ├── 06_harmonic_analysis.py
│   ├── 07_lissajous_analysis.py
│   ├── 08_fft_benchmarks.py
│   ├── 09_real_world_signals.py
│   └── 10_combined_experiments.py
├── tests/
├── data/
├── results/
├── pyproject.toml
└── README.md
```

## Technology Stack

- **Language:** Python 3.12+
- **Exact Arithmetic:** `fractions.Fraction` via `base60lab.core.rational.Rational`
- **Symbolic Mathematics:** SymPy
- **Numerical Arrays:** NumPy
- **Signal Processing:** SciPy
- **Testing:** pytest
- **Visualization:** Matplotlib

## Deliverables

1. **RESEARCH_PLAN.md** — This document
2. **HYPOTHESES.md** — Formal hypothesis statements with success criteria
3. **EXPERIMENT_PROTOCOLS.md** — Detailed experimental procedures
4. **RESULTS.md** — Documented findings from all 10 experiments

---

*Generated from PLAN.md (lines 630-636 references) and experimental implementation*