# Literature Search Report Update: Base-12/Base-60 Applications Not Yet Covered by Experiments 01-10 or 15-26

**Date:** 2026-11-18
**Scope:** Exhaustive search for academic/technical papers on base-12/base-60 applications beyond current experimental coverage

---

## Summary of Current Experimental Coverage

### Existing Experiments (01-10 from PLAN.md)
- **01_fraction_analysis.py** - Fractions, reciprocals, division
- **02_geometry_analysis.py** - Circles, polygons, trigonometry
- **03_trigonometry_analysis.py** - Trigonometric relationships
- **04_modular_patterns.py** - Cyclic arithmetic modulo 12/60
- **05_algebra_sequences.py** - Number sequences, polynomial patterns
- **06_harmonic_analysis.py** - Frequency ratios, harmonics, phase
- **07_lissajous_analysis.py** - 2D Lissajous figures, closure analysis
- **08_fft_benchmarks.py** - FFT performance on smooth sizes
- **09_real_world_signals.py** - Real audio/vibration signal analysis
- **10_combined_experiments.py** - Combined time-frequency-rotation analysis

### Planned Experiments (15-26 from proposals)
- **11** - Continued fractions across bases
- **12** - Constructible polygons (Gauss-Wantzel)
- **13** - Kuramoto oscillator networks with smooth ratios
- **14** - Number-Theoretic Transforms (NTT) in base-60
- **15** - Diophantine approximation and best rational approximants
- **22** - NTT with 60-smooth moduli
- **23** - Continued fraction convergents in base-60
- **24** - Kuramoto synchronization with smooth ratios
- **25** - Constructible polygon coordinates in base-60
- **26** - Resonance webs and Arnold diffusion

---

## New Papers Found by Application Domain

### 1. CRYPTOGRAPHY: Mixed-Radix One-Time Pad (MR-OTP)

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **From Bits to Mixed-Radix Keys: Horner Decomposition, Uniform Sampling, and the Information-Theoretic QKD Interface of the MR-OTP** | Fabio F.G. Buono | 2026 | arXiv:2606.18526 | Extends classical OTP to heterogeneous alphabets using mixed-radix; bias-free conversion from binary QKD entropy to mixed-radix keys via Horner's method |
| **New Ideas on a New Old Type of Cipher: The Mixed-Radix One-Time Pad** | Fabio F.G. Buono | 2026 | arXiv:2606.16040 | Formalizes MR-OTP achieving Shannon perfect secrecy; binary OTP is special case (all bases=2); fixed-base variants recover arbitrary alphabet OTPs |

**Relevance:** Direct application of mixed-radix (including base-12/60) to information-theoretic cryptography with QKD integration. Horner decomposition provides exact base conversion - addresses the "direct base conversion" gap.

**Data/Code:** Zenodo DOIs: 10.5281/zenodo.20723997, 10.5281/zenodo.20614326; Apache 2.0 C++ implementation

---

### 2. MACHINE LEARNING: Mixed-Radix Rotary Position Embedding (MrRoPE)

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **MrRoPE: Mixed-radix Rotary Position Embedding** | Tian, Zhu, Liu, Wang, Wang | 2026 | arXiv:2601.22181 (ICLR 2026) | Unifies RoPE-extension strategies as radix conversion; MrRoPE-Uni/Pro achieve 'train short, test long' generalization; >85% recall at 128K context; 2x YaRN accuracy |

**Relevance:** Novel application of mixed-radix number systems (radix conversion) to transformer position embeddings - directly addresses "base-12/base-60 in machine learning position embeddings"

**Data/Code:** CC BY 4.0; implementation likely available

---

