# New Experiment Proposals (27-31)

Based on comprehensive review of:
- Existing experiments 01-10, 15-18, 20-26
- PLAN.md experiments A-G
- RESEARCH_PAPER.md new directions (Section 5)
- src/base60lab module capabilities
- Downloaded literature (Plimpton 322, smooth FFT, ECFFT, Babylonian astronomy)

---

## Experiment 27: Babylonian Plimpton 322 & Reciprocal Tables Reconstruction

### Hypothesis
Babylonian reciprocal tables (*igī*) of all regular sexagesimal numbers (prime factors 2,3,5) up to 81 can be exactly reconstructed using base60lab rational arithmetic, and Plimpton 322's 15 Pythagorean triples can be regenerated via the reciprocal-pair relationship:
- `col II = igī(x) − x/2`
- `col III = igī(x) + x/2`
where `x` is a regular sexagesimal number from the standard reciprocal table.

### Mathematical Foundation
- Plimpton 322 (ca. 1800 BCE) contains 15 rows of Pythagorean triples
- Mansfield & Wildberger (2017) interpretation: columns II and III are `igī(x) ∓ x/2` for regular x
- Regular sexagesimal numbers: prime factors ⊆ {2, 3, 5}
- The tablet's 15 rows correspond to 15 specific regular numbers
- Exact rational arithmetic can verify the reconstruction precisely

### Existing Module Usage
- `base60lab.numerals`: `rational_to_base`, `int_to_base`, `terminating_denominators`, `is_terminating_in_base`
- `base60lab.core.rational`: `Rational` for exact reciprocal computation
- `base60lab.geometry`: `pythagorean_triple`, `polygon_summary` (for angle verification)
- `base60lab.metrics`: `analyze_fraction_in_bases` for reciprocal analysis
- `base60lab.sequences`: generate sequences of regular numbers

### Inputs
- Regular sexagesimal numbers up to 81 (standard Babylonian table range)
- Target: 15 specific x-values that generate Plimpton 322 rows
- Base-60 representation of all reciprocals (exact, terminating)
- Pythagorean triple verification: (x, igī(x) - x/2, igī(x) + x/2)

### Exact Computation
- All reciprocals: `Rational(1, x)` for regular x (guaranteed terminating in base-60)
- Pythagorean triple check: `(x)² + (igī(x) - x/2)² = (igī(x) + x/2)²` exactly
- Base-60 conversion using exact `rational_to_base`
- No floating point anywhere

### Outputs
- JSON: `27_plimpton322_results.json`
  - Complete reciprocal table (regular numbers 1-81)
  - 15 Plimpton 322 rows reconstructed
  - Base-60 representation of all values
  - Verification of Pythagorean identity per row
- CSV: `27_reciprocal_table.csv`, `27_plimpton_rows.csv`, `27_verification.csv`
- PNG: `27_reciprocal_table.png`, `27_plimpton_reconstruction.png`, `27_base60_patterns.png`
- Markdown: `experiment-27-plimpton322-reciprocals.md`

### Controls (from PLAN.md)
- Same quantity: all regular numbers up to 81 (complete set)
- Exact arithmetic: all operations use `Rational`
- Independent verification: cross-check with Mansfield & Wildberger (2017) published triples
- Equal conditions: same x-values across representations
- Negative results: report any rows that don't match

### Success Criteria
- Exact reconstruction of all 15 Plimpton 322 Pythagorean triples
- Complete sexagesimal reciprocal table matching YBC 7290
- Demonstrate base-60 is the *only* base where all regular reciprocals terminate
- Verify the reciprocal-pair formula generates correct triples

---

## Experiment 28: Smooth Number FFT Size Prediction & Enumeration

### Hypothesis
Exact convergent formulas for 3-smooth (base-12) and 5-smooth (base-60) counting can predict optimal FFT sizes near any target length, enabling precise benchmark planning and NTT parameter selection without empirical search.

### Mathematical Foundation
- Schumacher (2016, arXiv:1608.06928): exact convergent formulas for smooth number counting
- 3-smooth numbers (Hamming numbers): 2ᵃ3ᵇ — relevant for base-12 factorization
- 5-smooth numbers (regular numbers): 2ᵃ3ᵇ5ᶜ — relevant for base-60 factorization
- Count function: Ψ(x, y) = #{n ≤ x : P(n) ≤ y} where P(n) = largest prime factor
- Inverse problem: find k-th smooth number (needed for "next fast len" algorithms)
- SciPy's `next_fast_len` uses heuristic; exact formula enables optimal planning

### Existing Module Usage
- `base60lab.fft_benchmarks`: `is_smooth`, `is_5_smooth`, `is_12_smooth`, `is_60_smooth`, `next_fast_len_smooth`
- `base60lab.core.rational`: `Rational` for exact counting formulas
- `base60lab.numerals`: base conversion for displaying smooth numbers
- `base60lab.sequences`: generate sequences of smooth numbers
- `base60lab.metrics`: compare base representations of smooth numbers

