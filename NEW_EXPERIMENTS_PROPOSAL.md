# New Experiment Proposals for Base-12/Base-60 Research Programme

## Gap Analysis: What Mathematical Properties Are NOT Yet Tested?

After reviewing all 10 current experiments and PLAN.md experiments A–G, the following significant gaps remain:

| Mathematical Domain | Current Coverage | Gap |
|---|---|---|
| **Continued Fractions** | None | Best rational approximations, convergence rates across bases |
| **Constructible Polygons** | Partial (geometry.py) | Gauss-Wantzel theorem, exact algebraic representations |
| **Diophantine Approximation** | None | Quality of approximants for π, e, φ, √2, √3 in each base |
| **Number-Theoretic Transforms (NTT)** | None | Primitive roots of unity in base-60, modular FFT analog |
| **Coupled Oscillator Networks** | Single Lissajous only | Kuramoto synchronization, phase locking, normal modes |
| **Higher-Dimensional Phase Space** | 2D Lissajous only | 3D+ trajectories, torus topology, quasi-periodic orbits |
| **Rational Trigonometric Tables** | Exact values only | Babylonian-style interpolation, Plimpton 322 reconstruction |
| **Polynomial Modular Arithmetic** | Z/nZ only | (Z/nZ)[x] — cyclic codes, Reed-Solomon, BCH |
| **Combinatorial Designs** | None | Difference sets, finite geometries in base-12/60 |
| **Exact Signal Reconstruction** | Windowed FFT only | Prolate spheroidal wavefunctions, Slepian sequences |

---

## Proposed Experiment 11: Continued Fraction Approximation Across Bases

### Hypothesis
**H1-Extended:** Base-12 and base-60 continued fraction expansions yield simpler (shorter period, smaller coefficients) representations for quadratic irrationals related to geometric and harmonic ratios than base-10.

### Mathematical Basis
- Every irrational has a unique infinite continued fraction: `x = [a₀; a₁, a₂, ...]`
- Quadratic irrationals have eventually periodic continued fractions
- The quality of convergents `pₙ/qₙ` depends on the partial quotients `aₙ`
- Base-60's factors {2,3,5} may produce smaller partial quotients for ratios involving these primes

### Testable Claims
1. **Convergent Quality:** For √2, √3, √5, φ, π, e, the base-60 convergents reach a given accuracy with fewer terms
2. **Period Simplicity:** Quadratic irrationals related to 12/60 (e.g., √3, √12, √60) have shorter periods in base-12/60
3. **Best Approximant Visibility:** The "best rational approximants" are more visually apparent in base-60 notation

### Experimental Design

**Inputs:**
- Target irrationals: √2, √3, √5, √6, √12, √60, φ = (1+√5)/2, π, e
- Max terms: 50
- Bases: 10, 12, 60

**Procedure:**
1. Compute exact continued fraction expansion for each target using exact rational arithmetic
2. Generate convergents `pₙ/qₙ` as `Rational` objects
3. Convert convergents to each base notation
4. Measure: period length, max partial quotient, convergent accuracy vs denominator size
5. Compare base-10 vs base-12 vs base-60 representations

**Exact Computation:**
```python
from base60lab.core.rational import Rational
# Continued fraction using exact rational arithmetic only
def continued_fraction(x: Rational, max_terms: int) -> list[int]:
    terms = []
    for _ in range(max_terms):
        a = int(x)
        terms.append(a)
        x = x - Rational(a)
        if x == 0:
            break
        x = Rational(1) / x
    return terms

def convergents(terms: list[int]) -> list[Rational]:
    # p₋₂=0, p₋₁=1; q₋₂=1, q₋₁=0
    p = [Rational(0), Rational(1)]
    q = [Rational(1), Rational(0)]
    for a in terms:
        p.append(Rational(a) * p[-1] + p[-2])
        q.append(Rational(a) * q[-1] + q[-2])
    return [p[i] / q[i] for i in range(2, len(p))]
```

