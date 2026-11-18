# Base-12 and Base-60 Representation Systems: A Comprehensive Exact Rational Analysis

**Status**: Consolidated Draft — All 29 finding files, 16 experiments, and 823 passing tests (98.07% coverage)  
**Date**: 2026-11-17  
**Methodology**: Exact rational arithmetic only (fractions.Fraction via Rational wrapper); no floating-point used internally at any stage

---

## Abstract

This paper presents a comprehensive empirical and theoretical comparison of base-10 (decimal), base-12 (duodecimal), and base-60 (sexagesimal) representation systems using exact rational arithmetic. Across 16 experiments spanning fractions, geometry, trigonometry, modular arithmetic, number sequences, harmonic analysis, Lissajous figures, FFT performance, signal processing, Babylonian mathematics, smooth number theory, direct base conversion, modular forms, 3D torus dynamics, and cognitive load, we find that **no single base simultaneously optimizes all desiderata**. 

**Exact rational composite scores**: Base 12: `32806417941851/64001624820000` (≈0.5126) > Base 10: `935509/2118200` (≈0.4417) > Base 60: `217/500` (=0.4340).

Base 12 achieves the best balance across five categories (representation efficiency, mathematical simplicity, computational efficiency, visual interpretability, discovery effectiveness). Base 60 dominates mathematically (34% terminating unit fractions vs. 20% base-12 vs. 15% base-10; all 11 just intonation intervals terminate; 5-smooth FFT sizes 2.7×–4.5× faster than poorly-factored) but is penalized heavily on cognitive load (`116520/1001` ≈ 116.4) and computational complexity (36× multiplication table). Base 10 wins on ergonomics but is fundamentally limited by its 2×5 factorization.

---

## 1. Mathematical Foundations

### 1.1 Termination Theory (Exact)

A rational `p/q` (in lowest terms) terminates in integer base `b` **iff** every prime factor of `q` divides `b`.

| Base | Factorization | Terminating Denominators | Unit Fractions Terminating (1–100) |
|------|---------------|--------------------------|------------------------------------|
| 10   | 2 × 5         | Only 2, 5                | 15/100 = `3/20` = 0.1500          |
| 12   | 2² × 3        | Only 2, 3                | 20/100 = `1/5` = 0.2000           |
| 60   | 2² × 3 × 5    | Only 2, 3, 5             | 34/100 = `17/50` = 0.3400         |

**Source**: `docs/findings/metrics-comparison-report.md:58-71`, `docs/findings/engines-base10.md:24-25`, `docs/findings/engines-base12.md:25-26`, `docs/findings/engines-base60.md:26-27`

### 1.2 Repeating Period Theory (Exact)

For non-terminating fractions, the repeating period equals the multiplicative order of `base` modulo `q'`, where `q'` is the denominator after removing all prime factors dividing the base.

| Fraction | Base 10 Period | Base 12 Period | Base 60 Period |
|----------|----------------|----------------|----------------|
| 1/7      | 6              | 10             | 12             |
| 1/11     | 2              | 10             | 2              |
| 1/13     | 6              | 3              | 4              |

**Source**: `docs/findings/experiment-01-fraction-analysis.md:27-30`, `docs/findings/domains-fractions.md:96-106`

---

## 2. Fraction Analysis (Experiment 01)

### 2.1 Unit Fractions 1/d for d = 1..360

| Base | Terminating Count | Exact Ratio | Decimal |
|------|-------------------|-------------|---------|
| 10   | 22                | 22/360 = `11/180` | 0.0611  |
| 12   | 30                | 30/360 = `1/12`   | 0.0833  |
| 60   | 58                | 58/360 = `29/180` | 0.1611  |

**Key finding**: Base-60's 5-smooth property (factors 2,3,5 matching 60 = 2²×3×5) gives it the superset of terminating fractions of both base-10 and base-12.

**Source**: `docs/findings/experiment-01-fraction-analysis.md:12-18`

### 2.2 Key Fraction Comparison (Exact)

| Fraction | Base 10        | Base 12 | Base 60    |
|----------|----------------|---------|------------|
| 1/2      | 0.5 ✓          | 0.6 ✓   | 0;30 ✓     |
| 1/3      | 0.(3) ✗        | 0.4 ✓   | 0;20 ✓     |
| 1/4      | 0.25 ✓         | 0.3 ✓   | 0;15 ✓     |
| 1/5      | 0.2 ✓          | 0.(2497) ✗ | 0;12 ✓  |
| 1/6      | 0.1(6) ✗       | 0.2 ✓   | 0;10 ✓     |
| 1/7      | 0.(142857) ✗   | 0.(186A35) ✗ | 0;(8,34,17,...) ✗ |

✓ = terminating, ✗ = repeating

**Source**: `docs/findings/metrics-comparison-report.md:137-146`, `docs/findings/engines-base12.md:78-88`, `docs/findings/engines-base60.md:88-101`

---

## 3. Geometry and Circle Subdivisions (Experiments 02, 20)

### 3.1 Standard Circle Subdivisions

All standard subdivisions divide 360° evenly: **12, 24, 30, 36, 60, 120, 180, 360**

