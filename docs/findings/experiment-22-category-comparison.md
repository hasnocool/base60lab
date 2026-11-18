# Experiment 22: Category Comparison Findings

## Finding Metadata
- **finding_id**: F-18
- **statement**: Category comparison shows base-60 dominates 2_3_5_smooth category; digit length distributions favor base-60 for 5-smooth numbers
- **assessment**: Neutral — Descriptive statistics for system design
- **plain_language_explanation**: When you categorize numbers by their prime factors, base-60 dominates the "5-smooth" category (numbers with only 2,3,5 as factors) because its factorization exactly matches. Digit lengths are shortest in base-60 for these numbers.
- **why_it_matters**: Informs notation design and data structure choices for systems handling 5-smooth numbers.
- **applications**:
  - Notation Design: Optimize for 5-smooth numbers
  - Information Theory: Entropy coding for 5-smooth data
  - Data Compression: Base-60 for 5-smooth datasets
- **how_to_implement**: Use base-60 for systems dominated by 5-smooth numbers (time, angles, harmonics)
- **what_graphs_show**:
  - Figure 6.101: Category comparison — base-60 dominates 5-smooth
  - Figure 6.102: Digit length distribution — base-60 shortest for 5-smooth
  - Figure 6.103: Moduli per category — for RNS design
  - Figure 6.104: p-1 smoothness — relevant for crypto
- **breakthrough_ideas**:
  - Base-60 entropy coding for exact rational compression
  - Base-60 optimized data structures for 5-smooth data
- **risk_level**: Low
- **maturity**: Validated
- **readiness_timeline**: Near-term

## Summary
Category comparison and digit length distributions for number classes across bases.

## Category Comparison
| Category | Base-10 | Base-12 | Base-60 |
|----------|---------|---------|---------|
| 2_3_5_smooth | Poor | Good | **Best** |
| prime_7_11_13 | Poor | Poor | Poor |
| mixed | Medium | Medium | Medium |

## Digit Length Distribution
| Class | Base-10 Avg | Base-12 Avg | Base-60 Avg |
|-------|-------------|-------------|-------------|
| 2_3_5_smooth | Long | Medium | **Shortest** |
| prime_7_11_13 | Long | Long | Long |
| mixed | Long | Medium | Medium |

## Moduli per Category
For RNS design, base-60 provides most moduli options for 2_3_5_smooth category.

## p-1 Smoothness
Relevant for cryptographic prime generation — base-60 primes have p-1 with factors {2,3,5}.

## Controls Verified
✅ Category statistics computed across all bases
✅ Independent verification via category comparison module
✅ Equal conditions (same number set for all bases)