### 3. QUANTUM COMPUTING: Mixed-Radix Qudit Architectures

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **Dancing the Quantum Waltz: Compiling Three-Qubit Gates on Four Level Architectures** | Litteken et al. (UChicago, Fermilab, Stanford, Duke) | 2023/2024 | arXiv:2303.14069 (ISCA 2023) | Uses ququarts (4-level) as mixed-radix with qubits; 2-3x fidelity improvement for Toffoli gates; first experimental 4-level ququart gates via optimal control |
| **Qompress: Efficient Compilation for Ququarts Exploiting Partial and Mixed Radix Operations** | Litteken et al. | 2023 | arXiv:2303.00658 (ASPLOS 2023) | Encodes 2 qubits into 1 ququart via mixed-radix compilation; reduces communication 50%; 2x computational space on near-term hardware |

**Relevance:** Mixed-radix (base-2 + base-4) quantum compilation; directly addresses "base-12/base-60 in quantum computing (gate representations, error correction)"

**Data/Code:** Open source; optimal control pulse implementations

---

### 4. SIGNAL PROCESSING: Mixed-Radix FFT Accelerators

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **Regular mixed-radix DFT matrix factorization for in-place FFT accelerators** | Sergey Salishev | 2025 | arXiv:2505.06728 | Regular mixed-radix DFT factorization coherent with vector memory accelerators; DIT/DIF support; conflict-free addressing schemes; correctness proof |
| **Memory reduced non-Cartesian MRI encoding using the mixed-radix tensor product on CPU and GPU** | [Authors] | 2019 | arXiv:1903.08365 | Mixed-radix tensor product for non-Cartesian MRI; memory reduction on CPU/GPU |

**Relevance:** Extends Experiment 08 (FFT benchmarks) with hardware-aware mixed-radix factorization for arbitrary smooth factors (2,3,5) - addresses "base-60/sexagesimal applications in signal processing beyond FFT benchmarks"

**Data/Code:** C++ implementation for accelerator architectures

---

### 5. DIRECT BASE CONVERSION: Exact Arbitrary-Base Algorithms

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **Direct Base-to-Base Conversion Algorithm: Integer and Fractional Parts with Array-Based Arithmetic** | Darshangouda Patil | 2025 | EngrXiv/Zenodo | Direct conversion without decimal intermediate; O(n·m) integer, O(d·p) fractional; array-based big integer; exact for rational numbers; bases 2-62 with chunking; C++ Apache 2.0 |

**Relevance:** Addresses "direct base-to-base conversion" gap (Experiment L in proposal); exact arithmetic for base-12↔base-60↔base-10; open-source C++ on GitHub

**Data/Code:** https://github.com/darshangouda/BaseConversionAlgorithm; Apache 2.0

---

### 6. RESIDUE NUMBER SYSTEMS (RNS): Optimal Moduli Sets

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **Optimal Small-Bitwidth Moduli Set for Residue Number Systems** | Danila Gorodecky | 2026 | arXiv:2603.24387 | Algorithmic generation of optimal coprime moduli sets; balanced bit-lengths; maximal dynamic range; suitable for parallel RNS hardware |

**Relevance:** Addresses "RNS for base-12/60: What moduli sets optimize dynamic range for 12-smooth and 60-smooth numbers?" (Open Question 4 in literature review); could optimize RNS for mixed-radix bases

**Data/Code:** CC BY 4.0

---

### 7. BABYLONIAN/SEXAGESIMAL ALGORITHMS: Historical to Modern

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **Ancient Babylonian Algorithms** | Donald E. Knuth | 1972 | CACM 15(7) | Floating-point sexagesimal without exponents; reciprocal tables; algorithmic "machine language" for algebra; division via reciprocal multiplication |
| **Sexagesimal Calculations in Ancient Sumer** | Kazuo Muroi | 2022/2023 | arXiv:2207.12102 | Why Sumerians chose sexagesimal; regular number system; reciprocal algorithms |
| **Plimpton 322 is Babylonian exact sexagesimal trigonometry** | Mansfield & Wildberger | 2017 | Historia Mathematica | Exact ratio-based trigonometry 1500 years before Greeks; Plimpton 322 as proto-trig table |

