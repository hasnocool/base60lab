# EXPANSION WAVE 2 — LEAD L-09: Babylonian Reciprocal Tables and Plimpton 322 Reconstruction

## Research Summary

This exhaustive literature search covers **YBC 7290** (trapezoid area calculation), **YBC 7289** (√2 approximation), **Plimpton 322** (Pythagorean triples), and **Babylonian exact sexagesimal arithmetic** — the computational methods documented and their relevance to base60lab's exact rational tools.

---

## 1. YBC 7290: The Practical Application Tablet

**Tablet**: YBC 7290 (Yale Babylonian Collection, P255049)  
**Period**: Old Babylonian, c. 1800–1600 BCE  
**Content**: Trapezoid area calculation with bases 2;20 and 2;00, height 2;20

### Exact Computation (from safeguard.sh worked example)
```
Area = (B₁ + B₂) × h / 2
     = (2;20 + 2;00) × 2;20 / 2
     = (4;20) × 2;20 / 2
     = 5;03,20  (sexagesimal)
```

**Decimal check**: 
- 2;20 = 2 + 20/60 = 2.333...
- 2;00 = 2
- Average = (2.333... + 2)/2 = 2.1666... = 2;10
- 2;10 × 2;20 = 2.1666... × 2.333... = 5.0555... = 5;03,20 ✓

### Mathematical Significance
- **Not a reciprocal table per se**, but embodies the mathematical culture that produced them
- Demonstrates **practical land surveying** using exact sexagesimal arithmetic
- Uses the **average-of-bases formula** (modern trapezoid area formula)
- All numbers involved are **regular** (only prime factors 2, 3, 5), enabling exact computation

### Connection to Reciprocal Tables
Division by 2 is trivial (multiply by 0;30), but the general trapezoid formula requires division by arbitrary numbers. The Babylonian method: **division = multiplication by reciprocal**. For regular divisors, this is exact and fast.

---

## 2. YBC 7289: The √2 Approximation Tablet

**Tablet**: YBC 7289 (Yale Babylonian Collection)  
**Content**: Square with diagonals; numbers 30, 1;24,51,10, 42;25,35

### The Approximation
```
√2 ≈ 1;24,51,10 (sexagesimal)
   = 1 + 24/60 + 51/3600 + 10/216000
   = 30547/21600
   = 1.41421296...
```

**True √2**: 1.41421356...
**Error**: ~6 parts in 10 million (< 1 part in 2 million relative)

### Computation Method: Babylonian (Heron) Iteration
```
a₀ = 1;30 = 1.5
a₁ = (a₀ + 2/a₀)/2 = (1.5 + 2/1.5)/2 = 1.41666... = 1;25
a₂ = (1;25 + 2/1;25)/2 = 1;24,51,10,35,17,38... → truncate to 1;24,51,10
a₃ = 1;24,51,10,7,46,6... (11 decimal places correct)
```

**Critical insight**: The iteration requires division by `2a`. At step 2, `2a = 2;50` = 170/60, which has factor 17 → **not regular**. The scribe **could not** do this division exactly from tables. The value was likely copied from a table of constants (YBC 7243) or computed using an approximation.

### Floating-Point Interpretation
The same digits can be read as:
- Side = 30, diagonal = 42;25,35 → √2
- Side = 0;30 (½), diagonal = 0;42,25,35 → 1/√2

This **reciprocal pair** interpretation (Fowler & Robson 1998) aligns with the centrality of reciprocal pairs in Babylonian mathematics.

---

## 3. Plimpton 322: Pythagorean Triples Tablet

**Tablet**: Plimpton 322 (Columbia University, P254790)  
**Period**: Old Babylonian, c. 1822–1784 BCE (Robson)  
**Content**: 15 rows × 4 columns of sexagesimal numbers

### Table Structure (reconstructed)
| Row | Col 1: (d/l)² | Col 2: s (short side) | Col 3: d (diagonal) | l = long side (not written) |
|-----|---------------|----------------------|---------------------|----------------------------|
| 1   | 1;59,0,15     | 1,59                 | 2,49                | 120                        |
| 2   | 1;56,56,58,14,50,6,15 | 56,7           | 1,20,25             | 3,456                      |
| 3   | 1;55,7,41,15,33,45    | 1,16,41        | 1,50,49             | 4,800                      |
| ... | ...           | ...                  | ...                 | ...                        |
| 11  | 1;15          | 45                   | 1,15                | 60 (3-4-5 scaled by 15)    |
| ... | ...           | ...                  | ...                 | ...                        |

