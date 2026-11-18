# New Experiment Proposals (32-36)

Based on comprehensive review of:
- Existing experiments 01-10, 15-18, 20-26
- Proposed experiments 27-31
- PLAN.md experiments A-G
- Literature search report (6 target areas with significant gaps)
- src/base60lab module capabilities

---

## Experiment 32: Mixed-Radix One-Time Pad (MR-OTP) with Base-12 and Base-60

### Hypothesis
The Mixed-Radix One-Time Pad (Buono 2026) instantiated with base-12 (duodecimal) and base-60 (sexagesimal) alphabets provides information-theoretic perfect secrecy with higher key entropy per symbol than binary OTP, and the Horner decomposition (Buono 2026b) enables bias-free conversion of QKD binary entropy to uniform base-12/60 keys.

### Mathematical Foundation
- **MR-OTP (Buono 2026, 2606.16040)**: Generalizes Shannon's OTP to heterogeneous alphabets. For a message space with mixed-radix alphabet sizes (r₁, r₂, ..., rₙ), encryption is cᵢ = (mᵢ + kᵢ) mod rᵢ with uniform random key kᵢ ∈ [0, rᵢ).
- **Perfect secrecy proof**: H(M|C) = H(M) holds for any mixed-radix system. Classical binary OTP is special case rᵢ = 2.
- **Horner decomposition (Buono 2026b, 2606.18526)**: Convert binary QKD output to uniform mixed-radix keys via biased coin flipping using Horner's method with rejection sampling for exact uniformity.
- **Base-12 alphabet**: 12 symbols per position → log₂(12) ≈ 3.585 bits/symbol (vs 1 bit/symbol for binary)
- **Base-60 alphabet**: 60 symbols per position → log₂(60) ≈ 5.907 bits/symbol
- **Key efficiency**: Fewer symbols needed for same security level; base-60 key is 5.9× shorter than binary for equivalent entropy.

### Existing Module Usage
- `base60lab.numerals`: `rational_to_base`, `int_to_base`, `convert_rational_base` for key representation
- `base60lab.core.rational`: `Rational` for exact probability calculations in Horner decomposition
- `base60lab.metrics`: `compute_base_metrics`, `compare_bases` for alphabet efficiency comparison
- `base60lab.modular`: `mod_add`, `mod_sub`, `mod_mul` for encryption/decryption operations
- `base60lab.sequences`: Generate uniform random sequences for key material

### Inputs
- Message lengths: 10, 100, 1000 symbols
- Alphabets: Binary (r=2), Base-12 (r=12), Base-60 (r=60), Mixed-radix (e.g., [12, 60, 12, 60] alternating)
- QKD binary entropy source: simulated uniform random bits
- Horner decomposition rejection threshold: configurable
- Security parameter: target entropy in bits (128, 256, 512)

### Exact Computation
- All modular arithmetic using exact integer operations (Python ints, no floats)
- Horner decomposition: exact rational probability calculations using `Rational`
- Uniformity verification: χ² test with exact expected counts as `Rational`
- Key entropy: exact calculation H = Σ log₂(rᵢ) using exact rational log₂ via high-precision binary splitting
- Rejection sampling: exact acceptance probability as `Rational`

### Outputs
- JSON: `32_mr_otp_results.json`
  - Key generation statistics per alphabet (length, entropy, uniformity p-values)
  - Encryption/decryption correctness verification (100% required)
  - Horner decomposition efficiency (acceptance rate, bits consumed per output symbol)
  - Comparison table: binary vs base-12 vs base-60 vs mixed-radix
- CSV: `32_key_generation.csv`, `32_encryption_verification.csv`, `32_horner_efficiency.csv`, `32_alphabet_comparison.csv`
- PNG: `32_key_entropy_comparison.png`, `32_horner_convergence.png`, `32_mixed_radix_distribution.png`, `32_alphabet_efficiency.png`
- Markdown: `experiment-32-mr-otp-base12-base60.md`

### Controls (from PLAN.md)
- **Same quantity**: Equal target entropy (128, 256, 512 bits) across all alphabets
- **Exact arithmetic**: All modular operations and probability calculations use `Rational`
- **Independent verification**: Cross-check perfect secrecy proof with Buono 2026 Theorem 1; verify Horner decomposition against Algorithm 1 in Buono 2026b
- **Equal conditions**: Same QKD entropy source simulation for all alphabets
- **Negative results**: Report rejection rates where Horner decomposition is inefficient; report mixed-radix configurations with worse uniformity than fixed-base