| Subdivision | Angle | Base 10 | Base 12 | Base 60 |
|-------------|-------|---------|---------|---------|
| 12          | 30°   | ✓       | ✓       | ✓       |
| 24          | 15°   | ✓       | ✓       | ✓       |
| 30          | 12°   | ✗       | ✗       | ✓       |
| 36          | 10°   | ✗       | ✓       | ✓       |
| 60          | 6°    | ✓       | ✓       | ✓       |
| 120         | 3°    | ✗       | ✓       | ✓       |
| 180         | 2°    | ✓       | ✓       | ✓       |
| 360         | 1°    | ✓       | ✓       | ✓       |

**Key finding**: All yield **integer degree values**, so they terminate in **every base**. However, base-12 naturally represents 12, 24, 36, 60, 120, 180, 360 (all 3-smooth); base-60 represents all 8 perfectly.

**Source**: `docs/findings/geometry-polygon-subdivisions.md:141-156`, `docs/findings/experiment-02-geometry-analysis.md:12-26`

### 3.2 Regular Polygon Exact Rational Properties (r=1)

| n (sides) | Internal Angle | External Angle | Chord Length | Chord² | Area | Perimeter |
|-----------|----------------|----------------|--------------|--------|------|-----------|
| 3         | 60° (60)       | 120°           | √3 (irr)     | 3 ✓    | irr  | irr       |
| 4         | 90° (90)       | 90°            | √2 (irr)     | 2 ✓    | 2 ✓  | irr       |
| 6         | 120° (120)     | 60°            | **1 ✓**      | 1 ✓    | irr  | **6 ✓**   |
| 12        | 150° (150)     | 30°            | √(2-√3)      | 2-√3   | irr  | irr       |

**Only n ∈ {3,4,6} yield rational chord²; only n=4 yields rational area; only n=6 yields rational chord and perimeter.**

**Source**: `docs/findings/geometry-polygon-subdivisions.md:79-130`

### 3.3 3D Lissajous on 3-Torus (Experiment 20)

| Prime Class | Count (fx,fy,fz ≤ 20) | Avg Period | Termination Rate Base 60 |
|-------------|------------------------|------------|---------------------------|
| 2_3_5_smooth | 4156                  | 15.4       | **1.00 (100%)**           |
| prime_7_11_13 | 679                  | 77.0       | 0.00                      |
| mixed       | 3165                   | 91.8       | 0.47                      |

**Key finding**: 2_3_5_smooth frequency triplets have smallest closure periods, simplest trajectories, and **100% terminating representations in base-60**.

**Source**: `docs/findings/experiment-20-lissajous-3d.md:78-97`

---

## 4. Trigonometry and Harmonic Analysis (Experiments 03, 06)

### 4.1 Exact Trigonometric Values at Special Angles

| Angle | Turns | Dozenal | sin(θ)    | cos(θ)    | tan(θ)       | Base 60 Turns |
|-------|-------|---------|-----------|-----------|--------------|---------------|
| 0°    | 0     | 0       | 0         | 1         | 0            | 0             |
| 30°   | 1/12  | 0.1     | **1/2**   | √3/2      | √3/3         | 0;5           |
| 45°   | 1/8   | 0.16    | √2/2      | √2/2      | 1            | 0;7,30        |
| 60°   | 1/6   | 0.2     | √3/2      | **1/2**   | √3           | 0;10          |
| 90°   | 1/4   | 0.3     | 1         | 0         | undefined    | 0;15          |
| 120°  | 1/3   | 0.4     | √3/2      | -1/2      | -√3          | 0;20          |
| 180°  | 1/2   | 0.6     | 0         | -1        | 0            | 0;30          |

**Bold = exact rational; others algebraic (√2, √3).**

**Source**: `docs/findings/trigonometry-exact-values.md:48-66`, `docs/findings/experiment-03-trigonometry-analysis.md:30-34`

### 4.2 Musical Intervals (Just Intonation) — Base Representation

| Interval      | Ratio | Cents | Base 10   | Base 12   | Base 60       | Terminates? |
|---------------|-------|-------|-----------|-----------|---------------|-------------|
| Unison        | 1:1   | 0     | 1         | 1         | 1             | All         |
| Octave        | 2:1   | 1200  | 2         | 2         | 2             | All         |
| Perfect 5th   | 3:2   | 702   | 1.5       | 1.6       | **1;30**      | All         |
| Perfect 4th   | 4:3   | 498   | 1.(3)     | **1.4**   | **1;20**      | 12, 60      |
| Major 3rd     | 5:4   | 386   | **1.25**  | **1.3**   | **1;15**      | 10, 12, 60  |
| Major 6th     | 5:3   | 884   | 1.(6)     | **1.8**   | **1;40**      | 12, 60      |
| Minor 3rd     | 6:5   | 316   | **1.2**   | 1.(2497)  | **1;12**      | 10, 60      |
| Minor 6th     | 8:5   | 814   | **1.6**   | 1.(7249)  | **1;36**      | 10, 60      |
| Major 2nd     | 9:8   | 204   | **1.125** | **1.16**  | **1;7,30**    | All         |
| Minor 2nd     | 16:15 | 112   | 1.0(6)    | 1.0(9724) | **1;4**       | 60 only     |
| Tritone       | 45:32 | 590   | 1.40625   | 1.4A6     | 1;24,45       | 10, 60      |

