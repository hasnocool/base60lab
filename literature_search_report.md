# Base-12/Base-60 Literature Search Report
## Academic/Technical Papers for New Experiment Directions

**Repository:** Base60Research  
**Existing Experiments Covered (01-10, 15-21):** Fraction analysis, geometry/trigonometry, modular patterns, algebra/sequences, harmonic analysis, Lissajous figures, FFT benchmarks (12/60-smooth), real-world signals, combined experiments, Babylonian reciprocals, smooth FFT prediction, direct base conversion, modular forms q-series, 3D Lissajous/torus dynamics, cognitive load mitigation.

**Target Areas for NEW Papers (NOT covered by existing experiments):**
1. Base-12/duodecimal in cryptography (beyond NTT)
2. Base-60/sexagesimal in signal processing (beyond FFT benchmarks)
3. Base-12/base-60 in physics simulations (orbital mechanics, wave equations)
4. Base-12/base-60 in ML (position embeddings, weight representations)
5. Base-12/base-60 in quantum computing (gate representations, error correction)
6. Mixed-radix number systems in computer architecture
7. Any other novel base-12/base-60 applications

---

## PAPERS FOUND

### 1. Base-12/Duodecimal in Cryptography

| # | Title | Authors | Year | arXiv ID | Abstract Summary | Relevance to Target Area | Code Availability |
|---|-------|---------|------|----------|------------------|-------------------------|-------------------|
| 1 | **Encryption by using base-n systems with many characters** | Armin Hoenen | 2023 | 2306.02378 | General base-n framework for encryption using Unicode character digit sets; demonstrates base conversion as encryption mimicking encoding errors/noise; notes base switching doesn't guarantee compression | **Target #1**: General base-n cryptography framework; mentions hexadecimal but NOT base-12/60 specifically | PDF, HTML, TeX source available |
| 2 | **Base Encryption: Dynamic algorithms, Keys, and Symbol Set** | Po-Han Lin | 2000 | cs/0007028 | Novel encryption using base conversion, symbol remapping, dynamic algorithms; claims immunity to plaintext/brute-force attacks; plug-and-play cipher engine | **Target #1**: Foundational base-conversion cryptography; dynamic algorithms using arbitrary bases | No PDF; other formats available |
| 3 | **New Ideas on a New Old Type of Cipher: The Mixed-Radix One-Time Pad** | Fabio F.G. Buono | 2026 | 2606.16040 | Generalizes OTP to heterogeneous alphabets (Mixed-Radix OTP); proves Shannon perfect secrecy; classical binary OTP is special case; fixed-base variants recover OTPs over arbitrary alphabets | **Target #1**: **Directly relevant** - mixed-radix OTP with base-12/60 as special cases; only paper explicitly addressing mixed-radix (base-12) in cryptography | PDF, HTML available |
| 4 | **From Bits to Mixed-Radix Keys: Horner Decomposition, Uniform Sampling, and the Information-Theoretic QKD Interface of the MR-OTP** | Fabio F.G. Buono | 2026 | 2606.18526 | Practical bias-free conversion of QKD binary entropy to uniform mixed-radix keys via Horner's method; rejection sampling for uniformity; end-to-end IT security for QKD pipelines | **Target #1 + #5**: QKD interface for mixed-radix keys; base-12/60 key generation from quantum sources | PDF, HTML available |
| 5 | **Cryptographic transformations over polyadic rings** | Steven Duplij, Qiang Guo, Na Fu | 2025/2026 | 2512.12580 | General algebraic framework; could include base-12/60 as special cases but not targeted | **Target #1**: Polyadic rings generalization; base-12/60 could be instantiations | Not specified |
| 6 | **Binary-ternary collisions and the last significant digit of n! in base 12** | Deshouillers, Jelinek, Spiegelhofer | 2024 | 2412.09124 | Proves every integer 1-11 appears as last nonzero digit of n! in base 12 infinitely often; asymptotic densities for digits | **Target #1 (indirect)**: Pure number theory on base-12 factorial digits; could inform base-12 cryptographic properties | PDF, HTML, TeX available |

