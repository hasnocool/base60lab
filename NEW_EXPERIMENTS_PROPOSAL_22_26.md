# New Experiment Proposals (22-26)

Based on comprehensive review of:
- Existing experiments 01-10, 15-18, 20-21
- PLAN.md experiments A-G
- EXPERIMENT_DESIGN_SUMMARY.md leads and claims
- src/base60lab module capabilities

---

## Experiment 22: Number-Theoretic Transform (NTT) with 60-Smooth Moduli

### Hypothesis
Base-60 factorization (2² × 3 × 5) provides more available NTT-friendly prime moduli than base-10 (2 × 5) or base-12 (2² × 3) because the additional factor 3 enables more Fermat-prime-related moduli of the form k·2ⁿ+1 where k is 5-smooth.

### Mathematical Foundation
- NTT requires primes p where p-1 is smooth (has only small prime factors)
- For transform length N = 2ᵃ3ᵇ5ᶜ, we need primitive N-th roots of unity modulo p
- This requires p ≡ 1 (mod N), i.e., p = k·N + 1 for some integer k
- More smooth factors in N → more flexibility in choosing p with smooth p-1

### Existing Module Usage
- `base60lab.fft_benchmarks`: `is_smooth`, `is_5_smooth`, `is_12_smooth`, `is_60_smooth`
- `base60lab.core.rational`: `Rational` for exact arithmetic
- `base60lab.numerals`: base conversion for displaying moduli
- `base60lab.metrics`: `compute_base_metrics`, `compare_bases` for comparing moduli properties

### Inputs
- Target transform lengths: powers of 2, 3-smooth (12-smooth), 5-smooth (60-smooth)
- Search range for k: 1 ≤ k ≤ 1000
- Prime search up to 2³¹-1 (Mersenne primes) or practical limits

### Exact Computation
- All modular arithmetic using exact integer operations (no floats)
- Primitive root verification: g^((p-1)/q) ≠ 1 (mod p) for all prime factors q of p-1
- NTT convolution via exact integer arithmetic (CRT reconstruction if needed)

### Outputs
- JSON: `22_ntt_smooth_moduli_results.json`
  - Available moduli per smoothness category
  - Moduli properties (bit-length, smoothness of p-1, primitive roots)
  - Comparison table: base-10 vs base-12 vs base-60 factorization
- CSV: `22_ntt_moduli.csv`, `22_transform_lengths.csv`
- PNG: `22_moduli_distribution.png`, `22_smooth_factor_comparison.png`, `22_ntt_performance.png`
- Markdown: `experiment-22-ntt-smooth-moduli.md`

### Controls (from PLAN.md)
- Same quantity: test equal number of transform lengths per category
- Exact arithmetic: all modular operations use Python integers
- Independent verification: cross-check with known NTT primes from literature (Crandall & Pomerance)
- Equal conditions: same k-search range for all categories
- Negative results: record categories with fewer available moduli

### Success Criteria
- Quantify number of available NTT primes per smoothness class
- Demonstrate base-60 factorization (including 3) yields strictly more options than base-10
- Identify practical transform sizes for cryptographic applications

---

## Experiment 23: Continued Fraction Convergents and Diophantine Approximation in Base-60

### Hypothesis
While continued fraction *period lengths* are base-invariant (claim 8 counter-evidence), the *digit patterns* of convergents and the *visibility* of near-integer relationships are enhanced in base-60 for constants with 2,3,5-factor-related algebraic structure.

### Mathematical Foundation
- Continued fractions: x = [a₀; a₁, a₂, ...] with convergents pₙ/qₙ
- Period length of quadratic irrationals is base-invariant (Lagrange)
- But digit representation of convergents pₙ, qₙ depends on base
- Best rational approximants to π: 3/1, 22/7, 333/106, 355/113, 103993/33102, ...
- Base-60 may reveal structure in numerators/denominators with 2,3,5 factors

### Existing Module Usage
- `base60lab.core.rational`: `Rational` for exact convergent computation
- `base60lab.numerals`: `rational_to_base`, `int_to_base` for digit analysis
- `base60lab.metrics`: `analyze_fraction_in_bases`, `compute_base_metrics`
- `base60lab.sequences`: generate sequences of convergents
- `base60lab.modular`: modular arithmetic for period detection