### Inputs
- Target sizes: 10³, 10⁴, 10⁵, 10⁶, 10⁷
- Smoothness bounds: B = 3 (12-smooth), B = 5 (60-smooth), B = 7 (for comparison)
- Count formulas: Ψ(x, 3) and Ψ(x, 5) using Schumacher's convergent series
- Inverse lookup: k-th smooth number for k = 1..1000

### Exact Computation
- Smooth number enumeration via exact integer generation (no floats)
- Schumacher's convergent formula: Ψ(x, y) = Σ μ(d) ⌊x/d⌋ for d y-smooth (exact integer arithmetic)
- Inverse lookup via binary search on count function
- Next/previous smooth number to any target
- Base-60 representation of smooth numbers for pattern analysis

### Outputs
- JSON: `28_smooth_fft_prediction_results.json`
  - Count tables: Ψ(x, 3) and Ψ(x, 5) for x up to 10⁷
  - Optimal FFT sizes near each target
  - k-th smooth number tables
  - Base-60 digit patterns of smooth numbers
- CSV: `28_count_table_3smooth.csv`, `28_count_table_5smooth.csv`, `28_optimal_sizes.csv`, `28_kth_smooth.csv`
- PNG: `28_count_convergence.png`, `28_optimal_size_comparison.png`, `28_base60_smooth_patterns.png`, `28_next_fast_len_error.png`
- Markdown: `experiment-28-smooth-fft-prediction.md`

### Controls
- Same quantity: equal target ranges for 3-smooth and 5-smooth
- Exact arithmetic: all counting via integer operations
- Independent verification: cross-check with Schumacher (2016) published values and OEIS A003586 (3-smooth), A051037 (5-smooth)
- Equal conditions: same target sizes across smoothness classes
- Negative results: report targets where no good smooth size exists

### Success Criteria
- Exact count formulas match Schumacher (2016) to full precision
- Predict optimal FFT sizes with <1% deviation from true smooth numbers
- Demonstrate 5-smooth (base-60) provides denser coverage than 3-smooth (base-12)
- Provide practical "next fast len" algorithm with proven error bounds

---

## Experiment 29: Elliptic Curve FFT (ECFFT) with 5-Smooth Group Orders

### Hypothesis
Elliptic Curve FFT (Ben-Sasson et al. 2021) using elliptic curves with 5-smooth (base-60) group orders provides a viable alternative to NTT for finite field arithmetic, where the natural 2,3,5 factorization of 60 aligns with the group structure of curves over extension fields.

### Mathematical Foundation
- ECFFT: FFT on elliptic curve groups instead of multiplicative groups
- Requires: elliptic curve E/F_q with group order #E(F_q) = N = 2ᵃ3ᵇ5ᶜ (5-smooth)
- Coset decomposition: E = H₁ ∪ ... ∪ Hₘ where Hᵢ are subgroups of smooth order
- Base-60 factorization naturally matches 5-smooth group orders
- Unlike NTT, no requirement for q ≡ 1 (mod N) — only need curve with smooth group order
- Applications: SNARKs, polynomial commitment schemes, polynomial evaluation

### Existing Module Usage
- `base60lab.fft_benchmarks`: `is_5_smooth`, `is_60_smooth`, smoothness checking
- `base60lab.core.rational`: `Rational` for exact group order arithmetic
- `base60lab.modular`: modular arithmetic for curve operations
- `base60lab.numerals`: base-60 representation of group orders and coordinates
- `base60lab.metrics`: compare base representations of group orders

### Inputs
- Search space: curves over F_p and F_{p²} for p < 2³¹
- Target group orders: 5-smooth numbers N = 2ᵃ3ᵇ5ᶜ in range [10³, 10⁶]
- Curve forms: short Weierstrass y² = x³ + ax + b, Montgomery, Edwards
- Search for curves with smooth group order using Schoof-Elkies-Atkin (SEA) algorithm

### Exact Computation
- Group order verification: #E(F_q) computed exactly (integer)
- Smoothness check: exact prime factorization of group order
- Base-60 representation of group orders and coordinates
- Subgroup decomposition: find chains of subgroups with 5-smooth orders
- All arithmetic in finite fields using exact integer operations

### Outputs
- JSON: `29_ecfft_smooth_orders_results.json`
  - Curves with 5-smooth group orders found
  - Subgroup chain decompositions
  - Base-60 representation of group orders
  - ECFFT complexity estimates vs NTT
- CSV: `29_curves_5smooth.csv`, `29_subgroup_chains.csv`, `29_group_orders_base60.csv`
- PNG: `29_curve_search_results.png`, `29_subgroup_lattice.png`, `29_ecfft_vs_ntt_comparison.png`, `29_base60_group_orders.png`
- Markdown: `experiment-29-ecfft-smooth-orders.md`