**GAP ASSESSMENT:** Only 1 paper (Buono 2026) directly addresses mixed-radix/base-12 cryptography. **Significant gap** for base-12/60 specific cryptographic applications beyond general base-n frameworks.

---

### 2. Base-60/Sexagesimal in Signal Processing (Beyond FFT Benchmarks)

| # | Title | Authors | Year | arXiv ID | Abstract Summary | Relevance to Target Area | Code Availability |
|---|-------|---------|------|----------|------------------|-------------------------|-------------------|
| 1 | **Regular mixed-radix DFT matrix factorization for in-place FFT accelerators** | Sergey Salishev | 2025 | 2505.06728 | Generic vector memory-based accelerator for DIT/DIF FFT; regular mixed-radix DFT factorization coherent with architecture; radices 2,3,4,5,6,8,10,12 | **Target #2 + #6**: Mixed-radix FFT accelerator design; radix-12 (base-12) explicitly included; extensible to base-60 via 2×3×5 | HTML (experimental); code may be available |
| 2 | **Residue Number System Comparison Revisited, a Software Perspective** | Didier, El Mrabet | 2026 | 2605.18415 | Software perspective on RNS; base extension operations; converting RNS between bases including base-12/60; residue computation | **Target #2 + #6**: RNS base conversion directly relevant; base-60 = {2²,3,5} moduli sets; software implementation guidance | PDF available; may have software tools |
| 3 | **Analog Fast Fourier Transforms for Scalable and Efficient Signal Processing** | Xiao, Feinberg, et al. | 2024/2026 | 2409.19071 | Scalable analog FFT computing 65,536-point DFT; >500× larger than previous analog systems | **Target #2**: Large-scale FFT techniques adaptable to base-60 frequency analysis | v3 HTML; some author implementations |
| 4 | **Fast Compressed-Domain N-Point DFT: The "Twiddless" FFT Algorithm** | Saulo Queiroz | 2025 | 2505.23718 | Twiddless FFT eliminating twiddle factors; reduced computational overhead | **Target #2**: Algorithmic improvement for FFT; could combine with base-60 mixed-radix | v2 HTML; may have implementation |
| 5 | **MrRoPE: Mixed-radix Rotary Position Embedding** | Tian, Zhu, Liu, Wang, Wang | 2026 | 2601.22181 | Treats RoPE as β-radix (mixed-base) encoding; progressive radix conversion (MrRoPE-Pro); unifies NTK, YaRN; ICLR 2026 oral | **Target #2 + #4**: Theoretical foundation for mixed-radix position encodings adaptable to base-60 frequency grids | ICLR 2026 accepted; GitHub expected |

**GAP ASSESSMENT:** No papers on base-60 filter design, wavelet transforms, or spectral analysis specific to sexagesimal representations. **Significant gap** for signal processing applications beyond FFT.

---

### 3. Base-12/Base-60 in Physics Simulations

| # | Title | Authors | Year | arXiv ID | Abstract Summary | Relevance to Target Area | Code Availability |
|---|-------|---------|------|----------|------------------|-------------------------|-------------------|
| 1 | **Approximations and modifications of celestial dynamics tested on the three-body system** | Søren Toxvaerd | 2025/2026 | 2512.03823 | PM, MOND, Yukawa, MOGA modifications on three-body system; PM/MOND destabilize, Yukawa/MOGA stabilize; momentum conservation issues | **Target #3**: Celestial mechanics with numerical approximations; relevant to physics simulation foundations | Not explicitly stated; involves N-body methods |
| 2 | **Binary-ternary collisions and the last significant digit of n! in base 12** | Deshouillers, Jelinek, Spiegelhofer | 2024 | 2412.09124 | Base-12 factorial digit distributions; every digit 1-11 appears infinitely often | **Target #3 (indirect)**: Pure number theory; could inform base-12 coordinate representations | PDF, HTML, TeX available |