**Key property**: Every `l` (long side) is a **regular number** (only prime factors 2, 3, 5).

### Three Interpretations

#### Reading 1: Number Theory (Neugebauer & Sachs 1945)
Generate triples via Euclid's formula with regular parameters:
```
p, q regular, p > q
s = p² - q², l = 2pq, d = p² + q²
```
Row 1: p=12, q=5 → s=144-25=119, l=120, d=169 (all regular factors)

**Zeeman's observation**: Exactly 16 such triples fit natural constraints (q ≤ 60, slope 30°–45°); 15 appear on the tablet.

#### Reading 2: Reciprocal Pairs & Teacher's List (Bruins → Robson & Friberg) — **Most Supported**
```
Choose regular x, look up 1/x
d/l = (x + 1/x)/2
s/l = (x - 1/x)/2
```
**Row 1 worked example** (from safeguard.sh):
```
1. Choose x = 2;24 (12/5 = 2.4)
2. 1/x = 0;25 (from table: 25 × 2,24 = 1)
3. (x + 1/x)/2 = (2;24 + 0;25)/2 = 2;49/2 = 1;24,30 = d/l
4. (x - 1/x)/2 = (2;24 - 0;25)/2 = 1;59/2 = 0;59,30 = s/l
5. (d/l)² = 1;24,30² = 1;59,0,15 = Column 1
6. Scale by 2,0 (120): s = 1,59 (119), d = 2,49 (169)
```

**Evidence supporting this reading**:
- Column headings match: "square of diagonal from which 1 is torn out, so width comes up" → (d/l)² - 1 = (s/l)²
- Row 13 error: scribe wrote 7,12,1 (which is 2,41²) instead of 2,41 → working with squares/square sides
- Row 15 error: common factor 2 removed from one column but not the other
- All operations (reciprocal lookup, halving, squaring, scaling by regular factors) are **table operations** scribes were trained in

#### Reading 3: Exact Sexagesimal Trigonometry (Mansfield & Wildberger 2017)
- Claims tablet is a trigonometric table of ratios (s/d, l/d) based on exact rational arithmetic
- **Controversial**: Most historians consider "angle" concept anachronistic for Old Babylonian period
- **Agreed by all**: Every ratio is exact in base 60 because l is regular

---

## 4. Babylonian Reciprocal Tables: Construction & Algorithms

### Regular Numbers Definition
A number is **regular** in base 60 iff its prime factors ⊆ {2, 3, 5} (i.e., 5-smooth numbers).

### Standard Reciprocal Table (27 entries)
From the Old Babylonian school curriculum (Sachs 1947; safeguard.sh):
```
igi 2   gál.bi 30        igi 27  gál.bi 2,13,20
igi 3   gál.bi 20        igi 30  gál.bi 2
igi 4   gál.bi 15        igi 32  gál.bi 1,52,30
igi 5   gál.bi 12        igi 36  gál.bi 1,40
igi 6   gál.bi 10        igi 40  gál.bi 1,30
igi 8   gál.bi 7,30      igi 45  gál.bi 1,20
igi 9   gál.bi 6,40      igi 48  gál.bi 1,15
igi 10  gál.bi 6         igi 50  gál.bi 1,12
igi 12  gál.bi 5         igi 54  gál.bi 1,6,40
igi 15  gál.bi 4         igi 1,4 gál.bi 56,15
igi 16  gál.bi 3,45      igi 1,21 gál.bi 44,26,40
igi 18  gál.bi 3,20
igi 20  gál.bi 3
igi 24  gál.bi 2,30
igi 25  gál.bi 2,24
```

**Missing**: 7, 11, 13, 14, 17, 19, 21, 22, 23, 26, 28, 29, 31, 33, 34, 35, 37... (any with prime factor > 5)

### Construction Algorithms (Friberg 2016, 2019; Muroi 2013)

#### 1. Successive Doubling/Tripling (a-rá-kár "blowing up multiplication")
```
Start with 1
Multiply by 2:  2, 4, 8, 16, 32, 1,4, 2,8, 4,16, 8,32, 17,4, 34,8, ...
Multiply by 3:  3, 9, 27, 1,21, 4,3, 12,9, 36,27, 1,48,54, 5,37,48, ...
Multiply by 5:  5, 25, 2,5, 10,25, 52,5, 2,42,5, 13,22,5, ...
```