### Inputs
- Constants: π, e, √2, √3, √5, √6, √10, √12, √15, √30, φ, ln(2), ζ(3)
- Maximum convergent index: n ≤ 50
- Base-60 digit analysis of pₙ, qₙ

### Exact Computation
- Continued fraction expansion using exact rational arithmetic
- Convergents computed via recurrence: pₙ = aₙpₙ₋₁ + pₙ₋₂, qₙ = aₙqₙ₋₁ + qₙ₋₂
- All operations in `Rational` (no floating point)
- Base-60 representation of pₙ, qₙ using exact conversion

### Outputs
- JSON: `23_continued_fractions_results.json`
  - Convergents for each constant in all three bases
  - Digit pattern analysis (terminating vs repeating, digit frequencies)
  - Approximation quality (|x - pₙ/qₙ|) in exact rational form
- CSV: `23_convergents_pi.csv`, `23_convergents_sqrt.csv`, `23_digit_patterns.csv`
- PNG: `23_convergent_approximation.png`, `23_base60_digit_patterns.png`, `23_approximation_quality.png`
- Markdown: `experiment-23-continued-fractions-diophantine.md`

### Controls
- Same quantity: equal number of convergents per constant
- Exact arithmetic: all rational operations exact
- Independent verification: compare convergents with known values (OEIS)
- Equal conditions: same max_n for all constants
- Negative results: report constants where base-60 offers no advantage

### Success Criteria
- Document digit pattern differences across bases for same convergents
- Identify constants where base-60 representation reveals algebraic structure
- Test claim 10: best approximants to π in base-60

---

## Experiment 24: Kuramoto Oscillator Networks with Smooth Frequency Ratios

### Hypothesis
Phase-locking boundaries in Kuramoto oscillator networks with {2,3,5}-smooth frequency ratios are more clearly delineated in base-60 phase representation because the natural synchronization manifolds align with base-60's factor structure.

### Mathematical Foundation
- Kuramoto model: dθᵢ/dt = ωᵢ + (K/N) Σⱼ sin(θⱼ - θᵢ)
- Synchronization occurs when frequency differences are within coupling strength
- Phase-locked state: θᵢ(t) = Ωt + ψᵢ where Ω = mean frequency
- Phase differences ψᵢ - ψⱼ satisfy sin(ψᵢ - ψⱼ) = (ωᵢ - ωⱼ)/K
- For rational frequency ratios ωᵢ/ωⱼ = p/q, phase space has toroidal structure

### Existing Module Usage
- `base60lab.frequency`: `FrequencyRatio`, `Phase`, `Harmonic` classes
- `base60lab.lissajous`: `LissajousParameters`, `closure_info` for phase analysis
- `base60lab.core.rational`: exact rational arithmetic for frequency ratios
- `base60lab.angles`: `turn_to_degrees`, `normalize_turns` for phase representation
- `base60lab.numerals`: base-60 phase representation
- `base60lab.metrics`: compare base representations of phase differences

### Inputs
- N oscillators (N = 3, 5, 8)
- Frequency ratios from 5-smooth set: {1:1, 2:1, 3:2, 4:3, 5:4, 5:3, 8:5, 9:8, ...}
- Coupling strength K sweep
- Initial phase conditions: random, clustered, uniform

### Exact Computation
- Frequency ratios as exact `Rational` (no floating point)
- Phase differences as exact `Phase` objects (fractions of turn)
- Synchronization condition: |ωᵢ - ωⱼ| ≤ K computed exactly
- Phase-locked manifold equations solved symbolically where possible
- Base-60 representation of phase coordinates for visualization

### Outputs
- JSON: `24_kuramoto_sync_results.json`
  - Phase-locking regions per frequency ratio set
  - Base-60 phase coordinate representations
  - Order parameter r(t) evolution
- CSV: `24_sync_regions.csv`, `24_phase_differences.csv`, `24_order_parameter.csv`
- PNG: `24_sync_diagram_base60.png`, `24_sync_diagram_base10.png`, `24_basin_boundaries.png`, `24_phase_space_trajectories.png`
- Markdown: `experiment-24-kuramoto-smooth-ratios.md`