### Controls
- Same quantity: equal search effort per curve form
- Exact arithmetic: all group orders and coordinates exact integers
- Independent verification: cross-check with Ben-Sasson et al. (2021) known curves
- Equal conditions: same smoothness bound (5-smooth) for all curves
- Negative results: report curve forms where no 5-smooth curves found

### Success Criteria
- Find ≥ 10 elliptic curves with 5-smooth group orders in practical ranges
- Construct complete subgroup chains for ECFFT
- Demonstrate base-60 representation naturally encodes subgroup structure
- Compare ECFFT complexity with NTT for same smoothness class

---

## Experiment 30: Babylonian Planetary Periods & Synodic Cycles in Base-60

### Hypothesis
Babylonian astronomical tablets recording planetary synodic periods (e.g., Venus 584 days, Mars 780 days, Jupiter 399 days, Saturn 378 days) exhibit natural termination and pattern structure in base-60 representation, explaining why sexagesimal was preserved for astronomy.

### Mathematical Foundation
- Synodic period: time between successive conjunctions with Sun
- Babylonian Goal-Year Texts: periods expressed in sexagesimal
- Key periods (days): Mercury 116, Venus 584, Mars 780, Jupiter 399, Saturn 378
- Sidereal periods (years): Mercury 0.241, Venus 0.615, Earth 1.0, Mars 1.881, Jupiter 11.862, Saturn 29.457
- Base-60 = 2²×3×5; many planetary periods have 5-smooth rational approximations
- Example: 584 = 2³×73 (not 5-smooth), but 584/360 = 1;37,20 in base-60 (terminating!)
- 378 = 2×3³×7, 378/360 = 1;3,0 in base-60 (terminating!)

### Existing Module Usage
- `base60lab.numerals`: `rational_to_base`, `int_to_base`, `is_terminating_in_base`, `repeating_period_in_base`
- `base60lab.core.rational`: `Rational` for exact period ratios
- `base60lab.angles`: `turn_to_degrees`, `normalize_turns` for phase analysis
- `base60lab.frequency`: `FrequencyRatio`, `Phase` for exact frequency relationships
- `base60lab.metrics`: `analyze_fraction_in_bases`, `compare_bases`
- `base60lab.geometry`: circle subdivisions for zodiac analysis

### Inputs
- Planetary synodic periods (days): Mercury 116, Venus 584, Mars 780, Jupiter 399, Saturn 378
- Sidereal periods (Earth years as exact rationals from modern astronomy)
- Babylonian period relations (e.g., Venus 8 years = 5 synodic cycles = 2920 days)
- Zodiac: 12 signs × 30° = 360°, base-60 subdivisions
- Goal-Year periods: combinations yielding integer years

### Exact Computation
- All periods as exact `Rational` (no floats)
- Synodic/sidereal ratios as exact `FrequencyRatio`
- Base-60 representation of all periods and ratios
- Phase alignment over Goal-Year periods (exact turn fractions)
- Zodiac position computation in base-60 degrees

### Outputs
- JSON: `30_babylonian_planetary_results.json`
  - Synodic/sidereal periods in all three bases
  - Goal-Year period alignments
  - Base-60 terminating/repeating analysis
  - Zodiac positions over time
- CSV: `30_synodic_periods.csv`, `30_sidereal_ratios.csv`, `30_goal_year_alignments.csv`, `30_zodiac_positions.csv`
- PNG: `30_planetary_periods_base60.png`, `30_synodic_alignment.png`, `30_goal_year_visualization.png`, `30_base_comparison.png`
- Markdown: `experiment-30-babylonian-planetary.md`

### Controls
- Same quantity: all 5 classical planets + Mercury
- Exact arithmetic: all periods and ratios as `Rational`
- Independent verification: cross-check with Neugebauer (1955) Babylonian astronomy tables and modern JPL ephemerides
- Equal conditions: same precision for all bases
- Negative results: report planets/periods where base-60 offers no advantage

### Success Criteria
- Demonstrate terminating base-60 representations for key planetary ratios
- Reconstruct Babylonian Goal-Year period relations exactly
- Show base-60 zodiac positions align naturally with synodic cycles
- Explain historical preservation of sexagesimal for astronomy

---

## Experiment 31: Spherical Trigonometry & 3D Rotations in Base-60

### Hypothesis
Spherical trigonometry (navigation, astronomy) and 3D rotation groups (SO(3), quaternions) have natural representations in base-60 because:
1. Spherical triangle angles sum to π + area (excess), and 360° = 6×60 = 30×12
2. Quaternion components for rational rotations have denominators with 2,3,5 factors
3. Euler angle representations in base-60 reveal symmetry structure
4. Hopf fibration S³ → S² has natural 5-smooth structure