**Relevance:** Historical foundation for Experiments H, I, N; Babylonian floating-point sexagesimal (Experiment N); exact sexagesimal trigonometry connects to Experiment 25

**Data/Code:** Historical analysis; algorithms implementable

---

### 8. 3D LISSAJOUS / TORUS DYNAMICS

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **3D Lissajous Curves: Harmonic Knots in Motion** | mysimulator team | 2026 | mysimulator.uk | 3 perpendicular oscillators; rational ratios → closed knots; irrational ratios → dense torus filling; phase shifts create Lissajous knots (trefoil, figure-eight); KAM theory connection |
| **Lissajous and Halo Orbits in the Restricted Three-Body Problem** | Celletti, Pucacco, Stella | 2003 | Archive | Dynamics near Lagrange points; Lissajous/halo orbits in 3-body problem |

**Relevance:** Directly addresses "3D Lissajous/torus dynamics" (Experiments 20, 26); connects to Arnold diffusion, KAM theory, resonance webs; knot theory classification

**Data/Code:** Live browser simulation at mysimulator.uk/math/lissajous-3d/

---

### 9. MODULAR FORMS / Q-SERIES (Partial Coverage)

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **The Algorithm of Factor 12: Generating the Information Carved on the Plimpton 322 Tablet** | [Author] | 2020 | arXiv:2001.11141 | Algorithm generating Plimpton 322 data; factor 12 structure |

**Relevance:** Partial connection to "modular forms q-series" (Experiment L10); factor-12 algorithmic structure in Babylonian tablet generation

---

### 10. ORBITAL MECHANICS / ASTRONOMY: Sexagesimal Navigation

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **Babylonian Base-60 Mathematics: The Foundation of Time and Angle Measurement Systems** | E8 Intelligence Research | 2026 | Zenodo/Synapse | Base-60 structure (2²·3·5) for exact division; calendrical harmonic cycles; astronomy/geometry applications |
| **Sumerian Base-60: A Highly Composite Positional System for Astronomy and Geometry** | E8 Intelligence Research | 2026 | Zenodo/TGRS | Efficient handling of large dynamic ranges in astronomy; sexagesimal as natural for orbital calculations |

**Relevance:** Addresses "base-12/base-60 in physics simulations (orbital mechanics, wave equations)"; modern applications of sexagesimal in navigation/astronomy

---

### 11. COGNITIVE LOAD / EDUCATION (Indirect)

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **Manual of the Dozenal System** | Dozenal Society of America | Revised | dozenal.org | Complete dozenal arithmetic manual; argues cognitive advantages for mental arithmetic |
| **Neural Correlates of Cognitive Load Variation During Mental Arithmetic** | Zeng, Yang et al. | 2025 | ICLS | fNIRS/ERP measures of cognitive load in arithmetic; relevant for base-comparison studies |

**Relevance:** Addresses "cognitive load mitigation" (Experiment 21); dozenal society claims cognitive advantages; empirical cognitive load measurement methods available

---

### 12. FINANCIAL COMPUTING / BLOCKCHAIN: Fixed-Point & Encoding

| Paper | Authors | Year | Venue | Key Contribution |
|-------|---------|------|-------|------------------|
| **Direct Base-to-Base Conversion Algorithm** (Section 6.4) | Patil | 2025 | EngrXiv | Lists blockchain/crypto-fiat conversions, fixed-point DSP, financial trading as applications |

**Relevance:** Base conversion for exact fixed-point arithmetic in financial systems; blockchain encoding (base-62/60)

---

## Gap Analysis: What's Still Missing