### Controls
- Same quantity: equal number of initial conditions per experiment
- Exact arithmetic: frequency ratios and phases as `Rational`
- Independent verification: compare with numerical ODE integration (floats)
- Equal conditions: same K, N, frequency sets across representations
- Negative results: report frequency ratios where base-60 adds no clarity

### Success Criteria
- Visualize synchronization boundaries in base-60 vs base-10 phase coordinates
- Quantify "clarity" of boundaries (separation in phase space)
- Test if {2,3,5}-smooth ratios produce more regular boundaries in base-60

---

## Experiment 25: Constructible Polygon Coordinates and Gauss-Wantzel Theorem in Base-60

### Hypothesis
Coordinates of constructible polygons (Gauss-Wantzel theorem: n = 2ᵏ × product of distinct Fermat primes) have algebraic expressions involving nested square roots; while not rational (claim 9 correction), their *base-60 digit expansions* reveal the underlying 2,3,5-factor structure more clearly than base-10.

### Mathematical Foundation
- Constructible n-gons: n = 2ᵏ · p₁ · p₂ · ... where pᵢ are distinct Fermat primes (3, 5, 17, 257, 65537)
- Vertex coordinates: cos(2π/n), sin(2π/n) expressible via nested square roots
- Gauss's construction of 17-gon: cos(2π/17) = 1/16[-1 + √17 + √(34-2√17) + 2√(17+3√17-√(34-2√17)-2√(34+2√17))]
- Base-60 representation of these algebraic numbers may show periodic/pattern structure

### Existing Module Usage
- `base60lab.core.rational`: `Rational` for exact rational components
- `base60lab.numerals`: `rational_to_base` for algebraic number digit expansion
- `base60lab.trigonometry`: `cos_degrees`, `sin_degrees` for exact values
- `base60lab.geometry`: `polygon_summary`, `chord_length_squared`
- `base60lab.metrics`: `analyze_fraction_in_bases` for rational components

### Inputs
- Constructible n: 3, 4, 5, 6, 8, 10, 12, 15, 16, 17, 20, 24, 30, 32, 34, 40, 48, 51, 60, 64, 68, 80, 85, 96, 102, 120, ...
- Focus on n with Fermat prime factors: 3, 5, 17, 257, 65537
- Maximum nested radical depth: 4 (for 17-gon, 257-gon)
- Digit expansion precision: 200 base-60 digits

### Exact Computation
- Exact trigonometric values via `trigonometry.py` for supported angles
- For higher n: symbolic nested radical expressions evaluated to high precision using exact rational arithmetic at each step
- Base-60 expansion of algebraic numbers via iterative multiplication (exact rational)
- Period detection in base-60 expansions

### Outputs
- JSON: `25_constructible_polygons_results.json`
  - Exact coordinate expressions for each constructible n
  - Base-60 digit expansions (first 200 digits)
  - Period/pattern analysis of expansions
  - Comparison with base-10 and base-12 expansions
- CSV: `25_coordinates.csv`, `25_base60_expansions.csv`, `25_pattern_analysis.csv`
- PNG: `25_base60_expansions.png`, `25_coordinate_comparison.png`, `25_17gon_construction.png`
- Markdown: `experiment-25-constructible-polygons-base60.md`

### Controls
- Same quantity: equal digit expansion length for all bases
- Exact arithmetic: nested radicals evaluated with rational intermediate steps
- Independent verification: coordinates satisfy x² + y² = 1 exactly
- Equal conditions: same precision for all bases
- Negative results: report n where base-60 shows no pattern advantage

### Success Criteria
- Document base-60 digit patterns for constructible polygon coordinates
- Identify which Fermat prime factors produce most visible patterns
- Correct claim 9: not "terminating" but "pattern-revealing" representations

---

## Experiment 26: Resonance Webs and Arnold Diffusion in Multi-Frequency Systems

### Hypothesis
In coupled multi-frequency oscillator systems (n ≥ 4), the resonance web structure — dense networks of overlapping resonances — is more navigable/analyzable in base-60 frequency space because the 2,3,5-factorization naturally aligns with the dominant low-order resonances that govern transport.