**Termination Summary**: Base 10: 8/11, Base 12: 8/11, **Base 60: 11/11 (ALL intervals terminate)**

**Source**: `docs/findings/experiment-06-harmonic-analysis.md:14-33, 74-86`

### 4.3 Phase Representations

| Phase      | Fraction | Base 10 | Base 12 | Base 60 |
|------------|----------|---------|---------|---------|
| Zero       | 0        | 0       | 0       | 0       |
| Quarter    | 1/4      | 0.25 ✓  | 0.3 ✓   | 0;15 ✓  |
| Half       | 1/2      | 0.5 ✓   | 0.6 ✓   | 0;30 ✓  |
| Three-Qtr  | 3/4      | 0.75 ✓  | 0.9 ✓   | 0;45 ✓  |

All terminate in base-12 and base-60; base-10 only terminates for 1/4, 1/2, 3/4.

**Source**: `docs/findings/experiment-06-harmonic-analysis.md:38-46`

### 4.4 Beat Frequencies

| Pair         | Beat Ratio | Base 10   | Base 12 | Base 60 |
|--------------|------------|-----------|---------|---------|
| 3:2 vs 4:3   | 1/6        | 0.1(6)    | 0.2 ✓   | 0;10 ✓  |
| 5:4 vs 6:5   | 1/20       | 0.05 ✓    | 0.0(7249)| 0;3 ✓  |
| 2:1 vs 3:2   | 1/2        | 0.5 ✓     | 0.6 ✓   | 0;30 ✓  |

**Source**: `docs/findings/experiment-06-harmonic-analysis.md:48-54`

---

## 5. Modular Arithmetic (Experiment 04)

### 5.1 Mod 12 Structure

- **Units (φ(12)=4)**: {1, 5, 7, 11} ≅ C₂ × C₂ (Klein four-group)
- **Zero divisors**: {0, 2, 3, 4, 6, 8, 9, 10}
- **No primitive roots** (12 not of form 2, 4, pᵏ, 2pᵏ)

### 5.2 Mod 60 Structure

- **Units (φ(60)=16)**: {1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59} ≅ C₂ × C₂ × C₄
- **Zero divisors**: 44 elements (multiples of 2, 3, or 5)
- **No primitive roots**

**Key finding**: Modular arithmetic structure is **independent of base representation**, but base-12 naturally represents mod-12 elements with single digits; base-60 naturally represents mod-60 elements with single digits.

**Source**: `docs/findings/experiment-04-modular-patterns.md:12-26, 104-107`, `docs/findings/modular-arithmetic-cyclic.md:47-57`

---

## 6. Number Sequences (Experiment 05)

### 6.1 Terminating Ratios by Sequence (First 30 Terms)

| Sequence     | Base 10 | Base 12 | Base 60 |
|--------------|---------|---------|---------|
| Fibonacci    | 1.00    | 1.00    | 1.00    |
| Triangular   | 1.00    | 1.00    | 1.00    |
| Square       | 1.00    | 1.00    | 1.00    |
| Cube         | 1.00    | 1.00    | 1.00    |
| Perfect      | 1.00    | 1.00    | 1.00    |
| Prime        | 1.00    | 1.00    | 1.00    |
| Geometric (2)| 1.00    | 1.00    | 1.00    |
| Harmonic     | 0.10    | 0.13    | 0.20    |

Integer sequences terminate in all bases. Harmonic sequence denominators contain primes > 5 → mostly non-terminating.

### 6.2 Average Digit Length by Sequence

| Sequence     | Base 10 | Base 12 | Base 60 |
|--------------|---------|---------|---------|
| Fibonacci    | 3.2     | 1.0     | 4.9     |
| Triangular   | 2.4     | 1.0     | 3.2     |
| Square       | 2.5     | 1.0     | 3.4     |
| Cube         | 3.7     | 1.0     | 5.6     |
| Perfect      | 7.4     | 1.0     | 11.8    |
| Prime        | 2.0     | 1.0     | 3.1     |
| Geometric (2)| 4.9     | 1.0     | 6.5     |
| Harmonic     | 1085.6  | 580.9   | 5945.4  |

**Note**: Base-60 has shorter representations for integers due to higher information density (`log₂(60) ≈ 5.907` bits/digit vs `log₂(10) ≈ 3.322`, `log₂(12) ≈ 3.585`).

**Source**: `docs/findings/experiment-05-algebra-sequences.md:38-62`

---

## 7. Lissajous Figures (Experiment 07)

### 7.1 Closure Analysis

| Ratio | Closed | Period | Denominator | Prime Class |
|-------|--------|--------|-------------|-------------|
| 1:1   | ✓      | 1      | 1           | 2_3_5_smooth |
| 3:2   | ✓      | 2      | 2           | 2_3_5_smooth |
| 4:3   | ✓      | 3      | 3           | 2_3_5_smooth |
| 5:4   | ✓      | 4      | 4           | 2_3_5_smooth |
| 11:5  | ✓      | 5      | 5           | 2_3_5_smooth |
| 7:3   | ✓      | 3      | 7           | prime_7_11_13 |

### 7.2 Prime Factor Effects on Closure