### Mathematical Foundation
- Spherical law of cosines: cos(a) = cos(b)cos(c) + sin(b)sin(c)cos(A)
- Spherical excess: E = A + B + C - π (area on unit sphere)
- Euler angles: (α, β, γ) ∈ [0, 2π)³, natural in base-60 (360° = 6×60)
- Quaternions: q = cos(θ/2) + sin(θ/2)(xi + yj + zk)
- For rational rotations θ = 2π·(p/q), quaternion components are algebraic
- Hopf map: (z₁, z₂) → (2z₁z₂*, |z₁|² - |z₂|²) with S¹ fibers
- Binary polyhedral groups: 2T (24), 2O (48), 2I (120) — 120 = 2³×3×5 (5-smooth!)

### Existing Module Usage
- `base60lab.trigonometry`: `cos_degrees`, `sin_degrees`, `spherical_law_of_cosines`
- `base60lab.geometry`: `spherical_triangle_area`, `polygon_summary`
- `base60lab.angles`: `turn_to_degrees`, `degrees_to_turns`, `normalize_turns`
- `base60lab.numerals`: `rational_to_base` for algebraic number expansions
- `base60lab.core.rational`: `Rational` for exact angle arithmetic
- `base60lab.lissajous`: `Lissajous3DParameters` for 3-torus trajectories
- `base60lab.frequency`: `Phase` for quaternion angle components

### Inputs
- Spherical triangles with rational angles (multiples of 1° = 1/360 turn)
- Key angles: 30°, 45°, 60°, 90°, 120° and their base-60 fractions
- Binary polyhedral group elements (24, 48, 120 elements)
- Rational rotation angles: 2π·(p/q) for q 5-smooth
- Hopf fibration parameters with 5-smooth fiber ratios

### Exact Computation
- All angles as exact `Rational` (fractions of turn)
- Trigonometric values via `trigonometry.py` exact methods
- Spherical trigonometry identities verified exactly
- Quaternion components for rational rotations
- Base-60 expansion of algebraic coordinates (high precision)
- Hopf map computation with exact rational arithmetic

### Outputs
- JSON: `31_spherical_trig_results.json`
  - Spherical triangle solutions in all three bases
  - Quaternion representations of rational rotations
  - Binary polyhedral group element coordinates
  - Hopf fiber base-60 patterns
- CSV: `31_spherical_triangles.csv`, `31_quaternion_rotations.csv`, `31_polyhedral_groups.csv`, `31_hopf_fibers.csv`
- PNG: `31_spherical_triangles_base60.png`, `31_quaternion_base60.png`, `31_2I_group_120.png`, `31_hopf_base60.png`
- Markdown: `experiment-31-spherical-trigonometry.md`

### Controls
- Same quantity: equal number of spherical triangles per angle family
- Exact arithmetic: all angles and trig values as `Rational`/algebraic
- Independent verification: cross-check with standard spherical trigonometry references
- Equal conditions: same precision for all bases
- Negative results: report angle families where base-60 adds no insight

### Success Criteria
- Document base-60 advantage for spherical triangle angle representation
- Show binary icosahedral group (120 elements, 5-smooth) has natural base-60 structure
- Demonstrate Hopf fibration fibers align with base-60 phase representation
- Connect to Experiment 20 (3D Lissajous) and Experiment 26 (resonance webs)

---

## Summary: Module Reference Map

| Experiment | Primary Modules | Secondary Modules |
|------------|-----------------|-------------------|
| 27: Plimpton 322 | numerals, core.rational, geometry | metrics, sequences |
| 28: Smooth FFT Prediction | fft_benchmarks, core.rational, numerals | sequences, metrics |
| 29: ECFFT | fft_benchmarks, modular, core.rational, numerals | metrics |
| 30: Babylonian Planetary | numerals, core.rational, angles, frequency, geometry | metrics |
| 31: Spherical Trigonometry | trigonometry, geometry, angles, numerals, lissajous, frequency | core.rational, metrics |

---

## Implementation Priority

1. **Experiment 27 (Plimpton 322)** — Historical significance, pure exact arithmetic, validates base-60 for Babylonian math
2. **Experiment 28 (Smooth FFT Prediction)** — Practical computational application, extends Experiment 16
3. **Experiment 30 (Babylonian Planetary)** — Connects to historical astronomy, natural base-60 fit
4. **Experiment 31 (Spherical Trigonometry)** — Extends 3D Lissajous (Exp 20) to spherical geometry
5. **Experiment 29 (ECFFT)** — Most exploratory, builds on NTT (Exp 22) and modular forms (Exp 18)

---

Each experiment uses only exact rational arithmetic internally (`base60lab.core.rational.Rational`), with base conversion only for output/display.