**GAP ASSESSMENT:** **Complete absence** of papers on base-12/base-60 in orbital mechanics, wave equations, numerical relativity, finite element methods, or coordinate systems. Only 1 relevant paper (Toxvaerd) on general celestial mechanics.

---

### 4. Base-12/Base-60 in Machine Learning (Position Embeddings, Weight Representations)

| # | Title | Authors | Year | arXiv ID | Abstract Summary | Relevance to Target Area | Code Availability |
|---|-------|---------|------|----------|------------------|-------------------------|-------------------|
| 1 | **MrRoPE: Mixed-radix Rotary Position Embedding** | Tian, Zhu, Liu, Wang, Wang | 2026 | 2601.22181 | RoPE as β-radix encoding system; MrRoPE-Uni (uniform) and MrRoPE-Pro (progressive) extensions; outperforms YaRN; extends context to 128K+; 85%+ NIAH recall | **Target #4**: **Most relevant** - full theoretical framework for mixed-radix position embeddings; base-12/60 as direct instantiations | ICLR 2026 oral; GitHub implementations expected |
| 2 | **nD-RoPE: A Generalized RoPE for n-Dimensional Position Embedding** | - | 2026 | 2606.12146 | Generalizes RoPE to arbitrary dimensions; evaluated on LLaMA2-7B, Qwen2.5-3B; stable to 128K context | **Target #4**: n-dimensional extension; could incorporate base-12/60 dimension selection | arXiv HTML |
| 3 | **Transformers Can Do Arithmetic with the Right Embeddings** | McLeish et al. | 2024 | 2405.17399 | Position embeddings encoding digit position relative to number start; 99% accuracy on 100-digit addition; enables input injection, recurrent layers | **Target #4**: Position embeddings for arithmetic reasoning; base choice affects performance | PDF, HTML |
| 4 | **Arithmetic in the Wild: Llama uses Base-10 Addition to Reason About Cyclic Concepts** | Feucht et al. | 2026 | 2605.01148 | Empirical study: LLMs use base-10 for cyclic concepts; base choice affects reasoning about cyclic structures | **Target #4**: **Direct evidence** base choice matters for cyclic reasoning; base-12/60 study would be valuable | arXiv HTML; may have analysis code |
| 5 | **Weight Space Representation Learning: A Survey** | - | 2026 | 2603.10090 | Comprehensive survey on weight space learning; foundation for weight representation choices | **Target #4**: Foundation for base-specific weight encodings | arXiv |
| 6 | **any4: Learned 4-bit Numeric Representation for LLMs** | - | 2025 | ICML 2025 | Learned 4-bit representations for LLMs; could extend to base-12/60 | **Target #4**: Learned numeric representations adaptable to base-12/60 | ICML 2025 |
| 7 | **WeightCLIP: Aligns Datasets/Models in Weight Space** | - | 2026 | 2607.03551 | Alignment in weight space; could incorporate base-specific encodings | **Target #4**: Weight space alignment with potential base-12/60 variants | arXiv |

**GAP ASSESSMENT:** MrRoPE (2026) provides the **only** theoretical framework for mixed-radix position embeddings. **No papers** on explicit base-12 or base-60 weight representations. Feucht et al. (2026) shows base choice matters empirically.

---

### 5. Base-12/Base-60 in Quantum Computing