**Output Formats:**
- JSON: `11_continued_fractions_results.json` — all expansions, convergents, metrics
- CSV: `11_convergent_metrics.csv` — period, max_partial, accuracy_per_term per base/target
- PNG: `11_convergence_comparison.png` — log-log accuracy vs term count per base
- Markdown: `docs/findings/experiment-11-continued-fractions.md`

**Modules Used:**
- `base60lab.core.rational.Rational` — exact arithmetic
- `base60lab.numerals.rational_to_base` — base conversion
- `base60lab.metrics.compute_base_metrics` — representation efficiency

**Controls (from PLAN.md):**
- Control 1: Same `Rational` inputs across all bases
- Control 2: No float operations in metric computation
- Control 3: Independent verification — convergents satisfy `pₙqₙ₋₁ - pₙ₋₁qₙ = (-1)ⁿ⁻¹`
- Control 4: Same max_terms, same target irrationals
- Control 5: Record when base-10 outperforms (e.g., π may have simpler base-10 expansion)

---

## Proposed Experiment 12: Constructible Polygons and Exact Geometric Algebra

### Hypothesis
**H2-Extended:** Base-60 representation naturally expresses the exact algebraic coordinates of constructible regular polygons (Gauss-Wantzel theorem), making their geometric relationships more computationally tractable.

### Mathematical Basis
- A regular n-gon is constructible iff `n = 2ᵏ × p₁ × ... × pₘ` where `pᵢ` are distinct Fermat primes {3, 5, 17, 257, 65537}
- Base-60 = 2² × 3 × 5 contains the first two Fermat primes
- Exact coordinates involve nested square roots: `cos(2π/n)` expressible by radicals
- The chord lengths, areas, and diagonal ratios of constructible polygons are algebraic numbers of degree 2ᵏ

### Testable Claims
1. **Coordinate Simplicity:** Vertices of constructible n-gons (n=3,4,5,6,8,10,12,15,16,17,20,24,30,...) have coordinates with simpler base-60 representations
2. **Radical Nesting Visibility:** The depth of radical nesting for `cos(2π/n)` is apparent in base-60 digit patterns
3. **Diagonal Product Formulas:** Products of diagonal lengths (e.g., for n=17, product = 17) have terminating base-60 representations

### Experimental Design

**Inputs:**
- Constructible n-gons: n ∈ {3,4,5,6,8,10,12,15,16,17,20,24,30,32,34,40,48,51,60,64,68,80,85,96,102,120,136,160,170,204,240,255,256,257,...} up to 360
- Non-constructible: n ∈ {7,9,11,13,14,18,19,21,22,23,25,26,27,28,29,31,33,...}

**Procedure:**
1. For each constructible n, compute exact vertex coordinates using radical expressions (via SymPy)
2. Convert coordinates to base-10, base-12, base-60
3. Measure: representation length, terminating vs repeating, radical nesting depth
4. For non-constructible n, verify no exact radical representation exists
5. Test Gauss-Wantzel products: `∏ diagonal_lengths = n` for prime Fermat n

**Exact Computation:**
```python
from base60lab.core.rational import Rational
from base60lab.geometry import chord_length_squared
# Use SymPy for exact cos(2π/n) for constructible n
# Chord length squared is rational for n=6: chord_length_squared(6) = Rational(1)
# For n=17: nested radicals, but chord_length_squared is algebraic
```

**Output Formats:**
- JSON: `12_constructible_polygons_results.json` — coordinates, base representations, constructibility proof
- CSV: `12_polygon_metrics.csv` — n, constructible(Y/N), coord_length_per_base, radical_depth
- PNG: `12_constructible_visualization.png` — polygons with vertex coordinates labeled in all three bases
- Markdown: `docs/findings/experiment-12-constructible-polygons.md`

**Modules Used:**
- `base60lab.geometry` — chord_length, chord_length_squared, polygon_area, polygon_perimeter
- `base60lab.core.rational.Rational` — exact rational coordinates where available
- `base60lab.numerals.rational_to_base` — base conversion
- `base60lab.trigonometry` — exact trig values for supported angles