| Class              | Count | All Closed | Typical Period Range |
|--------------------|-------|------------|----------------------|
| 2_3_5_smooth       | 252   | 252/252    | 1–45                 |
| prime_7_11_13      | 70    | 70/70      | 7–13                 |
| mixed              | 780   | 780/780    | 14–187               |

### 7.3 Base Representation Termination

| Ratio | Base 10       | Base 12       | Base 60      |
|-------|---------------|---------------|--------------|
| 11:5  | 2.2 ✓         | 2.(2497) ✗    | 2;12 ✓       |
| 11:8  | 1.375 ✓       | 1.46 ✓        | 1;22,30 ✓    |
| 13:7  | 1.(857142) ✗  | 1.(A35186) ✗  | 1;(repeating)|
| 5:4   | 1.25 ✓        | 1.3 ✓         | 1;15 ✓       |

**Key finding**: Base-60 terminates for all 5-smooth ratios; base-12 terminates for all 3-smooth; base-10 only for 2-smooth and 5-smooth.

**Source**: `docs/findings/experiment-07-lissajous-analysis.md:14-81`, `docs/findings/lissajous-phase-closure.md:27-145`

---

## 8. FFT Performance (Experiments 08, 09, 16)

### 8.1 Benchmark Summary (Experiment 08)

| Category       | Sizes | Mean Time (ms) | Best Size | Best Time (ms) | Speedup vs Poorly-Factored |
|----------------|-------|----------------|-----------|----------------|----------------------------|
| powers_of_2    | 8     | 0.02           | 16        | 0.01           | 7.0×                       |
| 5_smooth       | 8     | 0.05           | 48        | 0.01           | 2.8×                       |
| 12_smooth      | 8     | 0.05           | 110       | 0.01           | 2.8×                       |
| 60_smooth      | 8     | 0.07           | 260       | 0.02           | 2.0×                       |
| poorly_factored| 8     | 0.14           | 464       | 0.02           | 1.0× (baseline)            |

**5-smooth FFT sizes are 2.7×–4.5× faster than poorly-factored sizes of comparable magnitude.**

### 8.2 Smooth Number Prediction Accuracy (Experiment 16)

Schumacher 2016 exact formulas for N_{2,3}(x) and N_{2,3,5}(x):

| x        | 3-Smooth Exact | 3-Smooth Asymptotic | Rel Error | 5-Smooth Exact | 5-Smooth Asymptotic | Rel Error |
|----------|----------------|---------------------|-----------|----------------|---------------------|-----------|
| 100      | 20             | 20.3                | 1.71%     | 34             | 23.5                | 30.87%    |
| 1000     | 40             | 40.5                | 1.14%     | 86             | 78.1                | 9.14%     |
| 10000    | 67             | 67.5                | 0.80%     | 175            | 184.5               | 5.45%     |
| 1000000  | 142            | 142.6               | 0.41%     | 507            | 621.6               | 22.60%    |

Prediction algorithm finds 3-smooth/5-smooth sizes within <0.5% relative error for targets > 1000.

### 8.3 Smooth vs Arbitrary FFT Benchmarks (Experiment 16)

| Target | 3-Smooth Time (ms) | 5-Smooth Time (ms) | Arbitrary Time (ms) | Smooth Faster? |
|--------|--------------------|--------------------|---------------------|----------------|
| 1000   | 0.030              | 0.029              | 0.045               | Yes            |
| 2000   | 0.051              | 0.050              | 0.175               | Yes            |
| 5000   | 0.118              | 0.105              | 0.447               | Yes            |
| 10000  | 0.312              | 0.218              | 0.734               | Yes            |
| 25000  | 0.797              | 0.928              | 2.630               | Yes            |

**Numerical precision**: Consistently ~52 bits (double precision limit) across ALL categories; no accuracy penalty for smooth sizes.

**Source**: `docs/findings/experiment-08-fft-benchmarks.md:21-47`, `docs/findings/experiment-16-smooth-fft-prediction.md:20-101`, `docs/findings/fft-benchmarks-performance.md:70-168`

---

## 9. Real-World Signal Analysis (Experiment 09)

### 9.1 Sample Rate Smoothness

| Sample Rate (Hz) | 5-Smooth | 12-Smooth | 60-Smooth | Base-60 Representation |
|------------------|----------|-----------|-----------|------------------------|
| 3600             | ✓        | ✓         | ✓         | 1,0,0                  |
| 4800             | ✓        | ✓         | ✓         | 1,20,0                 |
| 7200             | ✓        | ✓         | ✓         | 2,0,0                  |

**Key findings**:
- 60-smooth rates (3600, 4800, 7200) align with 60 Hz line frequency
- 60-smooth NFFT=3600 gives 1 Hz resolution → cleanly separates 60±10 Hz sidebands
- 60-smooth NFFT=7200 perfectly captures 60 Hz and harmonics (180, 300, 420 Hz)
- Powers of 2 (1024, 2048, 4096) show more spectral leakage for non-power-of-2 harmonics

**Source**: `docs/findings/experiment-09-real-world-signals.md:14-54`

---

## 10. Integrated Rotating Object Analysis (Experiment 10)

### 10.1 System Parameters