| # | Title | Authors | Year | arXiv ID | Abstract Summary | Relevance to Target Area | Code Availability |
|---|-------|---------|------|----------|------------------|-------------------------|-------------------|
| 1 | **On non-Archimedean quantum mathematics and non-Archimedean (quantum) computation** | Nikolaj Glazunov | 2026 | 2601.05133 | Directly addresses non-Archimedean (base system) approaches to quantum computing; p-adic and non-Archimedean quantum computation | **Target #5**: **Most relevant** - explicitly addresses base-system quantum computing foundations | arXiv HTML |
| 2 | **Quantum codes are quantized codes** | Michael Zurel | 2026 | 2610.06607 | Finite field theory for quantum codes; base-60 could map to composite fields GF(4)×GF(3)×GF(5) via CRT | **Target #5**: Finite field approach; base-60 via Chinese Remainder Theorem structure | arXiv HTML |
| 3 | **A 12-CNOT Double Qubit Excitation Gate** | Irfansha Shaik | 2026 | 2608.11733 | 12-CNOT decomposition of double qubit excitation operator; lowest CNOT count/depth among SOTA | **Target #5 (indirect)**: 12-CNOT count (not base-12 representation); relevant for gate optimization | PDF, HTML, TeX |
| 4 | **Optimized Many-Hypercube Codes** | - | 2025/2026 | 2512.00561 | Quantum error correction codes with many-hypercube structures | **Target #5**: QEC codes; could adapt to base-12/60 symmetries | arXiv |
| 5 | **Scalable platform for qudit-based quantum computing using polar molecules** | - | 2025/2026 | 2508.10850 | Qudit-based QC with large alphabets; time-bin encoding | **Target #5**: Large-alphabet/time-base encoding relates to sexagesimal (60 symbols) | arXiv HTML |
| 6 | **Large Alphabet Set Time-bin Encoded MQKD** | - | 2026 | 2606.01262 | Multi-qubit QKD with large time-bin alphabets; relates to base-60 time encoding | **Target #5**: Time-bin encoding with large alphabets; sexagesimal connection | arXiv |

**GAP ASSESSMENT:** Glazunov (2026) is the **only** paper directly addressing non-Archimedean/base-system quantum computing. Zurel (2026) provides finite field framework adaptable to base-60 via CRT. **Significant gap** for base-12/60 quantum gates, error correction, and qubit representations.

---

### 6. Mixed-Radix Number Systems in Computer Architecture