### Mathematical Foundation
- Hamiltonian systems with n degrees of freedom: H = H₀(I) + εH₁(θ, I)
- Resonances: k·ω = 0 for integer vector k (|k| small)
- Dominant resonances have small |k| and involve 2,3,5 factors
- Arnold diffusion: slow drift along resonance channels
- Frequency vector ω = (ω₁, ..., ωₙ) with 5-smooth ratios
- Base-60 representation of resonance vectors k may reveal web structure

### Existing Module Usage
- `base60lab.lissajous`: `Lissajous3DParameters`, `closure_info_3d`, `analyze_kam_diophantine_conditions`
- `base60lab.frequency`: `FrequencyRatio`, `Harmonic` for exact frequency vectors
- `base60lab.core.rational`: exact rational arithmetic for resonance conditions
- `base60lab.modular`: modular arithmetic for resonance lattice
- `base60lab.numerals`: base-60 representation of resonance vectors
- `base60lab.metrics`: compare base representations of resonance strengths

### Inputs
- Frequency vectors with 5-smooth ratios: ω = (1, 3/2, 4/3, 5/4, 6/5, 8/5, 9/8, 16/15, ...)
- Dimension n = 4, 5, 6
- Resonance order |k| ≤ 6
- Coupling strength ε sweep

### Exact Computation
- Resonance condition: k·ω = 0 computed exactly with `Rational`
- Resonance strength: |k|⁻¹ computed exactly
- Resonance web adjacency: two resonances connected if they share a common frequency
- Base-60 representation of resonance vectors k
- Diophantine approximation quality via `lissajous.diophantine_approximation_quality`

### Outputs
- JSON: `26_resonance_webs_results.json`
  - Resonance network graph (nodes, edges, weights)
  - Base-60 representation of resonance vectors
  - Arnold diffusion path estimates
  - KAM stability analysis per frequency vector
- CSV: `26_resonances.csv`, `26_resonance_network.csv`, `26_diffusion_paths.csv`
- PNG: `26_resonance_web_base60.png`, `26_resonance_web_base10.png`, `26_arnold_diffusion.png`, `26_kam_boundaries.png`
- Markdown: `experiment-26-resonance-webs-arnold-diffusion.md`

### Controls
- Same quantity: equal resonance order cutoff for all representations
- Exact arithmetic: all resonance conditions with `Rational`
- Independent verification: cross-check with numerical Hamiltonian integration
- Equal conditions: same frequency vectors, ε range
- Negative results: report dimensions/frequency sets where base-60 adds no insight

### Success Criteria
- Visualize resonance web in base-60 vs base-10 frequency coordinates
- Identify Arnold diffusion channels more clearly in base-60
- Quantify KAM boundary visibility across representations

---

## Summary: Module Reference Map

| Experiment | Primary Modules | Secondary Modules |
|------------|-----------------|-------------------|
| 22: NTT | fft_benchmarks, numerals, core.rational | metrics |
| 23: Continued Fractions | core.rational, numerals, metrics, sequences | modular |
| 24: Kuramoto | frequency, lissajous, core.rational, angles, numerals | metrics |
| 25: Constructible Polygons | core.rational, numerals, trigonometry, geometry | metrics |
| 26: Resonance Webs | lissajous, frequency, core.rational, modular, numerals | metrics |

---

## Implementation Priority

1. **Experiment 22 (NTT)** - Highest impact, clear computational application, directly tests Claim 11
2. **Experiment 23 (Continued Fractions)** - Tests Claims 8, 10 directly, pure mathematics
3. **Experiment 24 (Kuramoto)** - Connects to Experiment C (frequency/harmonics), tests Claim 10
4. **Experiment 25 (Constructible Polygons)** - Tests Claim 9 correction, connects to Experiment B (geometry)
5. **Experiment 26 (Resonance Webs)** - Most exploratory, builds on Experiment 20 (3D Lissajous)

---

## Output Format Consistency

All new experiments follow the established pattern:
- `run_experiment()` → returns results dict
- `save_json_results()` → `NN_experiment_name_results.json`
- `save_csv_measurements()` → multiple `NN_*.csv` files
- `create_visualizations()` → multiple `NN_*.png` files
- `generate_findings_markdown()` → `docs/findings/experiment-NN-name.md`
- `main()` → orchestrates all steps

Each experiment uses only exact rational arithmetic internally (`base60lab.core.rational.Rational`), with base conversion only for output/display.