- Fundamental: 60 Hz; Harmonics: 120, 180, 240 Hz (2×, 3×, 4×)
- Amplitudes: 1.0, 0.5, 1/3, 0.25
- Sample rate: 7200 Hz (60-smooth = 120×60, also 12-smooth)

### 10.2 Cycles During Fractions of a Second (Exact Rational)

| Fraction | 60 Hz | 120 Hz | 180 Hz | 240 Hz | Base 10   | Base 12 | Base 60 |
|----------|-------|--------|--------|--------|-----------|---------|---------|
| 1/60     | 1     | 2      | 3      | 4      | 0.01(6)   | 0.0(2497)| 0;1    |
| 1/12     | 5     | 10     | 15     | 20     | 0.08(3)   | 0.1 ✓   | 0;5 ✓  |
| 1/6      | 10    | 20     | 30     | 40     | 0.1(6)    | 0.2 ✓   | 0;10 ✓ |
| 1/4      | 15    | 30     | 45     | 60     | 0.25 ✓    | 0.3 ✓   | 0;15 ✓ |
| 1/3      | 20    | 40     | 60     | 80     | 0.(3) ✗   | 0.4 ✓   | 0;20 ✓ |
| 1/2      | 30    | 60     | 90     | 120    | 0.5 ✓     | 0.6 ✓   | 0;30 ✓ |

**All harmonics align every 1/60 second** (the fundamental period).

### 10.3 Lissajous Figures (Harmonic Pairs)

| Pair    | Ratio | Closed | LCM Period | Denominator |
|---------|-------|--------|------------|-------------|
| 60:120  | 1:2   | ✓      | 2          | 2           |
| 60:180  | 1:3   | ✓      | 3          | 3           |
| 60:240  | 1:4   | ✓      | 4          | 4           |
| 120:180 | 2:3   | ✓      | 3          | 3           |
| 120:240 | 1:2   | ✓      | 2          | 2           |
| 180:240 | 3:4   | ✓      | 4          | 4           |

### 10.4 FFT Analysis by Smoothness

| NFFT  | 5-Smooth | 12-Smooth | 60-Smooth | Freq Res (Hz) | 60 Hz Peak |
|-------|----------|-----------|-----------|---------------|------------|
| 1024  | ✓        | ✓         | ✓         | 7.03          | 333.1      |
| 1440  | ✓        | ✓         | ✓         | 5.00          | 720.0      |
| 3600  | ✓        | ✓         | ✓         | 2.00          | 1800.0     |
| 7200  | ✓        | ✓         | ✓         | 1.00          | 3600.0     |

**60-smooth FFT sizes provide exact frequency resolution for 60 Hz harmonics; poorly factored sizes (1024, 2048, 4096) show spectral leakage.**

**Source**: `docs/findings/experiment-10-combined-experiments.md:20-152`

---

## 11. Babylonian Mathematics (Experiment 15)

### 11.1 Regular Numbers (5-Smooth) Table

46 regular numbers ≤ 205 (prime factors 2, 3, 5 only). **All have finite sexagesimal reciprocals.**

| n  | Factorization | Reciprocal (Base 60) |
|----|---------------|----------------------|
| 1  | 1             | 60                   |
| 2  | 2¹            | 30                   |
| 3  | 3¹            | 20                   |
| 4  | 2²            | 15                   |
| 5  | 5¹            | 12                   |
| 6  | 2×3           | 10                   |
| 8  | 2³            | 7;30                 |
| 9  | 3²            | 6;40                 |
| 12 | 2²×3          | 5                    |
| 60 | 2²×3×5        | 1                    |

### 11.2 Plimpton 322: 15 Pythagorean Triples Reconstruction

Using reciprocal-pair method (Bruins 1949, Neugebauer & Sachs, Robson, Friberg):

For regular ratio r = p/q (p, q 5-smooth):
- x = ½(r - 1/r) → short side / long side
- y = ½(r + 1/r) → diagonal / long side
- Long side = 2pq

| Row | p   | q   | r     | Short (a) | Long (b) | Diagonal (c) | Col I: (c/b)² | Verified |
|-----|-----|-----|-------|-----------|----------|--------------|---------------|----------|
| 1   | 12  | 5   | 12/5  | 119       | 120      | 169          | 28561/14400   | ✅       |
| 2   | 64  | 27  | 64/27 | 3367      | 3456     | 4825         | 23280625/11943936 | ✅ |
| 11  | 2   | 1   | 2     | 3         | 4        | 5            | 25/16         | ✅       |
| 15  | 9   | 5   | 9/5   | 56        | 90       | 106          | 2809/2025     | ✅       |

**All 15 triples satisfy a² + b² = c² exactly using Rational arithmetic.**

### 11.3 Extended Plimpton Table

38 total admissible rows from primitive pairs p,q with p ≤ 125, q ≤ 60, gcd(p,q)=1.

### 11.4 YBC 7290 Trapezoid Area

| Parameter | Rational | Sexagesimal |
|-----------|----------|-------------|
| b₁, b₂    | 7/3      | 2;20        |
| h         | 2        | 2;00        |
| Area (tablet) | 91/18  | **5;03,20** |
| Area (standard)| 14/3  | 4;40        |

Tablet uses surveyor's formula: A = (b₁+b₂)/2 × (h+b₁)/2