**Controls:**
- Control 1: Same radius=1 for all polygons
- Control 2: Exact radical expressions verified via SymPy
- Control 3: Round-trip base → Rational → base identity
- Control 4: Same n-range for constructible and non-constructible
- Control 5: Document non-constructible cases where base-60 offers no advantage

---

## Proposed Experiment 13: Resonance Networks and Coupled Oscillators

### Hypothesis
**H3-Extended:** Base-12 and base-60 phase representations make synchronization manifolds, Arnold tongues, and resonance clusters in coupled oscillator networks more discoverable than base-10 or radian representations.

### Mathematical Basis
- Kuramoto model: `dθᵢ/dt = ωᵢ + (K/N) Σ sin(θⱼ - θᵢ)`
- Phase locking occurs when frequency ratios are rational
- Arnold tongues: regions in (K, Δω) space where phase locking occurs
- Base-60 factors {2,3,5} align with simple rational frequency ratios (2:1, 3:2, 4:3, 5:4, 5:3, 6:5)
- The "resonance web" of an oscillator network has structure visible in factorization of coupling ratios

### Testable Claims
1. **Phase Locking Clarity:** Rational frequency ratios with 2,3,5 factors show clearer phase locking boundaries in base-60
2. **Arnold Tongue Visibility:** Tongue widths (proportional to K) are more simply expressed in base-12/60
3. **Cluster Synchronization:** Oscillator clusters forming at ratios with {2,3,5} factors have simpler base-60 phase patterns

### Experimental Design

**Inputs:**
- N oscillators: 3, 4, 6, 12
- Frequency ratios: simple ratios (3:2, 4:3, 5:4, 5:3, 6:5, 7:5, 8:5) and non-smooth (7:3, 11:7)
- Coupling strength K: 0.1 to 5.0
- Phase representations: radians, degrees, turns, dozenal turns, sexagesimal degrees

**Procedure:**
1. Simulate Kuramoto dynamics with exact rational frequency ratios (using numerical ODE)
2. Track phase differences modulo 1 (turns)
3. Identify phase-locked states (bounded phase differences)
4. Map Arnold tongues in (K, Δω) space
5. Express phase differences and locking thresholds in all five representations
6. Compare visual clarity of synchronization boundaries

**Exact Computation:**
```python
from base60lab.frequency import FrequencyRatio, Phase
from base60lab.core.rational import Rational
# Frequency ratios as exact Rationals
ratio = FrequencyRatio(3, 2)  # exact 3/2
# Phase differences as exact Rationals modulo 1
phase_diff = Phase(Rational(1, 6))  # 1/6 turn = 60° = 10 dozenal = 10 sexagesimal
# Locking condition: |Δω| < K * |sin(phase_diff)|
```

**Output Formats:**
- JSON: `13_resonance_networks_results.json` — Arnold tongue data, phase trajectories, locking thresholds
- CSV: `13_locking_thresholds.csv` — ratio, base, locking_K, phase_at_lock
- PNG: `13_arnold_tongues_comparison.png` — tongue diagrams in each representation
- PNG: `13_phase_trajectories.png` — oscillator phase evolution
- Markdown: `docs/findings/experiment-13-resonance-networks.md`

**Modules Used:**
- `base60lab.frequency.FrequencyRatio`, `Phase` — exact rational frequency/phase
- `base60lab.lissajous` — closure analysis extended to N oscillators
- `base60lab.numerals` — base conversion for phase values
- `base60lab.modular` — phase arithmetic modulo 1
- `base60lab.signal_processing` — spectral analysis of oscillator outputs

**Controls:**
- Control 1: Same ωᵢ, K, initial conditions across all representations
- Control 2: Exact Rational frequency ratios; numerical integration only for dynamics
- Control 3: Independent verification — locking condition derived analytically
- Control 4: Same simulation time, dt, random seed
- Control 5: Record non-smooth ratios where base-10 may be clearer

---

## Proposed Experiment 14: Number-Theoretic Transforms in Base-60