| # | Title | Authors | Year | arXiv ID | Abstract Summary | Relevance to Target Area | Code Availability |
|---|-------|---------|------|----------|------------------|-------------------------|-------------------|
| 1 | **A Crypto-Agile Mixed-Radix NTT Accelerator for Negacyclic and Trinomial Rings** | Lee, Shin, Kim, Seo | 2026 | 2026/2610 (ePrint) | Unified butterfly integrating radix-2/3; conflict-free memory mapping; Artix-7 FPGA; 5,279 LUTs, 4 DSPs, 9 BRAMs at 141.5 MHz; supports ML-KEM, ML-DSA, HAETAE, etc. | **Target #6**: **Critical** - crypto-agile mixed-radix NTT on single datapath; directly applicable to base-12/60 NTT designs | Architecture details; no public code repo |
| 2 | **Regular mixed-radix DFT matrix factorization for in-place FFT accelerators** | Sergey Salishev | 2025 | 2505.06728 | Generic vector memory accelerator; fixed datapath DIT/DIF FFT; regular mixed-radix factorization | **Target #6**: **High** - mixed-radix FFT accelerator; fixed datapath suitable for base-12/60 | HTML experimental |
| 3 | **MrRoPE: Mixed-radix Rotary Position Embedding** | Tian, Zhu, Liu, Wang, Wang | 2026 | 2601.22181 | Theoretical foundation for ANY base RoPE; radix conversion framework | **Target #6**: Foundation for mixed-radix representations in hardware | ICLR 2026 |
| 4 | **Optimal Small-Bitwidth Moduli Set for Residue Number Systems** | Danila Gorodecky | 2026 | 2603.24387 | Algorithmic generation of optimal co-prime moduli sets; balances bit-lengths; maximizes dynamic range | **Target #6**: **Critical** - generates moduli for RNS; base-12={3,4,5}, base-60={7,11,13,17} etc. | Algorithm described; no public code |
| 5 | **MRUD: Maximally Redundant Unsigned Digit Number Systems** | Rahimi, Azarpeyvand | 2026 | 2610.39638 | Extends redundant digit systems to high radices; carry-free addition; 30% lower delay, 26% smaller area, 87% lower power vs MRSD | **Target #6**: **Critical** - redundant arithmetic for high radices; directly applicable to base-60 | FreePDK 45nm evaluation |
| 6 | **RISC-V Word-Size Modular Instructions for Residue Number Systems** | Didier, Robert | 2024 | 2412.05286 | RISC-V ISA extensions for RNS; word-size modular instructions; PQC applications | **Target #6**: **High** - ISA extensions; could incorporate base-12/60 word-size instructions | RISC-V compliance spec |
| 7 | **Hardware-Efficient FPGA Implementation of Sigmoid Using Mixed-Radix Hyperbolic Rotation CORDIC** | Panchal, Changela, Roy | 2026 | 2604.23547 | Mixed-radix CORDIC (radix-2/4/2-LVC); 835 logic slices, zero DSP, MAE 4.23×10⁻⁴ on Xilinx Virtex-7 | **Target #6**: **High** - mixed-radix CORDIC hardware; resource-efficient; adaptable to base-12/60 | FPGA implementation details |
| 8 | **A Generic Modulo-(2ⁿ±δ) RNS Multiplier Based on Twit Representation** | Gorgin, Sadr, Salami, Rahmati | 2026 | 2606.09965 | 12-modulus RNS configuration; 5-bit residue channels; small-moduli RNS | **Target #6**: **High** - 12-modulus RNS maps to base-12 concepts; small moduli for base-12/60 | 45nm FreePDK evaluation |
| 9 | **EMINEM: Efficient FPGA Implementation of Mixed-Radix NTT Hardware Accelerators** | Tu et al. | 2026 | ACM TRETS | Mixed-radix NTT for PQC (Falcon, Dilithium, HAWK); FPGA implementations | **Target #6**: **Critical** - FPGA mixed-radix NTT for multiple PQC standards | ACM TRETS 2026 |
| 10 | **New Ideas on a New Old Type of Cipher: The Mixed-Radix One-Time Pad** | Buono | 2026 | 2606.16040 | Mixed-radix OTP with base-12 cipher systems | **Target #1 + #6**: Direct base-12/cryptography relevance; mixed-radix cipher | arXiv HTML |

**GAP ASSESSMENT:** **No direct papers on sexagesimal ALU, base-60 carry-save adder, or duodecimal multiplier hardware.** The mixed-radix NTT/FFT accelerator papers (2025-2026) are the closest. MRUD (2026) provides redundant arithmetic foundation for high radices. **Significant hardware implementation gap** for base-12/60 specific arithmetic units.

---

### 7. Additional Novel Base-12/Base-60 Applications

| # | Title | Authors | Year | arXiv ID | Abstract Summary | Relevance | Code |
|---|-------|---------|------|----------|------------------|-----------|------|
| 1 | **The Prime Clockwork: A Dynamic Representation of Modular and Multiplicative Arithmetic** | - | 2026 | 2609.03896 | Dynamic visualization of modular/multiplicative arithmetic; prime patterns | Base-12/60 modular arithmetic visualization | arXiv HTML |
| 2 | **Binary-ternary collisions and the last significant digit of n! in base 12** | Deshouillers et al. | 2024 | 2412.09124 | Base-12 factorial digit distributions; collisions of s₂(n)=s₃(n) | Base-12 number theory; digit properties | PDF/HTML/TeX |

---

## EXPAND

### LEADS TO INVESTIGATE

- **LEAD: Mixed-Radix One-Time Pad (Buono 2026)** — WHY: Only paper explicitly implementing mixed-radix (base-12) cryptography with perfect secrecy proofs; QKD interface paper provides practical key generation — ANGLE: Implement MR-OTP with base-12 and base-60 as concrete instantiations; analyze key entropy, efficiency vs binary OTP