#### 2. Combined Generation (2ᵃ × 3ᵇ × 5ᶜ)
Systematic enumeration of all regular numbers up to a given bound.

#### 3. Seleucid Advanced Tables (Friberg & Al-Rawi 2016)
- Tablet AO 6456: 231 six-place regular numbers with first digit 1 or 2
- Knuth (1972): "first man in history to solve a computational problem that takes longer than one second on a modern electronic computer"
- Methods: "Direct and Inverse Factorization Algorithms" for many-place regular numbers

### Division via Reciprocals: 7,429 ÷ 36 (worked example)
```
Step 1: Look up reciprocal: igi 36 gál.bi 1,40  (1/36 = 0;1,40)
Step 2: Dividend in base 60: 7,429 = 2,3,49
Step 3: Multiply digit by digit (long multiplication in base 60)
Step 4: Carry from right (mod 60 per column)
Result: 3,26;21,40 = 206 + 13/36  ✓ exact
```

**Speed comparison**: Decimal long division needs 3 rounds of "how many times?" + multiply + subtract. Babylonian: 1 table lookup + 6 digit products + 3 carries. **No search step for regular divisors.**

---

## 5. Non-Regular Divisors: Approximation Methods

### Method: Find Regular Number Near Multiple
For 7,429 ÷ 37 (37 is prime, non-regular):
```
37 × 81 = 2,997 ≈ 3,000 = 50,0 (regular)
1/37 ≈ 81/3,000 = 81 × 0;0,1,12 = 0;1,37,12
Multiply: 2,3,49 × 0;1,37,12 ≈ 3,20;34,58,48
Whole part: 3,20 = 200
Check: 37 × 200 = 7,400, remainder 29 ✓
```

### Long Division for Non-Regular (if needed)
1/19 in base 60: period 18 (remainder cycles back after 18 steps)
```
1/19 = 0;3,9,28,25,15,47,22,6,18,56,50,31,34,44,12,37,53,41 (repeating)
```
Same period as decimal (18 digits), but **no table entry exists** — scribe must approximate.

---

## 6. Relevance to base60lab Experiments

### Experiment B: Geometry (Circle Subdivisions & Polygons)
| Babylonian Feature | base60lab Module | Connection |
|---|---|---|
| 360° = 6×60 circle | `geometry.CIRCLE_SUBDIVISIONS` | Direct descendant |
| Exact chord lengths for constructible polygons | `geometry.chord_length_squared` | n=6 gives rational (1); n=3,4 need √3, √2 |
| Trapezoid area formula | New: need `polygon_area` for trapezoid | YBC 7290 practical geometry |
| Diagonal of square (√2) | `trigonometry.exact_sin_cos` for 45° | YBC 7289 approximation |
| Pythagorean triples | New: need generator from reciprocal pairs | Plimpton 322 method |

**Implementation opportunity**: 
- Add **Babylonian trapezoid area** using exact rational arithmetic
- Add **Plimpton 322 triple generator** from reciprocal pairs (x, 1/x)
- Add **√2 approximation** via Babylonian iteration with exact rationals

### Experiment E: Modular Arithmetic (Mod 60)
| Babylonian Feature | base60lab Module | Connection |
|---|---|---|
| Regular numbers = units in ℤ/60ℤ | `modular.units(60)` | 16 units: {1,7,11,13,17,19,23,29,31,37,41,43,47,49,53,59} |
| Reciprocal = modular inverse | `modular.mod_inv` | Exact inverse for units |
| Non-regular = zero divisors | `modular.zero_divisors(60)` | 44 zero divisors (have prime factors 2,3,5) |
| Division via reciprocal | `modular.mod_div` | Works only for units |

**Critical insight**: The Babylonian "regular numbers" (2ᵃ3ᵇ5ᶜ) are **NOT** the units modulo 60. They are the **zero divisors** (plus 0). The units are numbers coprime to 60 (primes 7, 11, 13, 17...). This is a fundamental distinction:
- **Regular (Babylonian)**: finite sexagesimal reciprocal → exact division
- **Unit (modular)**: modular inverse exists → modular division

This duality is key: the Babylonians optimized for **exact fractional arithmetic**, not modular arithmetic.

