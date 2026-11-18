# Base60Research — Project Index

## Repository Structure

```
base12-base60-laboratory/
├── RESEARCH_PAPER.md          # Research paper (Markdown)
├── RESEARCH_PAPER.html        # Research paper (HTML)
├── RESEARCH_PAPER.pdf         # Research paper (PDF)
├── INDEX.md                   # This file
├── IMPLEMENTATION_STATUS.md   # Implementation status
├── PLAN.md                    # Original research proposal (871 lines)
├── pyproject.toml             # Package configuration
├── .gitignore                 # Git ignore rules
├── src/base60lab/             # Python package
│   ├── __init__.py            # Public exports (all 11 modules)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── rational.py        # Exact rational arithmetic
│   │   ├── types.py           # BaseNumber, Expression, Notation, Function
│   │   └── unknowns.py        # UnknownsRegistry
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── base10_engine.py   # Decimal engine
│   │   ├── base12_engine.py   # Duodecimal engine
│   │   └── base60_engine.py   # Sexagesimal engine
│   ├── domains/
│   │   ├── __init__.py
│   │   └── fractions.py       # FractionsDomain
│   ├── angles.py              # Degrees/turns/radians
│   ├── geometry.py            # Circles/polygons/subdivisions
│   ├── trigonometry.py        # Exact trig values
│   ├── modular.py             # Modular arithmetic mod 12/60
│   ├── sequences.py           # Number sequences
│   ├── frequency.py           # Oscillations/harmonics
│   ├── lissajous.py           # Lissajous plots
│   ├── signal_processing.py   # Filters/spectral analysis
│   ├── fft_benchmarks.py      # FFT performance benchmarks
│   ├── metrics.py             # Base comparison metrics
│   └── numerals.py            # Base conversion utilities
├── tests/                     # 761 tests, 97.92% coverage
│   ├── test_core/
│   ├── test_engines/
│   └── test_domains/
├── experiments/               # 10 experiment scripts
│   ├── 01_fraction_analysis.py
│   ├── 02_geometry_analysis.py
│   ├── 03_trigonometry_analysis.py
│   ├── 04_modular_patterns.py
│   ├── 05_algebra_sequences.py
│   ├── 06_harmonic_analysis.py
│   ├── 07_lissajous_analysis.py
│   ├── 08_fft_benchmarks.py
│   ├── 09_real_world_signals.py
│   └── 10_combined_experiments.py
├── docs/                      # Documentation
│   ├── RESEARCH_PLAN.md
│   ├── HYPOTHESES.md
│   ├── EXPERIMENT_PROTOCOLS.md
│   ├── RESULTS.md
│   └── findings/              # 29 finding files + CHANGELOG.md
├── data/                      # Empty (git-ignored)
├── results/                   # Experiment outputs (git-ignored)
└── smooth_fft_sizes.py        # Schumacher 2016 smooth number module
```

## Key Results Summary

| Finding | Result | Verified |
|---------|--------|----------|
| Base-12 composite score | 0.5126 (winner) | ✅ Exact rational |
| Base-60 terminating fractions | 34% (vs 20% base-12, 15% base-10) | ✅ Computed |
| Base-60 just intonation | 11/11 intervals terminate (only base) | ✅ Computed |
| 5-smooth FFT speedup | 2.7x–4.5x faster | ✅ Executed (9 targets) |
| Delta τ(n) mod 60 cycle | REFUTED (509/940 mismatches) | ✅ Executed |
| Partition congruences | All three CONFIRMED | ✅ Executed (n≤500) |
| No float internal arithmetic | Confirmed | ✅ Grep verified |

## Test Commands

```bash
# Full test suite with coverage gate
pytest --cov=src/base60lab --cov-fail-under=95 -v

# Run all experiments
for f in experiments/01_*.py experiments/10_combined_experiments.py; do python "$f"; done

# Verify specific claims
python verify_partition_congruence.py
python verify_smooth_fft_claim.py
python verify_delta_mod60.py
```