- **LEAD: MrRoPE Mixed-Radix Position Embedding (Tian et al. 2026, ICLR)** — WHY: Complete theoretical framework for mixed-radix position encodings; proven to extend context to 128K+; base-12/60 are direct instantiations — ANGLE: Implement MrRoPE-Pro with base-12 (2²×3) and base-60 (2²×3×5) radix conversions; benchmark on long-context tasks

- **LEAD: Non-Archimedean Quantum Computation (Glazunov 2026)** — WHY: Only paper directly addressing base-system quantum computing; p-adic framework naturally generalizes to composite bases — ANGLE: Explore base-12/60 as non-Archimedean bases for quantum gate representations and error correction

- **LEAD: Optimal RNS Moduli Sets for Base-12/60 (Gorodecky 2026)** — WHY: Algorithmic generation of co-prime moduli maximizing dynamic range; base-12={3,4,5}, base-60={4,3,5} or larger sets — ANGLE: Generate and evaluate RNS moduli sets for base-12/60; implement in hardware (FPGA/ASIC)

- **LEAD: MRUD Redundant Arithmetic for High Radices (Rahimi & Azarpeyvand 2026)** — WHY: 30% lower delay, 26% smaller area, 87% lower power; carry-free addition preserved at high radices — ANGLE: Adapt MRUD for base-60 (and base-12); design carry-free adders/multipliers

- **LEAD: Mixed-Radix CORDIC Hardware (Panchal et al. 2026)** — WHY: 835 logic slices, zero DSP on Virtex-7; mixed-radix hyperbolic rotation — ANGLE: Extend mixed-radix CORDIC to base-12/60 for transcendental function approximation

- **LEAD: Crypto-Agile Mixed-Radix NTT Accelerator (Lee et al. 2026)** — WHY: Unified radix-2/3 butterfly; conflict-free memory mapping; supports multiple PQC standards — ANGLE: Extend to base-12 (radix-3) and base-60 (radix-2/3/5) NTT for post-quantum crypto

- **LEAD: Empirical Base Choice Affects Cyclic Reasoning (Feucht et al. 2026)** — WHY: LLMs use base-10 for cyclic concepts; base choice affects reasoning — ANGLE: Controlled study comparing base-10 vs base-12 vs base-60 for cyclic arithmetic reasoning in LLMs

- **LEAD: Base-12 Factorial Digit Distribution (Deshouillers et al. 2024)** — WHY: Proves all digits 1-11 appear as last nonzero digit of n! in base 12 infinitely often with known densities — ANGLE: Use base-12 factorial properties for pseudorandom number generation or cryptographic primitives

### DEAD ENDS EXPLORED

- **DEAD END: Direct "sexagesimal signal processing" papers** — No papers found on base-60 filter design, wavelet transforms, or spectral analysis beyond mixed-radix FFT accelerators
- **DEAD END: "Duodecimal physics simulation" or "base-12 orbital mechanics"** — No papers found; only general celestial mechanics (Toxvaerd 2025)
- **DEAD END: "Base-12 quantum gates" or "duodecimal quantum error correction"** — Only 12-CNOT gate count paper (not base-12 representation); Glazunov 2026 is only non-Archimedean QC paper
- **DEAD END: "Sexagesimal ALU" or "base-60 carry-save adder"** — No direct papers; MRUD 2026 provides redundant arithmetic foundation but not base-60 specific
- **DEAD END: "Duodecimal multiplier hardware"** — No papers; mixed-radix OTP (Buono 2026) is closest cryptographic connection

---

## CLAIMS

- **CLAIM: The literature gap for base-12/base-60 applications is substantial across all 6 target areas** — RISK: normal — SOURCES: arXiv (cs.CR, cs.AR, quant-ph, cs.LG, math.NT) — COUNTER: None found; all searches returned zero or few indirect matches — PRIMARY: Comprehensive search via 4 parallel agents + 10+ manual web searches across arXiv

