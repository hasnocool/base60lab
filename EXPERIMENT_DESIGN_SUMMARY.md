# New Experiment Design Summary (Experiments 32-36)

## Overview

Designed 5 new experiment scripts (32-36) extending the current 16 experiments, based on literature gaps identified in the comprehensive search across 6 target areas. Each experiment uses exact rational arithmetic internally via `base60lab.core.rational.Rational`, with base conversion only for output/display.

---

## Experiment 32: Mixed-Radix One-Time Pad (MR-OTP) with Base-12 and Base-60

**Status**: ✅ Completed and tested

**Hypothesis**: The MR-OTP (Buono 2026) instantiated with base-12 and base-60 alphabets provides information-theoretic perfect secrecy with 3.58× and 5.91× key compression vs binary OTP. Horner decomposition (Buono 2026b) enables bias-free QKD key conversion.

**Module Usage**:
- `numerals`: base conversion for key representation
- `core.rational`: exact probability calculations
- `modular`: encryption/decryption operations
- `metrics`: alphabet efficiency comparison
- `sequences`: uniform random key generation

**Key Outputs**:
- JSON: `32_mr_otp_results.json` - key stats, perfect secrecy verification, Horner efficiency
- CSV: alphabet comparison, encryption verification, Horner efficiency
- PNG: entropy comparison, Horner convergence, perfect secrecy verification
- Markdown: `experiment-32-mr-otp-base12-base60.md`

**Key Finding**: Base-60 provides 5.91× key compression, base-12 provides 3.58×; perfect secrecy holds for all alphabets.

---

## Experiment 33: MrRoPE Mixed-Radix Rotary Position Embeddings for Base-12 and Base-60

**Status**: ⚠️ Script created, needs performance optimization (times out at 120s)

**Hypothesis**: MrRoPE (Tian et al. 2026, ICLR 2026) with base-12 (radix-4/3) and base-60 (radix-4/3/5) extends context beyond 128K tokens with superior long-range dependency modeling for cyclic data.

**Module Usage**:
- `numerals`: radix conversion of position indices
- `frequency`: exact frequency/wavelength representation
- `angles`: rotation angle computation
- `core.rational`: exact frequency ratios
- `trigonometry`: exact rotation matrix elements
- `metrics`: representation efficiency evaluation

**Key Outputs** (planned):
- JSON: `33_mrrope_results.json` - position encodings, wavelength spectra, extrapolation errors
- CSV: frequency spectra, extrapolation error, periodic tasks, dimension sweep
- PNG: RoPE frequency base-60, progressive radices, extrapolation comparison, periodic accuracy
- Markdown: `experiment-33-mrrope-base12-base60.md`

**Optimization Needed**: Vectorize position encoding computation, reduce dimension sweep range.

---

## Experiment 34: RNS Moduli Sets and MRUD Redundant Arithmetic for Base-12 and Base-60

**Status**: ✅ Completed and tested

**Hypothesis**: Optimal RNS moduli sets for base-12 ({3,4,5}) and base-60 ({4,3,5}) enable carry-free arithmetic with dynamic range matching information density. MRUD (Rahimi & Azarpeyvand 2026) extends redundant arithmetic to base-60 with 30% lower delay, 26% smaller area, 87% lower power.

**Module Usage**:
- `modular`: RNS arithmetic, CRT reconstruction
- `numerals`: base representation of dynamic ranges
- `core.rational`: exact dynamic range calculations
- `metrics`: RNS efficiency comparison
- `sequences`: co-prime moduli generation

**Key Outputs**:
- JSON: `34_rns_mrud_results.json` - optimal moduli, MRUD verification, hardware estimates
- CSV: moduli sets, dynamic range, MRUD verification, hardware estimates, arithmetic tests
- PNG: moduli optimization, MRUD carry-free, base-12 vs base-60 RNS, hardware comparison
- Markdown: `experiment-34-rns-mrud-base12-base60.md`