### Success Criteria
- Demonstrate perfect secrecy holds for base-12, base-60, and mixed-radix MR-OTP
- Quantify key length reduction: base-12 = 3.58× shorter, base-60 = 5.91× shorter than binary
- Verify Horner decomposition achieves > 90% acceptance rate for base-12/60 from binary QKD
- Show mixed-radix (alternating 12/60) achieves intermediate efficiency with flexibility

---

## Experiment 33: MrRoPE Mixed-Radix Rotary Position Embeddings for Base-12 and Base-60

### Hypothesis
The MrRoPE framework (Tian et al. 2026, ICLR 2026) instantiated with base-12 (radix-3/4) and base-60 (radix-3/4/5) rotary position embeddings extends context length beyond 128K tokens with superior long-range dependency modeling for cyclic/periodic data, because the 2,3,5-factorization naturally aligns with hierarchical temporal scales.

### Mathematical Foundation
- **RoPE (Su et al. 2021)**: Rotary Position Embedding encodes position p as rotation by θ·p in complex plane, with frequencies θₖ = 10000^(-2k/d).
- **MrRoPE (Tian et al. 2026, 2601.22181)**: Treats RoPE as β-radix encoding system. Two variants:
  - **MrRoPE-Uni**: Uniform radix β across all dimensions
  - **MrRoPE-Pro**: Progressive radix conversion, higher radices for lower frequencies
- **Base-12 instantiation**: Radix β = 12 = 2²×3. Dimensions grouped by factor: 2-dim (radix-4), 3-dim (radix-3)
- **Base-60 instantiation**: Radix β = 60 = 2²×3×5. Dimensions grouped: 4-dim (radix-4), 3-dim (radix-3), 5-dim (radix-5)
- **Key property**: The mixed-radix decomposition naturally encodes hierarchical timescales (seconds, minutes, hours for base-60 analogy)

### Existing Module Usage
- `base60lab.numerals`: `rational_to_base`, `int_to_base` for radix conversion of position indices
- `base60lab.frequency`: `FrequencyRatio`, `Phase` for exact frequency/wavelength representation
- `base60lab.angles`: `turn_to_degrees`, `normalize_turns` for rotation angles
- `base60lab.core.rational`: `Rational` for exact frequency ratios and interpolation
- `base60lab.trigonometry`: `cos_degrees`, `sin_degrees` for exact rotation matrix elements
- `base60lab.metrics`: `compare_bases` for evaluating representation efficiency

### Inputs
- Model dimensions: d = 128, 256, 512, 1024
- Radix configurations: 
  - Binary (β=2, standard RoPE)
  - Base-12 Uni (β=12 uniform)
  - Base-12 Pro (progressive: radices 4,3,4,3,...)
  - Base-60 Uni (β=60 uniform)
  - Base-60 Pro (progressive: radices 4,3,5,4,3,5,...)
- Context lengths: 1K, 4K, 16K, 64K, 128K, 256K, 512K, 1M tokens
- Base frequency: θ₀ = 1/10000 (standard) and θ₀ = 1/60 (base-60 natural)
- Evaluation: Synthetic periodic tasks (copy, reverse, arithmetic with cyclic patterns)

### Exact Computation
- Position encoding: Exact rational rotation angles θₖ·p as `Rational` (no floating point)
- Radix conversion: Exact base conversion of position index p using `numerals.py`
- Frequency ratios: Exact `FrequencyRatio` objects for each dimension group
- Interpolation (YaRN/NTK): Exact rational scaling factors
- Attention computation: Exact complex rotation via cos/sin of rational angles (using `trigonometry.py` exact values where possible, high-precision rational approximation otherwise)

### Outputs
- JSON: `33_mrrope_results.json`
  - Position encoding matrices for each configuration (first 100 positions)
  - Frequency/wavelength spectra in base-10, base-12, base-60
  - Long-context extrapolation error (exact rational distance)
  - Periodic task accuracy (exact counts)
- CSV: `33_position_encodings.csv`, `33_frequency_spectra.csv`, `33_extrapolation_error.csv`, `33_periodic_tasks.csv`
- PNG: `33_rope_frequency_base60.png`, `33_mrrope_progressive_radices.png`, `33_extrapolation_comparison.png`, `33_periodic_accuracy.png`
- Markdown: `experiment-33-mrrope-base12-base60.md`

