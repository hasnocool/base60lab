# L-10: Modular Forms and q-Series in Base-60 — Research Findings

## Papers Found

### Directly Relevant to Base-60 Connection

1. **Caldin, A.S. (2026)** — "Jones Polynomials at Roots of Unity and Modular L-Values via Mod 60 — E8 Intelligence Research"
   - **DOI**: 10.5281/zenodo.23333013
   - **Key Finding**: "Modular form Fourier coefficients exhibit periodicity mod 60 (e.g., Δ(τ) coefficients mod 60 follow a 60-cycle), linking to Babylonian sexagesimal arithmetic"
   - **Math**: "Periodicity mod 60 arises from Γ₀(2) congruence subgroup and Ramanujan tau-like congruences (e.g., τ(n) ≡ σ₁₁(n) mod 691, but mod 60 relates to η-function exponents mod 24 and 60 = lcm(12,20))"
   - **Connection**: Base-60 appears explicitly via cyclotomic field Q(ζ₆₀), Galois group (ℤ/60ℤ)ˣ of order 16, golden ratio via 2cos(2π/5) and 2cos(2π/10)

2. **Choi, J.; Kwon, Y.-W.; Lee, Y. (2026)** — "On the distribution of fourier coefficients of modular forms modulo odd integers"
   - **DOI**: 10.1007/s11139-026-01351-3
   - **Relevance**: Investigates a_f(n) mod M for odd M; conditions depend on prime divisors of M. Base-60 = 2²×3×5 has prime factors {2,3,5}

### Ramanujan Partition Congruences (mod 5, 7, 11)

3. **Zagier, D. (2026)** — "Ramanujan's congruences for partitions modulo 5, 7, and 11"
   - **DOI**: 10.46298/hrj.2026.17901
   - **Content**: Short uniform proofs of p(5n+4)≡0 mod 5, p(7n+5)≡0 mod 7, p(11n+6)≡0 mod 11

4. **Yavuz, A. (2018)** — "Ramanujan's congruences for the partition function modulo 5,7,11"
   - **Semantic Scholar ID**: dbee72e2a234de90a7c033441c9183f7d7bc570d

5. **Berndt, B. (2007)** — "RAMANUJAN'S CONGRUENCES FOR THE PARTITION FUNCTION MODULO 5, 7, AND 11"
   - **DOI**: 10.1142/S1793042107000961

6. **Atmani, S.; Bayad, A.; Hernane, M. (2022)** — "Congruences for Fourier coefficients of eta-quotients modulo powers of 5, 7, 11, 13, and 17"
   - **DOI**: 10.1002/mma.8816
   - **Relevance**: Direct work on eta-quotients η(τ)^λ mod prime powers; connects to Dedekind eta function q^(1/24)∏(1-q^n)

### Ramanujan Tau Function & Modular Forms

7. **Moree, P. (2002)** — "On some claims in Ramanujan's 'unpublished' manuscript on the partition and tau functions"
   - **arXiv**: math/0201265v2
   - **Content**: τ(n) ≡ ∑_{d|n} d¹¹ (mod 691); congruences for τ(n) modulo special primes q

8. **Doyon, A.; Lei, A. (2021)** — "Congruences between Ramanujan's tau function and elliptic curves"
   - **arXiv**: 2103.06154v1
   - **Key**: Congruences modulo p=2,3 (base-60 factors!) for elliptic curves with rational p-torsion

9. **Charles, D.X. (2006)** — "Computing the Ramanujan tau function"
   - **DOI**: 10.1007/s11139-006-6509-y

10. **Parnoff, E.; Raghuram, A. (2024)** — "Ramanujan's congruence primes"
    - **arXiv**: 2403.03345
    - **Content**: τ(p) ≡ p¹¹+1 (mod 691); prime 67 from L(6,χ)/(π⁶√5) for χ mod 5

### Dedekind Eta Function & q-Expansions

11. **Köhler, G. (2011)** — "Dedekind's Eta Function and Modular Forms"
    - **DOI**: 10.1007/978-3-642-16152-0_1
    - **Relevance**: η(τ) = q^(1/24)∏_{n≥1}(1-q^n); weight 1/2; Δ(τ) = η(τ)^24 weight 12

12. **Biagioli, A. (1990)** — "The construction of modular forms as products of transforms of the Dedekind eta function"
    - **DOI**: 10.4064/aa-54-4-273-300

13. **Apostol, T.M. (1990/1976)** — "The Dedekind eta function"
    - **DOI**: 10.1007/978-1-4612-0999-7_3

### Modular Forms mod 60 / Periodicity

14. **Strouse, C.R. (2026)** — "Analogue of Cardy's formula on the 60-degree parallelogram: a modular approach"
    - **arXiv**: 2608.29425
    - **Relevance**: Modular form η(τ)²η(3τ)² on π/3 parallelogram (60°)