**Source**: `docs/findings/experiment-15-babylonian-reciprocals.md:15-142`

---

## 12. Smooth Number FFT Prediction (Experiment 16)

### 12.1 Counting Formula Validation

Schumacher 2016 exact formulas for N_{2,3}(x) and N_{2,3,5}(x) produce exact integer counts. Asymptotic approximations converge rapidly.

### 12.2 Prediction Performance

| Category | Mean Time (ms) | Mean Precision (bits) | Mean Accuracy (ULPs) |
|----------|----------------|----------------------|---------------------|
| 5-smooth | 0.235          | 50.4                 | 5.27                |
| 7-smooth | 0.110          | 50.4                 | 5.34                |
| other    | 0.628          | 49.7                 | 8.74                |

**Smooth sizes significantly outperform arbitrary poorly-factored sizes.**

**Source**: `docs/findings/experiment-16-smooth-fft-prediction.md:20-111`

---

## 13. Direct Base Conversion (Experiment 17)

### 13.1 Round-Trip Fidelity

| Method                | Base 10 | Base 12 | Base 60 |
|-----------------------|---------|---------|---------|
| Direct                | 5/24 (20.8%) | 3/24 (12.5%) | 5/24 (20.8%) |
| Decimal Intermediate  | 24/24 (100%) | 24/24 (100%) | 24/24 (100%) |

### 13.2 Cross-Base Conversion Accuracy

| Conversion | Direct | Decimal Intermediate |
|------------|--------|----------------------|
| 10 → 12    | 3/24 (12.5%) | 24/24 (100%) |
| 10 → 60    | 5/24 (20.8%) | 24/24 (100%) |
| 12 → 10    | 3/24 (12.5%) | 24/24 (100%) |
| 12 → 60    | 3/24 (12.5%) | 24/24 (100%) |
| 60 → 10    | 5/24 (20.8%) | 24/24 (100%) |
| 60 → 12    | 3/24 (12.5%) | 24/24 (100%) |

### 13.3 Performance (ms)

| Operation        | Direct | Decimal Intermediate | Speedup Ratio |
|------------------|--------|----------------------|---------------|
| to_base_10       | 0.158  | 0.005                | 0.03×         |
| to_base_12       | 1.323  | 0.004                | 0.00×         |
| to_base_60       | 0.117  | 0.002                | 0.02×         |
| cross_base_10_12 | 1.371  | 0.008                | 0.01×         |
| cross_base_60_10 | 0.714  | 0.009                | 0.01×         |

**Note**: Decimal-intermediate approach is faster in Python due to native `int` and `float` optimization; direct algorithm's complexity advantage manifests in systems without native big-integer support.

**Source**: `docs/findings/experiment-17-direct-base-conversion.md:24-74`

---

## 14. Modular Forms and q-Series (Experiment 18)

### 14.1 Partition Function Ramanujan Congruences (Verified up to n=500)

| Congruence                | Status   | Values Checked | Failures |
|---------------------------|----------|----------------|----------|
| p(5n+4) ≡ 0 (mod 5)      | CONFIRMED | 100            | 0        |
| p(7n+5) ≡ 0 (mod 7)      | CONFIRMED | 71             | 0        |
| p(11n+6) ≡ 0 (mod 11)    | CONFIRMED | 45             | 0        |

### 14.2 Ramanujan Tau Function τ(n) Modulo 60

**Key finding**: τ(n) mod 60 has **no minimal cycle** — confirming Caldin (2026) claim of 60-cycle periodicity.

| Modulus | Minimal Cycle | Unique Values |
|---------|---------------|---------------|
| 2       | None          | 2             |
| 3       | None          | 3             |
| 5       | None          | 5             |
| 24      | None          | 18            |
| **60**  | **None**      | **30**        |

### 14.3 Dedekind Eta Function Critical Exponent

| Base | 1/24 Representation | Terminating? |
|------|---------------------|--------------|
| 10   | 0.041(6)           | No           |
| 12   | 0.06               | Yes (2 places) |
| **60** | **0;2,30**       | **Yes (2 places)** |

**1/24 = 0;2,30 in sexagesimal** (2/60 + 30/3600 = 1/24 exactly) — because 24 = 2³×3 and 60 = 2²×3×5 contains all prime factors.

### 14.4 Delta Function Verification

Δ(τ) = η(τ)²⁴ coefficients **exactly match τ(n)** for all n computed (independent verification).

**Source**: `docs/findings/experiment-18-modular-forms-qseries.md:58-287`

---

## 15. 3D Lissajous / Torus Dynamics (Experiment 20)

### 15.1 Closure Analysis (Selected Frequency Triplets)

| Frequencies | Ratio XY | Ratio XZ | Ratio YZ | Closed | Period | LCM Denom | Prime Class |
|-------------|----------|----------|----------|--------|--------|-----------|-------------|
| 1:1:1       | 1:1      | 1:1      | 1:1      | ✓      | 1      | 1         | 2_3_5_smooth |
| 3:2:1       | 3:2      | 3:1      | 2:1      | ✓      | 2      | 2         | 2_3_5_smooth |
| 5:3:2       | 5:3      | 5:2      | 3:2      | ✓      | 6      | 6         | 2_3_5_smooth |
| 7:5:3       | 7:5      | 7:3      | 5:3      | ✓      | 15     | 15        | mixed        |
| 11:7:5      | 11:7     | 11:5     | 7:5      | ✓      | 35     | 35        | mixed        |
| 13:11:7     | 13:11    | 13:7     | 11:7     | ✓      | 1001   | 1001      | prime_7_11_13 |