### Hypothesis
**H4-Extended:** Base-60's rich primitive root structure (φ(60)=16 units) enables efficient Number-Theoretic Transforms (NTT) for exact integer convolution, with advantages for modular arithmetic and cryptographic applications.

### Mathematical Basis
- NTT requires a prime modulus `p` with a primitive n-th root of unity
- For base-60 smooth sizes, we can use CRT with multiple primes
- Base-60 = 2² × 3 × 5 → NTT sizes can use factors {2,3,5}
- The 60-smooth numbers align with NTT-friendly factorizations
- NTT provides exact integer convolution (no floating-point error)

### Testable Claims
1. **NTT Size Availability:** More transform sizes are NTT-friendly in base-60 factorization than base-10
2. **Exact Convolution:** NTT with base-60 smooth sizes gives bit-exact convolution vs FFT rounding
3. **Modular Arithmetic Speed:** Base-60's small prime factors allow faster CRT reconstruction

### Experimental Design

**Inputs:**
- Transform sizes: 5-smooth, 12-smooth, 60-smooth up to 8192
- Prime moduli: NTT-friendly primes (e.g., 998244353 = 119×2²³+1, 167772161 = 5×2²⁵+1)
- Test signals: integer sequences, polynomial multiplication

**Procedure:**
1. Implement NTT for sizes with factors {2,3,5} using CRT
2. Compare NTT sizes available vs FFT sizes from Experiment 08
3. Benchmark: NTT (exact integer) vs FFT (floating-point) for convolution
4. Measure: exact integer recovery, speed, memory
5. Test polynomial multiplication exactness

**Exact Computation:**
```python
from base60lab.fft_benchmarks import is_5_smooth, is_12_smooth, is_60_smooth
# NTT requires primitive root of unity
# For size N = 2^a * 3^b * 5^c, find prime p = k*N + 1
# Use CRT with multiple primes for larger dynamic range
```

**Output Formats:**
- JSON: `14_ntt_results.json` — available sizes, primitive roots, benchmark data
- CSV: `14_ntt_vs_fft.csv` — size, NTT_time, FFT_time, exact_recovery(bool)
- PNG: `14_ntt_size_availability.png` — Venn diagram of NTT vs FFT sizes
- Markdown: `docs/findings/experiment-14-ntt-base60.md`

**Modules Used:**
- `base60lab.fft_benchmarks.is_5_smooth`, `is_12_smooth`, `is_60_smooth`
- `base60lab.core.rational.Rational` — exact rational reconstruction
- `base60lab.modular` — modular arithmetic for NTT
- `base60lab.signal_processing` — convolution comparison

**Controls:**
- Control 1: Same transform sizes tested for NTT and FFT
- Control 2: Exact integer convolution verified by direct O(N²) computation
- Control 3: Same random test signals (integer sequences)
- Control 4: Document where FFT outperforms NTT (e.g., non-smooth sizes)
- Control 5: Negative results — sizes where no NTT prime exists

---

## Proposed Experiment 15: Diophantine Approximation and Best Rational Approximants

### Hypothesis
**H1/H5-Extended:** The quality and visibility of best rational approximations to fundamental constants (π, e, φ, √2, √3, √5, γ) are enhanced in base-12 and base-60 due to their factorization structure.

### Mathematical Basis
- Dirichlet's approximation theorem: `|x - p/q| < 1/q²` has infinitely many solutions
- Best approximants are convergents of continued fraction
- The "approximation constant" depends on partial quotients
- Base-60's factors {2,3,5} may yield smaller partial quotients for constants involving these primes
- The approximation `355/113` for π (base-10 famous) — what are the base-60 analogs?

### Testable Claims
1. **Approximant Visibility:** Best approximants to π, e, φ have terminating or short-period representations in base-60
2. **Error Representation:** The approximation error `|x - p/q|` is more simply expressed in base-60
3. **Semi-Convergents:** Intermediate fractions (semi-convergents) reveal patterns in base-12/60

### Experimental Design

**Inputs:**
- Constants: π, e, φ = (1+√5)/2, √2, √3, √5, √6, ln(2), γ (Euler-Mascheroni)
- Denominator bounds: q ≤ 10000
- Bases: 10, 12, 60