- **CLAIM: MrRoPE (2601.22181) is the only theoretical framework for mixed-radix position embeddings adaptable to base-12/60** — RISK: normal — SOURCES: arXiv cs.LG, ICLR 2026 proceedings — COUNTER: nD-RoPE (2606.12146) generalizes dimensions but doesn't address base choice — PRIMARY: Tian et al. 2026 (ICLR 2026 oral)

- **CLAIM: Mixed-Radix One-Time Pad (Buono 2026) is the only paper implementing base-12/60 cryptography with information-theoretic security** — RISK: normal — SOURCES: arXiv cs.CR — COUNTER: Hoenen 2023 and Lin 2000 are general base-n but not mixed-radix or base-12/60 specific — PRIMARY: Buono 2026 (2606.16040, 2606.18526)

- **CLAIM: Non-Archimedean quantum computation (Glazunov 2026) provides the only direct foundation for base-system quantum computing** — RISK: normal — SOURCES: arXiv quant-ph — COUNTER: Zurel 2026 provides finite field approach via CRT but not base-system framework — PRIMARY: Glazunov 2026 (2601.05133)

- **CLAIM: No papers exist on base-12/60 in physics simulations (orbital mechanics, wave equations, numerical relativity)** — RISK: high — SOURCES: arXiv physics.* categories — COUNTER: Only Toxvaerd 2025 on general celestial mechanics approximations — PRIMARY: Search agent ArxivPhysicsSim + manual searches

- **CLAIM: Mixed-radix NTT/FFT hardware accelerators (2025-2026) are the closest existing work to base-12/60 computer architecture** — RISK: normal — SOURCES: arXiv cs.AR, ACM TRETS, IEEE TC — COUNTER: None address base-12/60 specifically; all focus on PQC-relevant radices — PRIMARY: Lee et al. 2026, Salishev 2025, Tu et al. 2026

- **CLAIM: Feucht et al. (2026) provides empirical evidence that base choice affects LLM cyclic reasoning** — RISK: normal — SOURCES: arXiv cs.AI — COUNTER: Single study on base-10; no base-12/60 comparison exists — PRIMARY: Feucht et al. 2026 (2605.01148)

- **CLAIM: MRUD (Rahimi & Azarpeyvand 2026) demonstrates redundant arithmetic scales to high radices with significant benefits** — RISK: normal — SOURCES: arXiv cs.AR — COUNTER: Only evaluated up to radix-2ʰ; base-60 not a power of 2 — PRIMARY: Rahimi & Azarpeyvand 2026 (2610.39638)

---

## Summary Statistics

| Target Area | Direct Papers | Indirect/Adaptable Papers | Total | Gap Level |
|-------------|---------------|---------------------------|-------|-----------|
| 1. Base-12/60 Cryptography | 1 (Buono MR-OTP) | 2 (Hoenen, Lin) | 3 | **Complete** |
| 2. Base-60 Signal Processing | 0 | 5 (FFT/RNS/RoPE) | 5 | **Large** |
| 3. Physics Simulations | 0 | 1 (Toxvaerd celestial) | 1 | **Complete** |
| 4. ML Position/Weights | 0 | 7 (MrRoPE, nD-RoPE, Feucht, etc.) | 7 | **Large** |
| 5. Quantum Computing | 1 (Glazunov) | 5 (Zurel, qudit, time-bin) | 6 | **Large** |
| 6. Mixed-Radix Architecture | 0 | 10 (NTT, RNS, CORDIC, MRUD) | 10 | **Medium** |

**Total Novel Research Opportunities:** 6 target areas with significant gaps, particularly in cryptography (MR-OTP), ML (MrRoPE adaptation), quantum (non-Archimedean), and hardware (MRUD/NTT/CORDIC for base-12/60).