### Controls (from PLAN.md)
- **Same quantity**: Equal model dimensions and context lengths across all radix configurations
- **Exact arithmetic**: All position encodings and rotations use exact `Rational` arithmetic
- **Independent verification**: Cross-check frequency spectra with Tian et al. 2026 Figure 3; verify RoPE equivalence at β=2
- **Equal conditions**: Same base frequency θ₀, same synthetic tasks, same evaluation protocol
- **Negative results**: Report radix configurations where extrapolation degrades; report dimensions where base-60 offers no advantage over base-12

### Success Criteria
- Implement MrRoPE-Uni and MrRoPE-Pro for β=12 and β=60 using exact rational arithmetic
- Demonstrate > 128K context extrapolation with < 5% degradation (vs > 50% for standard RoPE)
- Show base-60 Pro outperforms base-12 Pro on tasks with 3-timescale hierarchy (e.g., hour/minute/second)
- Verify exact rational arithmetic eliminates numerical drift in long-context position encoding

---

## Experiment 34: RNS Moduli Sets and MRUD Redundant Arithmetic for Base-12 and Base-60

### Hypothesis
Optimal Residue Number System (RNS) moduli sets for base-12 ({3, 4, 5} or {5, 7, 8, 9}) and base-60 ({4, 3, 5, 7, 11, 13} or larger co-prime sets) enable carry-free arithmetic with dynamic range matching the base's information density, and MRUD (Maximally Redundant Unsigned Digit) representation (Rahimi & Azarpeyvand 2026) extends redundant arithmetic to base-60 with 30% lower delay, 26% smaller area, and 87% lower power than conventional adders.

### Mathematical Foundation
- **RNS (Residue Number System)**: Represent integer X ∈ [0, M) by residues (x₁, x₂, ..., xₙ) where xᵢ = X mod mᵢ and M = ∏mᵢ. Moduli must be pairwise co-prime.
- **Base-12 RNS**: Natural moduli {3, 4, 5} → M = 60 (dynamic range 60). Extended: {5, 7, 8, 9} → M = 2520.
- **Base-60 RNS**: Natural moduli {4, 3, 5} → M = 60. Extended: {7, 11, 13, 17, 19, 23} → M > 10⁶.
- **Gorodecky 2026 (2603.24387)**: Algorithmic generation of optimal co-prime moduli sets balancing bit-lengths and maximizing dynamic range.
- **MRUD (Rahimi & Azarpeyvand 2026, 2610.39638)**: Redundant digit set D = {-a, ..., 0, ..., a} with a = β-1 for radix β. Carry-free addition: each digit sum stays within [-a, a]. Evaluated up to β=2ʰ; base-60 (β=60) extension needed.
- **Key property**: Base-60 = 2²×3×5 naturally decomposes to RNS moduli {4, 3, 5} with perfect Chinese Remainder Theorem reconstruction.

### Existing Module Usage
- `base60lab.modular`: `mod_add`, `mod_mul`, `mod_inv`, `mod_div`, `mod_pow` for RNS arithmetic
- `base60lab.numerals`: `int_to_base`, `rational_to_base` for base-12/60 representation of RNS values
- `base60lab.core.rational`: `Rational` for exact dynamic range calculations and redundancy factors
- `base60lab.metrics`: `compare_bases` for evaluating RNS efficiency across bases
- `base60lab.sequences`: Generate co-prime moduli sequences

### Inputs
- Target dynamic ranges: 10², 10³, 10⁴, 10⁶, 10⁹
- Base-12 moduli candidates: {3,4,5}, {5,7,8,9}, {7,8,9,11,13}
- Base-60 moduli candidates: {4,3,5}, {7,11,13,17}, {7,11,13,17,19,23,29}
- MRUD redundancy factor: a = β-1 (full redundancy) and a = ⌈β/2⌉ (minimal)
- Operation mix: Addition (70%), Multiplication (20%), Conversion (10%)
- Bit-width per modulus: 4-bit, 8-bit, 16-bit

### Exact Computation
- RNS representation: Exact integer residues via `modular.py`
- CRT reconstruction: Exact via Garner's algorithm using `mod_inv` and `mod_mul`
- Dynamic range: Exact product M = ∏mᵢ as Python int
- Redundancy analysis: Exact rational redundancy factor ρ = (2a+1)/β
- Carry-free verification: Exhaustive check that all digit sums ∈ [-a, a] for each base
- Delay/area/power: Analytical models using exact rational parameters from MRUD paper