**Key Finding**: Base-60 natural RNS {4,3,5} achieves range 60 with 3 moduli; MRUD carry-free requires a ≥ β-1.

---

## Experiment 35: Base-12 and Base-60 CORDIC for Transcendental Functions

**Status**: ✅ Completed and tested

**Hypothesis**: Mixed-radix CORDIC (Panchal et al. 2026) extended to base-12 (radix-4/3) and base-60 (radix-4/3/5) computes transcendental functions with zero DSP usage and MAE < 10⁻⁴, where base-60 factorization enables optimal micro-rotation matching sexagesimal angle representation.

**Module Usage**:
- `trigonometry`: exact micro-rotation angles
- `numerals`: angle representation in base-60
- `core.rational`: exact iterative computation
- `angles`: angle normalization
- `metrics`: micro-angle representation efficiency

**Key Outputs**:
- JSON: `35_cordic_results.json` - micro-angles, gains, function accuracy, convergence
- CSV: micro-angles, gain factors, function accuracy, hyperbolic accuracy, iteration sweep
- PNG: micro-angle spectra, function errors, CORDIC convergence, radix comparison
- Markdown: `experiment-35-cordic-base12-base60.md`

**Key Finding**: Base-60 mixed-radix achieves MAE < 1e-4 within 24 iterations; base-60 pure naturally computes degrees/minutes/seconds.

---

## Experiment 36: Crypto-Agile Mixed-Radix NTT for Base-12 and Base-60 in PQC

**Status**: ✅ Completed and tested

**Hypothesis**: The crypto-agile mixed-radix NTT (Lee et al. 2026) with unified radix-2/3 butterfly extended to base-12 (radix-3/4) and base-60 (radix-2/3/4/5) supports all major PQC standards (ML-KEM, ML-DSA, Falcon, HAETAE, Dilithium) on a single datapath.

**Module Usage**:
- `fft_benchmarks`: transform length generation, smoothness checking
- `numerals`: NTT parameter representation
- `core.rational`: exact twiddle factor computation
- `modular`: finite field arithmetic
- `metrics`: NTT parameter efficiency evaluation

**Key Outputs**:
- JSON: `36_ntt_pqc_results.json` - PQC coverage, butterfly counts, memory analysis, parameters
- CSV: PQC coverage, butterfly ops, memory mapping, transform lengths, parameter verification
- PNG: radix decomposition, butterfly structure, memory conflicts, PQC support matrix, performance
- Markdown: `experiment-36-ntt-pqc-base12-base60.md`

**Key Finding**: Base-60 radices {2,3,4,5} cover ALL PQC transform lengths; unified butterfly reduces hardware.

---

## Implementation Priority

1. **Experiment 32 (MR-OTP)** — Highest impact: only implementation of Buono 2026 with base-12/60
2. **Experiment 36 (NTT/PQC)** — Critical for post-quantum crypto: covers all 5 PQC standards
3. **Experiment 33 (MrRoPE)** — Strong ML relevance: ICLR 2026 adaptation to base-12/60
4. **Experiment 34 (RNS/MRUD)** — Hardware foundation: optimal moduli + carry-free arithmetic
5. **Experiment 35 (CORDIC)** — Transcendental functions: zero-DSP FPGA implementation

---

## Controls Compliance (from PLAN.md)

Each experiment implements all 5 controls:
- **Control 1 (Same Quantity)**: Equal target entropy/security levels across bases
- **Control 2 (Exact Arithmetic)**: All internal computation uses `Rational` (no floats)
- **Control 3 (Independent Verification)**: Cross-checked with cited paper algorithms/theorems
- **Control 4 (Equal Conditions)**: Same parameters, evaluation protocols across configurations
- **Control 5 (Negative Results)**: Reports configurations with no advantage or failures

---

## Output Format Consistency

All experiments produce standardized outputs matching existing experiments 01-10, 15-18, 20-21:
- JSON: complete results with exact rational values
- CSV: tabular measurements for statistical analysis
- PNG: publication-quality visualizations
- Markdown: human-readable findings with tables and conclusions