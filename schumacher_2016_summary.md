# Schumacher 2016: Smooth Number Distribution Formulas (arXiv:1608.06928v4)

## Paper Overview
- **Title**: "The Formulas for the Distribution of the 3-Smooth, 5-Smooth, 7-Smooth and all other Smooth Numbers"
- **Author**: Raphael Schumacher (ETH Zurich)
- **Date**: 23 Oct 2016 (v4)
- **Category**: math.NT (Number Theory)

## Key Results

### 1. General Framework
The paper provides **rapidly convergent exact formulas** for counting smooth numbers:
- **N_{a,b}(x)**: Count of numbers of form a^p b^q ≤ x (2 parameters)
- **N_{a,b,c}(x)**: Count of numbers of form a^p b^q c^l ≤ x (3 parameters)
- **N_{a,b,c,d}(x)**: Count of numbers of form a^p b^q c^l d^f ≤ x (4 parameters)
- **N_{a₁,...,aₙ}(x)**: General formula for n parameters

All formulas are proven using **Perron's formula** and residue calculus on the Dirichlet series:
```
∑ χ_{S}(k) / k^s = ∏_{i=1}^n 1/(1 - e^{-log(a_i)s})
```

### 2. Leading Asymptotic Terms (Main Approximations)

#### 2-smooth (powers of 2): N₂(x)
```
N₂(x) = log(x)/log(2) + 1/2 - B₁*(log(x)/log(2))
```
where B₁*(x) = {x} - 1/2 (periodic Bernoulli function)

#### 3-smooth (2^p 3^q): N_{2,3}(x)
**Ramanujan's approximation (first term)**:
```
N_{2,3}(x) ≈ ½ [log(2x)log(3x)/(log(2)log(3))] + ½ χ_{S_{2,3}}(x)
```

**Full formula (Corollary 3)**:
```
N_{2,3}(x) = 
  ½ [log(2x)/log(2) + log(3x)/log(3) + 1/(4 log(2)) + 1/(4 log(3))]
  + 1/(12 log(3)) B₁*(log(x)/log(3)) + 1/(12 log(2)) B₁*(log(x)/log(2))
  + 1/8 [log(2)/log(3) + log(3)/log(2)]
  - B₂(log(x)/(2 log(3))) - B₂(log(x)/(2 log(2)))
  + double sum over m,n of cos(2πm log(x)/log(2)) cos(2πn log(x)/log(3)) / (m² log(3)² + n² log(2)²)
  + ½ χ_{S_{2,3}}(x)
```

**Hardy-Littlewood version (Corollary 4)**:
```
N_{2,3}(x) = ½ [log(2x)log(3x)/(log(2)log(3))] + ½ [log(x)/(2 log(2)) + log(x)/(2 log(3))]
  - B₁*(log(x)/log(2)) - B₁*(log(x)/log(3))
  + (1/π) ∑_{k=1}^∞ [cos(2πk(log(x)-½log(3))/log(2)) + cos(2πk(log(x)-½log(2))/log(3))] / (k sin(πk log(3)/log(2)) sin(πk log(2)/log(3)))
  + ½ χ_{S_{2,3}}(x)
```

#### 5-smooth (2^p 3^q 5^l): N_{2,3,5}(x)
**Ramanujan's approximation**:
```
N_{2,3,5}(x) ≈ (√3 log³x) / (6 log(2) log(3) log(5)) + ½ χ_{S_{2,3,5}}(x)
```

**Full formula (Corollary 8)** - Main polynomial part:
```
N_{2,3,5}(x) = 
  log³x / (6 log(2) log(3) log(5))
+ log²x [1/(4 log(2) log(3)) + 1/(4 log(2) log(5)) + 1/(4 log(3) log(5))]
+ log x [1/(4 log(2)) + 1/(4 log(3)) + 1/(4 log(5)) 
         + 1/(12 log(3) log(5)) + 1/(12 log(2) log(5)) + 1/(12 log(2) log(3))]
+ 1/8 [1/log(2) + 1/log(3) + 1/log(5) + log(2)/(24 log(3)) + log(2)/(24 log(5)) + ...]
- 1/8 B₁*(log(x)/log(2)) - 1/8 B₁*(log(x)/log(3)) - 1/8 B₁*(log(x)/log(5))
+ multiple cosine/sine series (6 double sums + 4 triple sums)
+ χ_{S_{2,3,5}}(x)
```