---

## 7. Key Papers & Sources

| Source | Type | Key Contribution |
|---|---|---|
| **safeguard.sh blog** | Comprehensive tutorial | Worked examples of all 7 problems in base 60; reciprocal table; YBC 7289/322 analysis |
| **Mansfield & Wildberger (2017)** | *Historia Mathematica* 44(4) | "Plimpton 322 is Babylonian exact sexagesimal trigonometry" — controversial but mathematically rich |
| **Friberg (2019)** | *Archive for History of Exact Sciences* 73(2) | "Three thousand years of sexagesimal numbers" — comprehensive survey |
| **Friberg & Al-Rawi (2016)** | Springer book chapters | Late Babylonian many-place reciprocal tables; factorization algorithms |
| **Muroi (2013)** | Springer Proc. Math & Stat | Babylonian number theory & trigonometric functions in Plimpton 322 |
| **Sachs (1947)** | *J. Cuneiform Studies* 1(3) | Standard reciprocal table edition |
| **Neugebauer (1935)** | *Mathematische Keilschrift-Texte* | YBC collection publication |
| **Bečvářová (2021)** | Czech journal | Analysis of YBC 7290, 7289, 7302 together |
| **Caldin (2026)** | Zenodo series | E8 Intelligence Research — reciprocal-pair generation of Pythagorean triples |
| **Robson (2001, 2002)** | *Hist. Math.*, *Am. Math. Monthly* | Teacher's list interpretation of Plimpton 322 (most accepted) |

---

## 8. Reconstruction Plan for base60lab

### Immediate Additions (Week 1)
1. **BabylonianTrapezoid class** — exact area from YBC 7290 formula
2. **Plimpton322Generator** — generate triples from reciprocal pairs (x, 1/x) using exact rationals
3. **BabylonianSqrt2** — iteration with exact rationals, tracking where non-regular divisors force approximation
4. **RegularNumberSet** — generate all 5-smooth numbers up to bound; test `Rational.is_terminating_in_base(60)`

### Short-term (Month 1)
5. **ReciprocalTable** — construct standard 27-entry table; extend to many-place using Friberg's algorithms
6. **SexagesimalLongDivision** — implement digit-by-digit division for non-regular divisors
7. **YBC7289Reconstruction** — full square root iteration with error analysis at each step

### Experimental Validation
- Compare Babylonian division speed (table lookup + multiplication) vs modern long division for regular divisors
- Test Plimpton 322 triple generation: verify all 15 rows from reciprocal pairs
- Measure representation efficiency: base 60 vs base 10 vs base 12 for geometric constants

---

## 9. Dead Ends / Exhausted Leads

| Lead | Status |
|---|---|
| YBC 7290 as a "reciprocal table" | **Not a reciprocal table** — it's a trapezoid area tablet that *uses* the reciprocal arithmetic culture |
| Plimpton 322 as trigonometric table | **Controversial** — mathematically valid as ratio table, but "trigonometry" likely anachronistic |
| Direct modular arithmetic in Old Babylonian texts | **No evidence** — they used exact fractional arithmetic, not modular arithmetic |
| "Floating point" as modern concept | **Valid analogy** — but Babylonian system was more flexible (no fixed exponent) |

---

## EXPAND

- LEAD: **YBC 7290 trapezoid area as practical geometry validation** — WHY: Direct application of exact sexagesimal arithmetic to land surveying; ANGLE: Implement exact trapezoid area in base60lab.geometry and compare to modern floating-point
- LEAD: **Plimpton 322 reciprocal-pair generator** — WHY: Core algorithm linking reciprocal tables to Pythagorean triples; ANGLE: Implement exact rational generator from (x, 1/x) pairs and verify all 15 tablet rows
- LEAD: **Babylonian √2 iteration with exact rationals** — WHY: Demonstrates where exact arithmetic succeeds (regular divisors) and forces approximation (non-regular); ANGLE: Step-by-step reconstruction showing error propagation
- LEAD: **Friberg's factorization algorithms for many-place regular numbers** — WHY: Late Babylonian "number crunching" tables (9⁴⁶ etc.); ANGLE: Implement direct/inverse factorization for 60-smooth numbers
- DEAD END: **Plimpton 322 as trigonometric table** — exhausted; modern "trigonometry" concept anachronistic for Old Babylonian period