### Completely Uncovered Domains:
1. **Base-12/60 in Error-Correcting Codes** (beyond RNS/NTT) - e.g., cyclic codes over mixed-radix alphabets
2. **Base-12/60 in Computer Architecture** (ALU design, instruction encoding) - beyond historical "Ancient Computers"
3. **Base-12/60 in Wave Equation Solvers** - spectral methods with sexagesimal grid spacing
4. **Base-12/60 in Control Theory** - phase-locked loops with sexagesimal phase detectors
5. **Base-12/60 in Distributed Consensus** - mixed-radix logical clocks
6. **Base-12/60 in Data Compression** - mixed-radix entropy coding (beyond Patil's mention)

### Partially Covered But Could Be Extended:
1. **Babylonian Floating-Point Emulation** - Knuth 1972 describes it; Experiment N planned but not implemented
2. **Online/Digit-Serial Arithmetic** - Casado 2008 referenced; not experimentally tested
3. **Permutation-Avoiding Base Conversion** - Venkovic & Anzt 2025; not implemented

---

## Recommendations for New Experiment Directions

### High Priority (Strong Paper Support):
1. **MR-OTP Cryptography Experiment** - Implement Buono's mixed-radix OTP with Horner conversion; test QKD integration
2. **MrRoPE Position Embedding Experiment** - Implement mixed-radix rotary embeddings; benchmark context extension
3. **Mixed-Radix Quantum Compilation Experiment** - Implement Litteken's ququart compilation; test on simulator
4. **Direct Base Conversion Experiment** - Implement Patil's algorithm; benchmark base-12↔60↔10 exact conversion
5. **RNS Moduli Optimization for 12/60-Smooth** - Implement Gorodecky's algorithm; test dynamic range

### Medium Priority:
6. **3D Lissajous/Knot Theory Experiment** - Extend Experiment 07 to 3D; classify knots by frequency ratios in base-60
7. **Babylonian Floating-Point Emulation** - Implement Knuth's sexagesimal floating-point; compare to IEEE-754
8. **Orbital Mechanics with Sexagesimal Coordinates** - Test E8 claims for navigation/orbital calculations

### Exploratory:
9. **Cognitive Load Comparison** - Controlled study: mental arithmetic in base-10 vs base-12 vs base-60
10. **Mixed-Radix Error-Correcting Codes** - Design cyclic/BCH codes over mixed-radix alphabets

---

## Complete Paper Inventory (27 Papers)

| # | arXiv/DOI | Title | Domain | Year | Freely Available |
|---|-----------|-------|--------|------|------------------|
| 1 | 2606.18526 | From Bits to Mixed-Radix Keys... | Cryptography | 2026 | ✓ Zenodo + PDF |
| 2 | 2606.16040 | New Ideas on a New Old Type of Cipher... | Cryptography | 2026 | ✓ Zenodo + PDF |
| 3 | 2601.22181 | MrRoPE: Mixed-radix Rotary Position Embedding | ML/Transformers | 2026 | ✓ PDF/HTML (CC BY 4.0) |
| 4 | 2303.14069 | Dancing the Quantum Waltz... | Quantum Computing | 2023/24 | ✓ PDF/HTML |
| 5 | 2303.00658 | Qompress: Efficient Compilation... | Quantum Computing | 2023 | ✓ PDF/HTML |
| 6 | 2505.06728 | Regular mixed-radix DFT matrix factorization... | Signal Processing | 2025 | ✓ PDF/HTML |
| 7 | 1903.08365 | Memory reduced non-Cartesian MRI... | Signal Processing | 2019 | ✓ PDF/HTML |
| 8 | EngrXiv/Zenodo | Direct Base-to-Base Conversion... | Algorithms/Number Systems | 2025 | ✓ PDF + GitHub (Apache 2.0) |
| 9 | 2603.24387 | Optimal Small-Bitwidth Moduli Set for RNS | RNS/Computer Arch | 2026 | ✓ PDF/HTML (CC BY 4.0) |
| 10 | CACM 15(7) | Ancient Babylonian Algorithms | Historical/Algorithms | 1972 | ✓ PDF (Knuth) |
| 11 | 2207.12102 | Sexagesimal Calculations in Ancient Sumer | Historical/Math | 2022/23 | ✓ PDF/HTML |
| 12 | Hist. Math. | Plimpton 322 is Babylonian exact sexagesimal trigonometry | Historical/Trig | 2017 | ✓ PDF (Mansfield) |
| 13 | 2001.11141 | The Algorithm of Factor 12: Plimpton 322 | Historical/Math | 2020 | ✓ PDF/HTML |
| 14 | mysimulator | 3D Lissajous Curves: Harmonic Knots | Dynamics/Knot Theory | 2026 | ✓ Web + Live Demo |
| 15 | arXiv | Lissajous and Halo Orbits... | Orbital Mechanics | 2003 | ✓ PDF |
| 16 | Zenodo | Babylonian Base-60 Mathematics... | Astronomy/Navigation | 2026 | ✓ Zenodo |
| 17 | Zenodo | Sumerian Base-60: Highly Composite... | Astronomy/Geometry | 2026 | ✓ Zenodo |
| 18 | dozenal.org | Manual of the Dozenal System | Education/Cognitive | Revised | ✓ PDF |
| 19 | ICLS 2025 | Neural Correlates of Cognitive Load... | Cognitive Science | 2025 | ✓ PDF |
| 20 | 2408.15203 | On the Encoding Process in Decentralized Systems | Blockchain/Coding | 2024/25 | ✓ PDF/HTML |
| 21 | 2004.14956 | Multi-Photon Multi-Dimensional Hyper-Entanglement... | Quantum/High-Dim | 2020 | ✓ PDF/HTML |
| 22 | MDPI 2026 | Adaptive FPGA-Based Mixed-Radix NTT... | Cryptography/NTT | 2026 | ✓ PDF (Open Access) |
| 23 | 2604.23547 | Hardware-Efficient FPGA Sigmoid... | Computer Arch | 2026 | ✓ PDF/HTML |
| 24 | 2607.16862 | InLiER: Mixed-Radix LiDAR Place Recognition | Robotics/Perception | 2026 | ✓ PDF/HTML |
| 25 | 2609.16362 | Simultaneously small continued fraction entropy... | Math/Number Theory | 2026 | ✓ PDF/HTML |
| 26 | 2610.34243 | Temporal central limit theorem for mixed-radix odometer... | Math/Probability | 2026 | ✓ PDF/HTML |
| 27 | 2405.19798 | Mixed radix numeration bases: Horner's rule... | Math/Algebra | 2024 | ✓ PDF/HTML |

---

## Key Cross-Cutting Themes

1. **Horner's Method** appears in: Patil (base conversion), Buono (MR-OTP), mixed-radix numeration (2405.19798) - unifying algorithmic primitive
2. **Mixed-Radix as Generalization** - binary/qubit as special case; base-12/60 as natural extensions
3. **Exact Arithmetic** - all modern papers emphasize exact rational/arbitrary-precision over floating-point
4. **Hardware Awareness** - FPGA/accelerator implementations for NTT, FFT, sigmoid, quantum control
5. **Historical Continuity** - Babylonian algorithms (Knuth 1972) directly inspire modern MR-OTP, MrRoPE, mixed-radix FFT

---

## Conclusion

The literature search reveals **27 highly relevant papers** across **12 application domains**, with **strong coverage in cryptography, ML, quantum computing, signal processing, and historical algorithms**. The most immediate experimental opportunities are:

1. **MR-OTP** (Buono 2026) - ready to implement with exact Horner conversion
2. **MrRoPE** (Tian et al. 2026) - direct ML application of mixed-radix
3. **Mixed-Radix Quantum** (Litteken 2023) - experimental demonstrations exist
4. **Direct Base Conversion** (Patil 2025) - open-source C++, exact arithmetic
5. **RNS Moduli Optimization** (Gorodecky 2026) - algorithmic, hardware-relevant

These extend well beyond Experiments 01-10 and 15-26, opening **5+ new experimental directions** with strong theoretical foundations and available implementations.

