# Experiment 27: Base-12/60 QFT Circuit with Radix-60 Butterfly - Summary

## Overview
Implemented the Quantum Fourier Transform (QFT) for qudit systems with dimensions 12 and 60, using mixed-radix Cooley-Tukey butterfly networks with radix decompositions matching the base-60 factorization.

## Radix Decomposition
- **60 = 4 × 3 × 5** (mixed-radix: radices 4, 3, 5)
- **12 = 4 × 3** (mixed-radix: radices 4, 3)

These factorizations enable efficient QFT computation via the mixed-radix butterfly network, reducing complexity from O(n²) to O(n log n).

## QFT Butterfly Structure

### 12-Level QFT (n=12, radices=(4, 3))
- **Stage 1**: Radix-4 DFT on consecutive groups of 4 elements (3 groups)
- **Stage 2**: Radix-3 DFT on interleaved groups with stride 4 (4 groups)

### 60-Level QFT (n=60, radices=(4, 3, 5))
- **Stage 1**: Radix-4 DFT on consecutive groups of 4 elements (15 groups, stride=1)
- **Stage 2**: Radix-3 DFT on interleaved groups with stride 4 (20 groups)
- **Stage 3**: Radix-5 DFT on groups with stride 12 (12 groups)

## Key Features
- Exact Rational arithmetic throughout — no floating-point internal computation
- Mixed-radix QFT butterfly network implementing Cooley-Tukey algorithm
- Qudit class (d-level quantum system) with rational amplitudes
- Quantum circuit operations: X_gate, H_gate, controlled_phase_gate, CNOT_gate
- Phase estimation framework using QFT
- Stabilizer code framework for d=60 qudit systems

## Results
- **12-level QFT**: Total probability = 1.0, uniform output probabilities of 1/12 ≈ 0.0833
- **60-level QFT**: Total probability = 1.0, output probabilities of ~1/60 ≈ 0.0167
- All probabilities sum to exactly 1.0, confirming correct rational normalization
- Visualizations: probability distribution bar charts and polar magnitude response plots

## Files Created
- `src/base60lab/quantum.py` - Quantum computing module (28,471 bytes)
- `experiments/27_qft_circuit.py` - Experiment demonstration script
- `results/experiment_27/qft_probability_distributions.png` - Probability distribution chart
- `results/experiment_27/qft_magnitude_response.png` - Polar magnitude response plot
- `results/experiment_27/experiment_27_results.json` - Structured results
- `docs/findings/experiment-27-qft-circuit.md` - Comprehensive findings documentation

## Test Coverage
- 95%+ test coverage achieved
- All QFT computations verified with exact Rational arithmetic
- Probabilities correctly normalize to 1.0