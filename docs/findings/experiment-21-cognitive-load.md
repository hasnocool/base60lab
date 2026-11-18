# Experiment 21: Cognitive Load & Notation Studies Findings

## Finding Metadata
- **finding_id**: F-17
- **statement**: Base-60 cognitive load 116.4 vs base-10 28.9 (4× higher); base-12 composite score 0.5126 wins overall balance
- **assessment**: **Bad** for base-60 human usability; **Good** for base-12 balance
- **plain_language_explanation**: Base-60 requires memorizing 60 symbols and a 3,600-entry multiplication table (42× harder than base-10). Base-12 only needs 12 symbols and 144-entry table — learnable by humans. Base-12 wins the overall balance score (0.5126) combining math power and human usability.
- **why_it_matters**: Human factors determine adoption. Base-60 is for machines; base-12 is for humans. Hybrid architecture: base-12 display, base-60 internal.
- **applications**:
  - Education: Base-12 as "dozenal" curriculum
  - HCI: Base-12 display, base-60 internal
  - Notation Design: Hybrid base-12/60 systems
- **how_to_implement**: Hybrid architecture — base-12 for human-facing notation, base-60 for machine-internal exact computation
- **what_graphs_show**:
  - Figure 6.23: Symbol length distribution — base-12 optimal
  - Figure 6.24: Rendering length heatmap — base-12 optimal
  - Figure 6.25: Fraction representation — base-12 efficient
  - Figure 6.26: Composite load — base-12 wins (0.5126)
  - Figure 6.27: Variant radar — base-12 balanced
- **breakthrough_ideas**:
  - AI-assisted base-60 arithmetic tutoring with visual patterns
  - Hybrid base-12/60 notation systems
  - Base-12 as universal human-facing exact arithmetic notation
- **risk_level**: High (cognitive barrier)
- **maturity**: Validated (experiment 21 complete)
- **readiness_timeline**: Near-term (6-18 months)

## Summary
Cognitive load and notation efficiency analysis across bases with 4 notation variants evaluated.

## Cognitive Load Metrics
| Base | Cognitive Load | Multiplication Table | Symbols | Composite Score |
|------|----------------|----------------------|---------|-----------------|
| 10   | 28.9 | 100 entries | 10 | 0.4417 |
| 12   | ~50  | 144 entries | 12 | **0.5126** ✅ |
| 60   | 116.4 | 3,600 entries | 60 | 0.4340 |

## Notation Variants Evaluated
| Variant | Avg Length (chars) | Bits/Char | Composite |
|---------|-------------------|-----------|-----------|
| Compact Fixed-Width | 316.1 | 1.97 | 0.847 |
| Standard Comma-Separated | 347.7 | 1.85 | 0.791 |
| Chinese Rod Numerals | 630.2 | 1.32 | 0.623 |
| Babylonian Wedge | 500+ | 1.0 | 0.50 |

## Key Findings
1. **Base-12 wins composite score (0.5126)** — best balance of math power and human usability
2. **Base-60 cognitive load 4× base-10** — 116.4 vs 28.9
3. **Base-60 multiplication table 42× complexity** — 3,600 vs 100 entries
4. **Compact fixed-width notation** most efficient (0.847 composite)
4. **Base-12 is the "sweet spot"** — 12 symbols learnable, 5-smooth factorization

## Notation Variant Analysis
| Variant | Symbols | Cognitive Load | Best For |
|---------|---------|----------------|----------|
| Compact Fixed-Width | 60 fixed-width | Medium | Machine display |
| Standard Comma-Separated | 60 comma-sep | Low | Human display |
| Chinese Rod Numerals | Variable | High | Historical |
| Babylonian Wedge | Variable | High | Historical |

## Controls Verified
✅ 4 notation variants tested
✅ Cognitive load metrics computed
✅ Independent verification via cognitive load module
✅ Equal conditions (same test cases for all variants)