### Outputs
- JSON: `34_rns_mrud_results.json`
  - Optimal moduli sets per base and dynamic range
  - Dynamic range vs. moduli count trade-off curves
  - MRUD carry-free verification results
  - Estimated delay/area/power for base-12 and base-60 adders
  - Base conversion overhead (RNS ↔ base-12/60)
- CSV: `34_moduli_sets.csv`, `34_dynamic_range.csv`, `34_mrud_verification.csv`, `34_hardware_estimates.csv`
- PNG: `34_moduli_optimization.png`, `34_mrud_carry_free.png`, `34_base12_vs_base60_rns.png`, `34_hardware_comparison.png`
- Markdown: `experiment-34-rns-mrud-base12-base60.md`

### Controls (from PLAN.md)
- **Same quantity**: Equal target dynamic ranges for base-12 and base-60 RNS
- **Exact arithmetic**: All RNS operations and CRT reconstruction use exact integer arithmetic
- **Independent verification**: Cross-check moduli optimality with Gorodecky 2026 algorithm; verify MRUD carry-free property matches Rahimi & Azarpeyvand 2026
- **Equal conditions**: Same operation mix, same bit-width assumptions, same analytical models
- **Negative results**: Report dynamic ranges where base-12 RNS outperforms base-60; report MRUD redundancy factors where carry-free fails

### Success Criteria
- Generate optimal co-prime moduli sets for base-12 and base-60 matching Gorodecky 2026
- Verify MRUD carry-free addition for base-12 (β=12) and base-60 (β=60)
- Demonstrate base-60 RNS achieves 5.9× information density of binary with only 3 moduli {4,3,5}
- Quantify hardware benefits: target 30% delay reduction, 26% area reduction vs non-redundant base-60 adder

---

## Experiment 35: Base-12 and Base-60 CORDIC for Transcendental Functions

### Hypothesis
Mixed-radix CORDIC (Panchal et al. 2026, 2604.23547) extended to base-12 (radix-4/3) and base-60 (radix-4/3/5) computes transcendental functions (sin, cos, atan, sinh, cosh, exp, ln) with zero DSP usage, 835 logic slices on FPGA, and MAE < 10⁻⁴, where the base-60 factorization enables optimal micro-rotation angle selection matching sexagesimal angle representation.

### Mathematical Foundation
- **CORDIC (Volder 1959)**: Coordinate Rotation Digital Computer computes rotations via iterative micro-rotations by precomputed angles arctan(2⁻ⁱ) for binary.
- **Mixed-Radix CORDIC (Panchal et al. 2026)**: Generalizes to radices {2, 4, 2-LVC} with hyperbolic rotation. Micro-rotation angles: arctan(β⁻ⁱ) for radix β.
- **Base-12 CORDIC**: Radices {4, 3}. Micro-angles: arctan(4⁻ⁱ), arctan(3⁻ⁱ). 4⁻ⁱ = 2⁻²ⁱ enables fast shifts; 3⁻ⁱ requires division but better angle resolution.
- **Base-60 CORDIC**: Radices {4, 3, 5}. Micro-angles: arctan(4⁻ⁱ), arctan(3⁻ⁱ), arctan(5⁻ⁱ). Natural match to sexagesimal degrees: 1° = 1/360 turn = 1/(6×60).
- **Key property**: Base-60 angle representation (degrees/minutes/seconds) maps directly to CORDIC iterations with radices 60, 60, 60 or mixed 6/10/6.

### Existing Module Usage
- `base60lab.trigonometry`: `cos_degrees`, `sin_degrees`, `atan_rational` for exact micro-rotation angles
- `base60lab.numerals`: `rational_to_base`, `int_to_base` for angle representation in base-60
- `base60lab.core.rational`: `Rational` for exact iterative computation (no floating point)
- `base60lab.angles`: `turn_to_degrees`, `degrees_to_turns`, `normalize_turns` for angle normalization
- `base60lab.metrics`: `analyze_fraction_in_bases` for micro-angle representation efficiency

### Inputs
- Target functions: sin, cos, atan, sinh, cosh, atanh, exp, ln, sqrt
- Input ranges: Angles in [0, 2π) as exact `Rational` turns; hyperbolic in [0, 1]
- Radix configurations:
  - Binary (radix-2, baseline)
  - Base-12 mixed (radices 4, 3)
  - Base-60 mixed (radices 4, 3, 5)
  - Base-60 pure (radix 60, 60, 60 for degrees/minutes/seconds)
