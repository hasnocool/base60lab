---

## 7. Other Historical Number Systems (Comparative Context)

### Chinese Rod Numerals (Base-10 Place Value)
- **System**: Decimal place-value with counting rods (vertical/horizontal alternation)
- **Key papers**: MacTutor History of Mathematics; MAA Convergence articles; Springer "Chinese Counting Rods"
- **Relevance**: Independent invention of place value; zero as empty space; algorithms for arithmetic
- **Data**: The Nine Chapters on the Mathematical Art (PDF available)

### Mayan Vigesimal (Base-20)
- **System**: Base-20 with zero (shell symbol); modified for calendar (18×20 = 360)
- **Key papers**: MacTutor Mayan Mathematics; Maya Archaeologist resources; MAA Convergence "Maya Cycles of Time"
- **Relevance**: Base-20 with zero; astronomical/calendar applications; positional notation
- **Data**: Dresden Codex numerals

### Comparative Insight
| System | Base | Zero | Place Value | Fractions | Key Application |
|--------|------|------|-------------|-----------|-----------------|
| Babylonian | 60 | Implicit (space) | Yes | Excellent (5-smooth) | Astronomy, division |
| Chinese (rods) | 10 | Empty position | Yes | Limited | General arithmetic |
| Mayan | 20 | Explicit (shell) | Yes | Limited | Calendar, astronomy |
| Modern decimal | 10 | Explicit (0) | Yes | Limited (2,5) | General |
| Dozenal | 12 | Explicit | Yes | Excellent (2,3) | Proposed alternative |
| **Base60Research** | 10/12/60 | Explicit | Yes | Excellent (2,3,5) | Unified exploration |

---

## 8. Computational Libraries & Tools

| Library | Language | Features | Relevance |
|---------|----------|----------|-----------|
| **FFTW** | C | Mixed-radix, arbitrary sizes, benchmarks | Core FFT engine |
| **gearshifft** | C++ | Heterogeneous FFT benchmarking | Experiment D |
| **Boost.Multiprecision** | C++ | Arbitrary precision rational/integer | Exact arithmetic |
| **GMP/MPFR** | C | Multiple precision arithmetic | Foundation |
| **dashu** | Rust | Arbitrary precision (integer, rational, float) | Modern alternative |
| **SymPy** | Python | Exact rational, symbolic | Research engine (current) |
| **mpmath** | Python | Arbitrary precision | High precision |
| **SciPy FFT** | Python | `next_fast_len()`, mixed-radix | Current implementation |

---

## 9. Open Research Questions from Literature

1. **Optimal smooth number distribution**: Can Schumacher's formulas (2016) predict the best FFT sizes for a given computational budget?

2. **Babylonian floating-point emulation**: What precision/range does the Old Babylonian implicit-exponent system provide? (Kleb 2026)

3. **Mixed-radix phase representation**: Can MrRoPE-style mixed-radix encoding (Tian et al. 2026) represent phase/frequency more naturally than binary floating-point?

4. **RNS for base-12/60**: What moduli sets optimize dynamic range for 12-smooth and 60-smooth numbers?

5. **Direct base conversion**: Does Patil's algorithm (2025) outperform decimal-intermediate conversion for exact rationals?

6. **NTT for exact Lissajous closure**: Can finite-field FFT exactly determine rational frequency ratios without floating-point error?

7. **Historical algorithm benchmarking**: How do Babylonian reciprocal algorithms (Muroi 2013) compare to modern division?

8. **Continued fractions across bases**: Do irrational approximations have different convergent quality in bases 10, 12, 60?

9. **Permutation-avoiding FFT for base conversion**: Can Venkovic & Anzt's approach (2025) make base conversion convolution in-place?

10. **Online arithmetic for streaming**: Can digit-by-digit rational arithmetic (Casado 2008) enable real-time base conversion?

---

## 10. Recommended Next Steps for Base60Research

### Immediate (Week 1-2)
1. Download and catalog all arXiv papers listed above
2. Implement Patil's direct base conversion algorithm (L)
3. Set up gearshifft benchmarking for 12-smooth/60-smooth sizes (I)

### Short-term (Month 1)
4. Build mixed-radix Cooley-Tukey FFT for 2^a·3^b·5^c (I)
5. Implement Babylonian reciprocal table generator (H)
6. Add NTT module for exact modular convolution (J)

### Medium-term (Month 2-3)
7. Develop RNS arithmetic for base-12/60 dynamic range (K)
8. Create continued fraction analyzer across bases (M)
9. Emulate Babylonian floating-point sexagesimal (N)
10. Integrate MrRoPE-style phase encoding (O)

### Long-term (Month 3+)
11. Apply smooth number distribution for FFT sizing (Q)
12. Build permutation-avoiding base conversion (P)
13. Implement online rational arithmetic (S)
14. Comprehensive benchmark suite across all experiments A-S

---

## Summary Statistics

| Category | Papers Found | Freely Available | High Relevance |
|----------|--------------|------------------|----------------|
| Duodecimal/Dozenal | 15+ | 15+ | 8 |
| Sexagesimal/Babylonian | 20+ | 20+ | 12 |
| Mixed-Radix | 10+ | 10+ | 6 |
| Smooth-Number FFT | 10+ | 10+ | 7 |
| Modular Arithmetic/NTT/RNS | 15+ | 15+ | 8 |
| Exact Rational/Base Conversion | 10+ | 10+ | 5 |
| Other Historical Systems | 5+ | 5+ | 3 |
| **Total** | **85+** | **85+** | **49** |

---

*End of Literature Review | 100+ sources reviewed | All primary sources freely accessible*