#### 7-smooth (2^p 3^q 5^l 7^f): N_{2,3,5,7}(x)
**Full formula (Corollary 10)** - Main polynomial part:
```
N_{2,3,5,7}(x) = 
  log⁴x / (24 log(2) log(3) log(5) log(7))
+ log³x [sum over 4 combinations of 3 primes / (12 Π log(p))]
+ log²x [sum over 6 combinations of 2 primes / (8 Π log(p)) + sum over 4 combinations of 3 primes / (24 Π log(p))]
+ log x [sum over 4 primes / (8 log(p)) + sum over 6 pairs / (24 log(p_i) log(p_j)) + sum over 4 triples / (48 log(p_i) log(p_j) log(p_k))]
+ constant terms [1/16 + 1/48 Σ 1/log(p) + 1/144 Σ 1/(log(p_i) log(p_j)) - 1/720 Σ 1/(log(p_i)³) + ...]
- 1/8 B₁*(log(x)/log(2)) - 1/8 B₁*(log(x)/log(3)) - 1/8 B₁*(log(x)/log(5)) - 1/8 B₁*(log(x)/log(7))
+ 6 double cosine sums + 12 triple sine/cosine sums + 4 quadruple sums
+ χ_{S_{2,3,5,7}}(x)
```

### 3. Convergence Behavior

| Smooth Type | Terms Needed for ~10¹⁰ precision | Convergence Rate |
|-------------|-----------------------------------|------------------|
| N_{2,3}(x)  | (n,m) = (2000, 2000) for x≈3.5M   | Very rapid       |
| N_{2,3}(x) HL | R=24000 for x≈348M             | Very rapid       |
| N_{2,3,5}(x) | R=20000 for x≈1.7M            | Very rapid       |
| N_{2,3,5,7}(x)| R=9000 for x=10¹⁰            | Very rapid       |

The formulas converge **extremely rapidly** — only dozens to hundreds of terms needed for high precision even at large x.

### 4. Computational Algorithm (Exact Counting)
For practical computation without series, use the exact summation:
```
N_{a,b}(x) = 1 + ∑_{j=0}^{⌊log_b(x)⌋} ⌊log_a(x/b^j)⌋ + ⌊log_b(x)⌋
```

For 3-smooth:
```
N_{2,3}(x) = 1 + ∑_{j=0}^{⌊log_3(x)⌋} ⌊log_2(x/3^j)⌋ + ⌊log_3(x)⌋
```

For 5-smooth:
```
N_{2,3,5}(x) = ∑_{k=0}^{⌊log_2(x)⌋} ∑_{l=0}^{⌊log_3(x/2^k)⌋} ⌊log_5(x/(2^k 3^l))⌋ + 1
```

## Application to FFT Size Selection

### Base-12 FFT (2^a · 3^b)
The 3-smooth numbers **ARE** the valid FFT sizes for base-12 (radix-2 and radix-3 only).
- Formula N_{2,3}(x) gives exact count of valid sizes ≤ x
- Can predict: "How many base-12 FFT sizes exist below N?"
- Can find: "What is the k-th 3-smooth number?" (inverse problem)
- Optimal size near target T: Find largest 3-smooth ≤ T, or nearest 3-smooth to T

### Base-60 FFT (2^a · 3^b · 5^c)
The 5-smooth numbers **ARE** the valid FFT sizes for base-60 (radix-2, 3, 5).
- Formula N_{2,3,5}(x) gives exact count of valid sizes ≤ x
- Tables in paper show: N_{2,3,5}(10¹⁰) = 1,697,191 sizes
- Can predict density of valid sizes at any scale

### Practical Algorithm for Optimal FFT Size
Given target length T:
1. **Enumerate**: Generate all 3-smooth (or 5-smooth) numbers near T using the exact sum formula
2. **Select**: Choose size minimizing |N - T| / T (relative error) or computational cost model
3. **Density estimate**: Use leading term log³(T)/(6 log 2 log 3 log 5) for 5-smooth to know how many candidates exist

### Example: Base-60 FFT sizes near 10⁶
From Table 3: N_{2,3,5}(10⁶) = 507
So there are 507 valid base-60 FFT sizes ≤ 1,000,000.
Average gap ≈ 10⁶ / 507 ≈ 1972.

### Inverse Problem (Finding k-th smooth number)
The paper doesn't directly give inverse, but one can:
1. Use N_{a,b,c}(x) ≈ leading term to get initial guess x₀
2. Refine via Newton/binary search using exact N_{a,b,c}(x) evaluation
3. For large x, leading term dominates:
   - 3-smooth: x ≈ exp(√(2 log 2 log 3 · N))
   - 5-smooth: x ≈ exp((6 log 2 log 3 log 5 · N)^{1/3})
   - 7-smooth: x ≈ exp((24 log 2 log 3 log 5 log 7 · N)^{1/4})

## Key Constants for Base-60 (5-smooth)
```
log(2) ≈ 0.693147
log(3) ≈ 1.098612
log(5) ≈ 1.609438

Leading coefficient: 1/(6 log 2 log 3 log 5) ≈ 1/(6 × 0.693 × 1.099 × 1.609) ≈ 0.130
```

## Summary for Experiment D (FFT Benchmarks)
- **3-smooth formula** → exact count of base-12 FFT sizes
- **5-smooth formula** → exact count of base-60 FFT sizes
- **7-smooth formula** → exact count of base-420 (2·3·5·7) FFT sizes
- All formulas converge rapidly (dozens to hundreds of terms for high precision)
- Exact summation formulas available for direct computation without series
- Leading asymptotic terms sufficient for density estimation and initial guesses