- Iteration counts: 8, 16, 24, 32, 40, 48
- Precision target: MAE < 10⁻⁴, < 10⁻⁶, < 10⁻⁸

### Exact Computation
- Micro-rotation angles: Exact `Rational` via `atan_rational` from `trigonometry.py`
- CORDIC gain: Exact product K = ∏√(1+β⁻²ⁱ) as `Rational`
- Iteration: Exact rational arithmetic for x, y, z registers using `Rational`
- Convergence analysis: Exact rational error bounds
- Base-60 representation: Input/output angles converted via `numerals.py`

### Outputs
- JSON: `35_cordic_results.json`
  - Micro-rotation angle tables per radix configuration (exact rational)
  - Convergence curves: MAE vs iterations for each function
  - CORDIC gain K per configuration (exact rational)
  - Base-60 angle representation efficiency
- CSV: `35_micro_angles.csv`, `35_convergence.csv`, `35_gain_factors.csv`, `35_function_accuracy.csv`
- PNG: `35_cordic_convergence_base60.png`, `35_micro_angle_spectra.png`, `35_function_errors.png`, `35_radix_comparison.png`
- Markdown: `experiment-35-cordic-base12-base60.md`

### Controls (from PLAN.md)
- **Same quantity**: Equal iteration counts and input ranges across all radix configurations
- **Exact arithmetic**: All CORDIC iterations use exact `Rational` arithmetic
- **Independent verification**: Cross-check micro-angles with Panchal et al. 2026 Table I; verify CORDIC gain formulas
- **Equal conditions**: Same functions, same precision targets, same evaluation metrics
- **Negative results**: Report functions where base-60 CORDIC converges slower than binary; report precision targets unachievable within 48 iterations

### Success Criteria
- Implement mixed-radix CORDIC for base-12 (4,3) and base-60 (4,3,5) with exact rational arithmetic
- Achieve MAE < 10⁻⁴ for sin/cos/atan within 24 iterations for base-60
- Demonstrate base-60 pure CORDIC (radix-60 iterations) naturally computes degrees/minutes/seconds
- Show zero DSP usage achievable (shift-add only) for base-12/60 radices
- Verify exact rational arithmetic eliminates accumulation error in long iteration chains

---

## Experiment 36: Crypto-Agile Mixed-Radix NTT for Base-12 and Base-60 in Post-Quantum Cryptography

### Hypothesis
The crypto-agile mixed-radix NTT accelerator (Lee et al. 2026, ePrint 2026/2610) with unified radix-2/3 butterfly extended to base-12 (radix-3/4) and base-60 (radix-2/3/4/5) supports all major PQC standards (ML-KEM, ML-DSA, HAETAE, Falcon, Dilithium) on a single datapath, where base-60's 2,3,5-factorization provides the superset of radices needed for all NTT-friendly primes.

### Mathematical Foundation
- **NTT (Number-Theoretic Transform)**: FFT over finite field F_p where p = k·N + 1 has primitive N-th root of unity. Requires N | (p-1).
- **Mixed-Radix NTT**: Decompose N = ∏rᵢ into radices rᵢ; compute via Cooley-Tukey with mixed-radix butterflies.
- **Lee et al. 2026**: Unified butterfly for radix-2 and radix-3; conflict-free memory mapping; supports ML-KEM (256), ML-DSA (256), HAETAE (512, 1024).
- **Base-12 extension**: Radices 3, 4 (since 12 = 3×4). NTT lengths: 3ᵃ·4ᵇ.
- **Base-60 extension**: Radices 2, 3, 4, 5 (since 60 = 2²×3×5). NTT lengths: 2ᵃ·3ᵇ·4ᶜ·5ᵈ.
- **PQC requirements**: 
  - ML-KEM/ML-DSA: N=256 (power of 2)
  - Falcon: N=512, 1024 (powers of 2)
  - HAETAE: N=512, 1024
  - Dilithium: N=256
  - All use NTT-friendly primes: 12289 (2¹²·3+1), 7681 (2⁸·3·5+1), 12289 (2¹²·3+1), 8380417 (2²³·1+1)

### Existing Module Usage
- `base60lab.fft_benchmarks`: `is_smooth`, `is_5_smooth`, `is_12_smooth`, `generate_sizes` for transform length generation
- `base60lab.numerals`: `int_to_base`, `rational_to_base` for NTT parameter representation
- `base60lab.core.rational`: `Rational` for exact twiddle factor computation
- `base60lab.modular`: `mod_add`, `mod_mul`, `mod_pow`, `mod_inv` for finite field arithmetic
- `base60lab.metrics`: `compare_bases` for evaluating NTT parameter efficiency