**Procedure:**
1. Compute all best rational approximants `p/q` for each constant (using continued fractions)
2. For each approximant, compute exact error `E = |x - p/q|` as high-precision rational
3. Convert `p`, `q`, `p/q`, and `E` to base-10, base-12, base-60
4. Analyze: representation length, terminating/repeating, digit patterns
5. Find "visually simple" approximants in each base

**Exact Computation:**
```python
from base60lab.core.rational import Rational
# High-precision rational approximation of constants
# Use mpmath for high-precision float, then rational approximation
# Or use known rational approximations: 355/113, 22/7 for π
# 193/71 for e, 144/89 for φ (Fibonacci ratios)
```

**Output Formats:**
- JSON: `15_diophantine_results.json` — all best approximants, errors, base representations
- CSV: `15_approximant_metrics.csv` — constant, p, q, error, base10_len, base12_len, base60_len
- PNG: `15_approximation_quality.png` — log error vs log q per base
- PNG: `15_base60_approximants.png` — famous approximants rendered in base-60
- Markdown: `docs/findings/experiment-15-diophantine-approximation.md`

**Modules Used:**
- `base60lab.core.rational.Rational` — exact rational arithmetic
- `base60lab.numerals.rational_to_base` — base conversion
- `base60lab.metrics.representation_efficiency` — representation length metrics
- `base60lab.sequences.fibonacci` — Fibonacci ratios for φ

**Controls:**
- Control 1: Same constants, same denominator bounds across bases
- Control 2: Errors computed with mpmath at 200+ bits precision, then exact rational
- Control 3: Independent verification — approximants satisfy `|x - p/q| < 1/(2q²)`
- Control 4: Same q_max for all constants
- Control 5: Record cases where base-10 approximants are simpler (e.g., 22/7, 355/113)

---

## Implementation Priority & Dependencies

```
11_continued_fractions.py      → Independent (foundational)
12_constructible_polygons.py   → Depends on 02, 03 (geometry, trigonometry)
13_resonance_networks.py       → Depends on 06, 07, 04 (harmonic, lissajous, modular)
14_ntt_base60.py               → Depends on 08, 04 (fft_benchmarks, modular)
15_diophantine_approximation.py → Depends on 01, 11 (fractions, continued_fractions)
```

## Cross-Cutting Themes

These 5 new experiments extend the research in critical directions:

| Experiment | Hypotheses Extended | New Mathematical Territory |
|---|---|---|
| 11 | H1, H5 | Continued fractions, quadratic irrationals |
| 12 | H2, H5 | Algebraic number theory, constructibility |
| 13 | H3, H4 | Nonlinear dynamics, synchronization |
| 14 | H4 | Exact integer computation, NTT |
| 15 | H1, H5 | Diophantine approximation, visibility |

All experiments follow PLAN.md controls:
- Exact rational arithmetic throughout (`base60lab.core.rational.Rational`)
- JSON/CSV/PNG/Markdown output matching existing conventions
- Independent mathematical verification of every claimed pattern
- Explicit negative result documentation
- Deterministic, reproducible with fixed seeds

## Files to Create

```
/home/hyperion/Projects/Base60Research/base12-base60-laboratory/experiments/
├── 11_continued_fractions.py
├── 12_constructible_polygons.py
├── 13_resonance_networks.py
├── 14_ntt_base60.py
└── 15_diophantine_approximation.py
```

Each follows the exact structure of experiments 01–10:
- `run_*_experiment()` returning `dict[str, Any]`
- `save_json_results()`, `save_csv_measurements()`, `create_visualizations()`, `generate_findings_markdown()`
- `main()` entry point with `argparse` for configuration
- Output to `results/` and `docs/findings/`

---

*This proposal identifies 5 concrete, implementable experiments that extend the current 10 by addressing significant mathematical gaps in continued fractions, algebraic geometry, nonlinear dynamics, exact integer transforms, and Diophantine approximation — all using existing `src/base60lab` modules.*