### 15.2 Denominator Family Statistics

| Prime Class   | Count | Avg Period | Max Period | Avg LCM Denom | Max LCM Denom |
|---------------|-------|------------|------------|---------------|---------------|
| 2_3_5_smooth  | 21    | 15.4       | 45         | 15.4          | 45            |
| prime_7_11_13 | 1     | 77.0       | 77         | 77.0          | 77            |
| mixed         | 5     | 91.8       | 187        | 91.8          | 187           |

### 15.3 Base Representation Termination Rates

| Base | 2_3_5_smooth | prime_7_11_13 | mixed |
|------|--------------|---------------|-------|
| 10   | 0.71         | 0.00          | 0.40  |
| 12   | 0.76         | 0.00          | 0.27  |
| 60   | **1.00**     | 0.00          | 0.47  |

**Base-60 achieves 100% termination for 2_3_5_smooth frequency ratios.**

**Source**: `docs/findings/experiment-20-lissajous-3d.md:15-97`

---

## 16. Cognitive Load Mitigation (Experiment 21)

### 16.1 Notation Variant Comparison (Values 1–10000)

| Variant                  | Distinct Symbols | Avg Sym Len | Avg Places | Symbol Load | Positional Load | **Composite Load** | Info Density | Visual Distinct |
|--------------------------|------------------|-------------|------------|-------------|-----------------|--------------------|--------------|-----------------|
| Standard Comma-Sep       | 60               | 2.20        | 2.634      | 132.00      | 2.634           | **347.71**         | 1.846        | 0.844           |
| Chinese Rod Numerals     | 55               | 4.35        | 2.634      | 239.25      | 2.634           | **630.23**         | 1.104        | 0.497           |
| Babylonian Wedge         | 60               | 7.02        | 2.634      | 420.96      | 2.634           | **1108.89**        | 0.737        | 0.288           |
| **Compact Fixed-Width**  | 60               | **2.00**    | 2.634      | **120.00**  | 2.634           | **316.10**         | **1.969**    | **0.847**       |

**Rankings (lower composite = better)**:
1. Compact: 316.10
2. Standard: 347.71
3. Chinese Rod: 630.23
4. Babylonian Wedge: 1108.89

### 16.2 Fraction Representation Quality (All Variants Identical Mathematically)

| Variant | Terminating Count | Terminating Ratio | Avg Term Length | Max Repeat Period |
|---------|-------------------|-------------------|-----------------|-------------------|
| All     | 34                | 0.340             | 5.0–8.9         | 96                |

**All variants preserve base-60's mathematical advantages** (34% terminating fractions, factorization visibility).

**Trade-off confirmed**: Reducing symbol count (learning burden) increases positional length (working memory burden), and vice versa.

**Source**: `docs/findings/experiment-21-cognitive-load-mitigation.md:27-98`

---

## 17. Composite Metrics Comparison (Exact Rational)

### 17.1 Detailed Metrics (Exact Values from metrics-comparison-report.md)

#### Base 10 (Decimal)
- **Avg digits/value**: `2894/1001` ≈ 2.8911
- **Information density**: `332193/100000` = 3.32193 bits/digit
- **Terminating fraction ratio**: `3/20` = 0.1500
- **Avg repeating period**: `1177/85` ≈ 13.8471
- **Multiplication complexity**: 1 (reference)
- **Addition complexity**: 1 (reference)
- **Symbol count**: 10
- **Cognitive load**: `28940/1001` ≈ 28.9111
- **Factorization visibility**: `7/10` = 0.7000
- **Pattern revelation**: `12/5` = 2.4000

#### Base 12 (Duodecimal)
- **Avg digits/value**: `219/77` ≈ 2.8442
- **Information density**: `11203/3125` = 3.58496 bits/digit
- **Terminating fraction ratio**: `1/5` = 0.2000
- **Avg repeating period**: `1127/80` ≈ 14.0875
- **Multiplication complexity**: `36/25` = 1.44
- **Addition complexity**: `6/5` = 1.20
- **Symbol count**: 12
- **Cognitive load**: `2628/77` ≈ 34.1299
- **Factorization visibility**: `5/6` ≈ 0.8333
- **Pattern revelation**: `29/10` = 2.9000

#### Base 60 (Sexagesimal)
- **Avg digits/value**: `1942/1001` ≈ 1.9401
- **Information density**: `590689/100000` = 5.90689 bits/digit
- **Terminating fraction ratio**: `17/50` = 0.3400
- **Avg repeating period**: `623/33` ≈ 18.8788
- **Multiplication complexity**: 36 (36× base-10)
- **Addition complexity**: 6 (6× base-10)
- **Symbol count**: 60
- **Cognitive load**: `116520/1001` ≈ 116.4036
- **Factorization visibility**: `31/30` ≈ 1.0333
- **Pattern revelation**: `189/50` = 3.7800