### Inputs
- PQC standards: ML-KEM-512/768/1024, ML-DSA-44/65/87, Falcon-512/1024, HAETAE-128/192/256, Dilithium-2/3/5
- Target primes: 12289, 7681, 8380417, 1004535809, 2013265921, 2147483647
- Radix configurations:
  - Binary (radix-2 only, baseline)
  - Base-12 (radices 3, 4)
  - Base-60 (radices 2, 3, 4, 5)
  - Full mixed (radices 2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17)
- Transform lengths per standard: all NTT sizes required
- Architecture constraints: Single unified butterfly datapath, conflict-free memory

### Exact Computation
- NTT parameters: Exact integer arithmetic for primitive root search, twiddle factors
- Butterfly operations: Exact modular arithmetic via `modular.py`
- Memory mapping: Exact index calculation for conflict-free access
- Twiddle factors: Precomputed exact values using `mod_pow`
- Performance model: Exact cycle count based on radix decomposition depth

### Outputs
- JSON: `36_ntt_pqc_results.json`
  - Supported transform lengths per PQC standard per radix configuration
  - Unified butterfly operation counts (radix-2, 3, 4, 5)
  - Memory access patterns (conflict-free verification)
  - Cycle count estimates per standard
  - Prime coverage: which PQC primes supported per configuration
- CSV: `36_transform_lengths.csv`, `36_butterfly_ops.csv`, `36_memory_mapping.csv`, `36_pqc_coverage.csv`, `36_cycle_counts.csv`
- PNG: `36_radix_decomposition.png`, `36_butterfly_structure.png`, `36_memory_conflicts.png`, `36_pqc_support_matrix.png`, `36_performance_comparison.png`
- Markdown: `experiment-36-ntt-pqc-base12-base60.md`

### Controls (from PLAN.md)
- **Same quantity**: All PQC standards tested with equal thoroughness across radix configurations
- **Exact arithmetic**: All NTT arithmetic uses exact modular operations (no floating point)
- **Independent verification**: Cross-check primitive roots and transform lengths with PQC standard specifications (FIPS 203, 204, 205); verify butterfly correctness with Lee et al. 2026
- **Equal conditions**: Same architectural constraints (unified datapath, on-chip memory) for all configurations
- **Negative results**: Report PQC standards not supported by base-12/60 radices; report transform lengths requiring unsupported radices

### Success Criteria
- Demonstrate base-60 radices {2,3,4,5} cover ALL transform lengths required by ML-KEM, ML-DSA, Falcon, HAETAE, Dilithium
- Design unified butterfly supporting radix-2, 3, 4, 5 with conflict-free memory mapping
- Show base-60 configuration requires fewer total butterflies than binary-only for mixed-radix transform lengths
- Verify exact modular arithmetic produces bit-exact NTT results matching PQC reference implementations

---

## Summary: Module Reference Map

| Experiment | Primary Modules | Secondary Modules |
|------------|-----------------|-------------------|
| 32: MR-OTP | numerals, core.rational, modular | metrics, sequences |
| 33: MrRoPE | numerals, frequency, angles, core.rational | trigonometry, metrics |
| 34: RNS/MRUD | modular, numerals, core.rational | metrics, sequences |
| 35: CORDIC | trigonometry, numerals, core.rational | angles, metrics |
| 36: NTT/PQC | fft_benchmarks, modular, core.rational | numerals, metrics |

---

## Implementation Priority

1. **Experiment 32 (MR-OTP)** — Highest impact: only implementation of Buono 2026 MR-OTP with base-12/60; direct cryptographic application with perfect secrecy proof
2. **Experiment 36 (NTT/PQC)** — Critical for post-quantum crypto: unified accelerator for all 5 major PQC standards; base-60 radices cover all required NTT lengths
3. **Experiment 33 (MrRoPE)** — Strong ML relevance: ICLR 2026 oral paper adaptation to base-12/60; long-context positioning
4. **Experiment 34 (RNS/MRUD)** — Hardware foundation: optimal moduli sets + carry-free arithmetic for base-12/60 ALU design
5. **Experiment 35 (CORDIC)** — Transcendental functions: zero-DSP FPGA implementation; base-60 natural angle representation

---

Each experiment uses only exact rational arithmetic internally (`base60lab.core.rational.Rational`), with base conversion only for output/display, following the established protocol across all 16+ existing experiments.