## Key Mathematical Connections to Base-60

### 1. Eta Function Exponent 1/24 and 60 = lcm(12, 20)
- η(τ) = q^(1/24) ∏(1-qⁿ)
- Δ(τ) = η(τ)²⁴ = q ∏(1-qⁿ)²⁴ = ∑ τ(n) qⁿ (weight 12 cusp form)
- 60 = lcm(12, 20) where 12 = weight of Δ, 20 = ?
- Caldin (2026) explicitly states: "mod 60 relates to η-function exponents mod 24 and 60 = lcm(12,20)"

### 2. Fourier Coefficient Periodicity mod 60
- **Caldin**: "Δ(τ) coefficients mod 60 follow a 60-cycle"
- This means τ(n) mod 60 is periodic with period 60
- Direct link to sexagesimal arithmetic!

### 3. Partition Congruences and Base-60 Primes
- Ramanujan: p(5n+4)≡0(5), p(7n+5)≡0(7), p(11n+6)≡0(11)
- Base-60 = 2²×3×5 has prime factors {2,3,5}
- Only **5** is a Ramanujan congruence prime AND a base-60 factor
- 7 and 11 are NOT factors of 60
- Doyon & Lei (2021): τ(n) congruences modulo 2,3 (both base-60 factors!)

### 4. Cyclotomic Field Q(ζ₆₀)
- Roots of unity e^(2πi/60) generate 60th cyclotomic field
- Galois group (ℤ/60ℤ)ˣ has order φ(60) = 16
- 16 = rank-4 lattice D₄ symmetry
- 60 = 2×30, 30 = Coxeter number of E₈

### 5. Golden Ratio Connection
- 2cos(2π/5) = φ, 2cos(2π/10) = φ
- Both 5 and 10 divide 60
- φ emerges from 60th roots of unity

### 6. Γ₀(2) Congruence Subgroup
- Periodicity mod 60 arises from Γ₀(2)
- Level 2 subgroup relates to 2-adic structure (base-60 factor)

## Relevance to Experiment F (Algebra/Sequences)

### Experiment F Context (from NEW_EXPERIMENTS_PROPOSAL.md)
- "Ramanujan, mock theta, partition congruences"
- "Base-60 + Experiment D (FFT sizes) + Experiment C (RNS)"
- "Exact rational via NTT"

### Connections:
1. **Partition function p(n) sequence**: p(n) mod 5,7,11 are base-60 relevant (5 is a factor)
2. **Ramanujan tau sequence τ(n)**: Δ(τ) = ∑τ(n)qⁿ; τ(n) mod 60 has 60-cycle
3. **Mock theta functions**: Ramanujan's f, ω functions (Berg et al. 2013)
4. **Eta-quotients**: η(τ)^k mod prime powers (Atmani et al. 2022) — exact rational coefficients
5. **NTT for exact convolution**: Fourier coefficients of modular forms are integers; NTT can compute τ(n) exactly
6. **Mixed-radix FFT**: Base-60 = {2,3,5} smooth numbers → efficient NTT sizes for computing q-expansions

## Dead Ends / Unresearched Areas

1. **No paper directly studies**: "q-expansion digits in base-60 representation" — no one has written the q-series coefficients in sexagesimal and looked for patterns
2. **No paper on**: "Partition function p(n) in base-60 digit patterns" — all work is modulo primes, not base representation
3. **No paper on**: "Ramanujan tau function τ(n) base-60 digits" — only modulo 60 periodicity
4. **No paper on**: "Babylonian sexagesimal computation of modular forms" — historical gap

## Recommended Search Angles for Further Research

1. **Compute τ(n) mod 60 for n=1..1000** — verify 60-cycle, look for structure
2. **Convert p(n) to base-60** — do the famous congruences create visible digit patterns?
3. **Eta function q^(1/24) in base-60** — 1/24 = 0;2,30 in sexagesimal; does this fraction representation reveal something?
4. **NTT with 60-smooth sizes** for computing modular form coefficients exactly
5. **E₈ lattice connection** — 240 roots, 30 Coxeter number, 60 = 2×30

## Summary

**Strongest finding**: Caldin (2026) explicitly states "modular form Fourier coefficients exhibit periodicity mod 60 (e.g., Δ(τ) coefficients mod 60 follow a 60-cycle), linking to Babylonian sexagesimal arithmetic" — this is a direct, testable claim connecting base-60 to modular forms.

**The base-60 factor 5** is a Ramanujan congruence prime for partitions. **Factors 2,3** appear in tau function congruences (Doyon & Lei). The Dedekind eta function's 1/24 exponent and Δ=η²⁴ connect to 60 via lcm(12,20).

**Experiment F relevance**: High. Computing modular form coefficients via NTT using 60-smooth transform sizes, and investigating base-60 digit patterns in q-expansions, are unexplored experimental directions.