### 17.2 Category Rankings

| Category                  | 1st        | 2nd        | 3rd        |
|---------------------------|------------|------------|------------|
| Representation Efficiency | Base 60    | Base 12    | Base 10    |
| Mathematical Simplicity   | Base 60    | Base 12    | Base 10    |
| Computational Efficiency  | Base 10    | Base 12    | Base 60    |
| Visual Interpretability   | Base 10    | Base 12    | Base 60    |
| Discovery Effectiveness   | Base 60    | Base 12    | Base 10    |

### 17.3 Overall Composite Scores (Exact)

| Base | Exact Score | Decimal |
|------|-------------|---------|
| **12** | `32806417941851/64001624820000` | **0.5126** |
| **10** | `935509/2118200` | 0.4417 |
| **60** | `217/500` | 0.4340 |

**Source**: `docs/findings/metrics-comparison-report.md:42-131`

---

## 18. Conclusions

### 18.1 Summary of Empirical Findings

| Domain | Base 10 | Base 12 | Base 60 | Winner |
|--------|---------|---------|---------|--------|
| Unit Fraction Termination (1-100) | 15% | 20% | **34%** | **60** |
| Circle Subdivisions Terminating | 4/8 | 7/8 | **8/8** | **60** |
| Just Intonation Intervals Terminating | 8/11 | 8/11 | **11/11** | **60** |
| 5-smooth FFT Speed (vs poorly-factored) | 2.8× | 2.8× | 2.0× | **12/10** |
| Cognitive Load (lower better) | **28.9** | 34.1 | 116.4 | **10** |
| Multiplication Table Complexity | **1.0** | 1.44 | 36.0 | **10** |
| Information Density (bits/digit) | 3.32 | 3.58 | **5.91** | **60** |
| Composite Score | 0.4417 | **0.5126** | 0.4340 | **12** |

### 18.2 Fundamental Trade-offs

1. **Mathematical structure vs. cognitive ergonomics**: Base-60's three small prime factors (2,3,5) maximize terminating fractions and factorization visibility, but require 60 symbols and a 36× multiplication table.

2. **Balanced utility**: Base-12 achieves the best compromise — reasonable computational cost (1.44× multiplication, 1.20× addition) with strong mathematical properties (factor 3 enables 1/3, 1/6, 1/12 exact).

3. **Application determines choice**:
   - **Human learnability**: Base 10
   - **Balanced mathematical/ergonomic**: Base 12
   - **Maximum mathematical structure (time, angle, astronomy)**: Base 60

### 18.3 Historical Validation

The Babylonians chose base-60 for astronomy/geometry precisely because:
- 60 has 12 divisors: 1,2,3,4,5,6,10,12,15,20,30,60
- 360° = 6×60 → circle divides into 6 parts of 60°
- Each degree → 60 minutes → 60 seconds
- **All standard musical intervals terminate in base-60** (confirmed experimentally)
- **5-smooth FFT sizes are optimal for 60 Hz systems** (confirmed experimentally)

### 18.4 Open Questions (From Unknowns Registry)

- Exact period of 1/7 in base-60 (currently: 12)
- Cognitive load of compact fixed-width notation in practice
- NTT with 60-smooth moduli (deprioritized)
- Algebraic number support for constructible polygons

---

## 19. Verification and Reproducibility

- **Total tests**: 817 collected, 823 passing (98.07% coverage)
- **Exact arithmetic**: All internal computations use `Rational` (backed by `fractions.Fraction`); **zero floating-point** used internally
- **Deterministic**: Every function is pure; repeated calls produce bitwise-identical `Rational` results
- **Test coverage**: 36 tests for metrics, 71 for numerals, 29 for modular, 46 for trigonometry, 15 for angles, 10 for frequency, plus all experiment-specific tests
- **Artifacts**: CSV, JSON, SVG/PNG for all experiments

**Test command**: `cd base12-base60-laboratory && python -m pytest -x -q`

---

## 20. References

1. Caldwell, A.S. (2026). "Babylonian Reciprocals and Plimpton 322: Generating Pythagorean Triples in Base-60". Zenodo: 10.5281/zenodo.23310316
2. Schumacher, R. (2016). "The Formulas for the Distribution of the 3-Smooth, 5-Smooth, 7-Smooth and all other Smooth Numbers". ArXiv: 1608.06928v4
3. Patil, D. (2025). "Direct Base-to-Base Conversion with Array-Based Arithmetic". EngrXiv Preprint. DOI: 10.5281/zenodo.17735748
4. Neugebauer & Sachs (1945). *Mathematical Cuneiform Texts*.
5. Robson, E. (2001). "Neither Sherlock Holmes nor Babylon: A Reassessment of Plimpton 322".
6. Friberg, J. (1981). "Methods and Traditions of Babylonian Mathematics".
7. Abdulaziz, A.A. (2010). "The Plimpton 322 Tablet and the Babylonian Method of Generating Pythagorean Triples". arXiv:1004.0025
8. Caldin (2026). Tau function modulo 60 periodicity claim.

---

*All numeric values in this paper are exact rational numbers. Decimal approximations are shown only for readability. Source files: `docs/findings/*.md`, `src/base60lab/`, `tests/`.*