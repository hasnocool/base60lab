# Base60Research — Project Index

## Repository Structure
```
base12-base60-laboratory/
├── RESEARCH_PAPER.md          # Research paper (Markdown)
├── RESEARCH_PAPER.html        # Research paper (HTML)
├── RESEARCH_PAPER.pdf         # Research paper (PDF)
├── INDEX.md                   # This file
├── INDEX_ENHANCED.md          # Enhanced index with keywords & cross-references
├── IMPLEMENTATION_STATUS.md   # Implementation status
├── PLAN.md                    # Original research proposal (871 lines)
├── pyproject.toml             # Package config (Python 3.12+, pytest, sympy, numpy, scipy, mpmath, matplotlib, pandas)
├── .gitignore                 # Git ignore rules
├── src/base60lab/             # Python package (11 modules)
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
├── experiments/               # 36 experiment scripts
│   ├── 01_fraction_analysis.py
│   ├── 02_geometry_analysis.py
│   ├── 03_trigonometry_analysis.py
│   ├── 04_modular_patterns.py
│   ├── 05_algebra_sequences.py
│   ├── 06_harmonic_analysis.py
│   ├── 07_lissajous_analysis.py
│   ├── 08_fft_benchmarks.py
│   ├── 09_real_world_signals.py
│   ├── 10_combined_experiments.py
│   ├── 15_babylonian_reciprocals.py
│   ├── 16_smooth_fft_prediction.py
│   ├── 17_direct_base_conversion.py
│   ├── 18_modular_forms_qseries.py
│   ├── 20_lissajous_3d.py
│   ├── 21_cognitive_load_mitigation.py
│   ├── 22_ntt_smooth_moduli.py
│   ├── 23_continued_fractions.py
│   ├── 24_kuramoto_sync.py
│   ├── 25_constructible_polygons.py
│   ├── 26_resonance_webs.py
│   ├── 27_qft_circuit.py
│   ├── 28_cordic_edge.py
│   ├── 29_rns_pqc.py
│   ├── 30_wave_solver.py
│   ├── 31_timeseries.py
│   ├── 32_education.py
│   ├── 33_mrrope.py
│   ├── 34_rns_mrud.py
│   ├── 35_cordic.py
│   └── 36_ntt_pqc.py
├── docs/                      # Documentation
│   ├── RESEARCH_PLAN.md
│   ├── HYPOTHESES.md
│   ├── EXPERIMENT_PROTOCOLS.md
│   ├── RESULTS.md
│   └── findings/              # 51 finding files + CHANGELOG.md
├── data/                      # Empty (git-ignored)
├── results/                   # Experiment outputs (git-ignored)
├── experiments/wasm/          # Babylonian education visualizer (Rust→WASM→React)
└── smooth_fft_sizes.py        # Schumacher 2016 smooth number module
```

## Keyword Index (Cross-Reference)

### By Research Domain
| Domain | Keywords | Primary Files |
|--------|----------|---------------|
| **Exact Arithmetic** | `rational`, `exact`, `no-float`, `verified` | `src/base60lab/core/rational.py`, `core-rational.md` |
| **Base Conversion** | `base10`, `base12`, `base60`, `conversion`, `decimal-intermediate` | `src/base60lab/numerals.py`, `experiment-17-direct-base-conversion.md` |
| **Harmonics & Music** | `just-intonation`, `intervals`, `cents`, `harmonics`, `temperament`, `phase` | `src/base60lab/frequency.py`, `experiment-06-harmonic-analysis.md` |
| **Signal Processing** | `fft`, `ntt`, `cordic`, `filter`, `spectral`, `5-smooth`, `mixed-radix` | `src/base60lab/signal_processing.py`, `experiment-08-fft-benchmarks.md` |
| **Wave Physics** | `wave-equation`, `kuramoto`, `synchronization`, `lissajous`, `phase-space` | `src/base60lab/wave.py`, `src/base60lab/lissajous.py` |
| **Quantum Computing** | `qudit`, `qft`, `qec`, `stabilizer`, `phase-estimation` | `src/base60lab/quantum.py`, `experiment-27-qft-circuit.md` |
| **Cryptography** | `pqc`, `kyber`, `dilithium`, `falcon`, `rns`, `ntt`, `moduli` | `src/base60lab/rns_ntt.py`, `experiment-29-rns-pqc.md` |
| **Number Theory** | `modular-forms`, `partition`, `congruence`, `ramanujan`, `delta` | `experiment-18-modular-forms.md`, `experiment-16-smooth-fft-prediction.md` |
| **Geometry & Trigonometry** | `circle`, `subdivision`, `polygon`, `trigonometry`, `exact-values` | `src/base60lab/geometry.py`, `experiment-02-geometry-analysis.md` |
| **Financial Computing** | `time-series`, `interest`, `compound-interest`, `amortization` | `src/base60lab/timeseries.py`, `experiment-31-timeseries.md` |
| **Education** | `babylonian`, `visualization`, `fraction`, `plimpton322`, `ybc7290`, `wasm` | `experiments/wasm/`, `experiment-32-education.md` |
| **Cognitive Science** | `notation`, `cognitive-load`, `usability`, `dozenal` | `experiment-21-cognitive-load.md`, `experiment-21-cognitive-load-mitigation.md` |
| **Historical Reconstruction** | `babylonian`, `plimpton322`, `ybc7290`, `sexagesimal` | `experiment-15-babylonian-reciprocals.md`, `experiment-23-babylonian-pi.md` |

### By Key Finding (with Assessment)
| Finding | Assessment | Keywords |
|---------|------------|----------|
| Base-12 composite score: 0.5126 (winner) | **Good** | `composite-score`, `base12`, `metrics` |
| Base-60 terminates 34% fractions (vs 20%/15%) | **Good** | `terminating-fractions`, `base60`, `factorization` |
| Base-60: only base with all 11 JI intervals | **Good** | `just-intonation`, `music`, `base60` |
| 5-smooth FFT: 2.7x–4.5x faster | **Good** | `fft`, `5-smooth`, `mixed-radix`, `performance` |
| Delta τ(n) mod 60 cycle: REFUTED (509/940) | **Bad** | `delta-function`, `modular-forms`, `ramanujan` |
| Partition congruences confirmed (n≤500) | **Neutral** | `partition`, `ramanujan`, `congruence` |
| Base-60 cognitive load: 116.4 vs 28.9 (base-10) | **Bad** | `cognitive-load`, `usability`, `notation` |
| No float internal arithmetic | **Good** | `exact-arithmetic`, `rational`, `verified` |
| Base-60 QFT with radix-60 butterfly | **Good** | `quantum`, `qft`, `mixed-radix`, `qudit` |
| Base-60 RNS NTT for PQC | **Good** | `rns`, `ntt`, `pqc`, `kyber`, `dilithium` |
| Exact rational wave solver (zero drift) | **Good** | `wave-equation`, `pde`, `zero-drift` |
| Sexagesimal time-series (exact finance) | **Good** | `time-series`, `finance`, `exact-arithmetic` |
| Babylonian education visualizer (WASM) | **Good** | `education`, `babylonian`, `wasm`, `visualization` |

---

## Quick Navigation

### Source Modules (11)
- `src/base60lab/core/rational.py` — Exact rational arithmetic
- `src/base60lab/core/types.py` — Type system (Rational, Phase, FrequencyRatio, Harmonic)
- `src/base60lab/core/unknowns.py` — Unknowns tracking
- `src/base60lab/engines/base10_engine.py` — Decimal engine
- `src/base60lab/engines/base12_engine.py` — Duodecimal engine
- `src/base60lab/engines/base60_engine.py` — Sexagesimal engine
- `src/base60lab/domains/fractions.py` — Fractions domain
- `src/base60lab/angles.py` — Degrees/turns/radians
- `src/base60lab/geometry.py` — Circles/polygons/subdivisions
- `src/base60lab/trigonometry.py` — Exact trig values
- `src/base60lab/modular.py` — Modular arithmetic mod 12/60
- `src/base60lab/sequences.py` — Number sequences
- `src/base60lab/frequency.py` — Oscillations/harmonics
- `src/base60lab/lissajous.py` — Lissajous plots
- `src/base60lab/signal_processing.py` — Filters/spectral analysis
- `src/base60lab/fft_benchmarks.py` — FFT benchmarks
- `src/base60lab/metrics.py` — Base comparison metrics
- `src/base60lab/numerals.py` — Base conversion
- `src/base60lab/trigonometry.py` — Exact trig values
- `src/base60lab/lissajous.py` — Lissajous plots
- `src/base60lab/signal_processing.py` — Filters/spectral
- `src/base60lab/fft_benchmarks.py` — FFT benchmarks
- `src/base60lab/metrics.py` — Base comparison metrics
- `src/base60lab/numerals.py` — Base conversion
- `src/base60lab/quantum.py` — Qudit, QFT, QEC
- `src/base60lab/cordic.py` — CORDIC algorithms
- `src/base60lab/rns_ntt.py` — RNS NTT for PQC
- `src/base60lab/wave.py` — Wave equation solvers
- `src/base60lab/timeseries.py` — Sexagesimal time-series

### Experiments (36)
| # | Script | Domain |
|---|--------|--------|
| 01 | fraction_analysis.py | Fractions |
| 02 | geometry_analysis.py | Geometry |
| 03 | trigonometry_analysis.py | Trigonometry |
| 04 | modular_patterns.py | Modular arithmetic |
| 05 | algebra_sequences.py | Sequences |
| 06 | harmonic_analysis.py | Music/harmonics |
| 07 | lissajous_analysis.py | Lissajous/phase |
| 08 | fft_benchmarks.py | FFT performance |
| 09 | real_world_signals.py | Signal processing |
| 10 | combined_experiments.py | Multi-domain |
| 15 | babylonian_reciprocals.py | Babylonian math |
| 16 | smooth_fft_prediction.py | FFT prediction |
| 17 | direct_base_conversion.py | Base conversion |
| 18 | modular_forms_qseries.py | Modular forms |
| 20 | lissajous_3d.py | 3D Lissajous |
| 21 | cognitive_load_mitigation.py | Cognitive load |
| 22 | ntt_smooth_moduli.py | NTT/moduli |
| 23 | continued_fractions.py | Continued fractions |
| 24 | kuramoto_sync.py | Synchronization |
| 25 | constructible_polygons.py | Polygons |
| 26 | resonance_webs.py | Resonance |
| 27 | qft_circuit.py | Quantum QFT |
| 28 | cordic_edge.py | CORDIC |
| 29 | rns_pqc.py | RNS NTT/PQC |
| 30 | wave_solver.py | Wave equation |
| 31 | timeseries.py | Time-series DB |
| 32 | education.py | Education/WASM |
| 33 | mrrope.py | Position encoding |
| 34 | rns_mrud.py | RNS MRUD |
| 35 | cordic.py | CORDIC convergence |
| 36 | ntt_pqc.py | NTT PQC support |

### Documentation
- `docs/RESEARCH_PLAN.md` — Research plan
- `docs/HYPOTHESES.md` — Hypotheses H1–H5
- `docs/EXPERIMENT_PROTOCOLS.md` — Experiment protocols
- `docs/RESULTS.md` — Aggregated results
- `docs/findings/` — 51 finding files + CHANGELOG.md

### Research Paper (3 Formats)
- `RESEARCH_PAPER.md` — Markdown source
- `RESEARCH_PAPER.html` — HTML with Bootstrap
- `RESEARCH_PAPER.pdf` — PDF via reportlab

### Enhanced Index
- `INDEX_ENHANCED.md` — Full keyword index with cross-references

---

## Key Results Summary

| Finding | Result | Verified |
|---------|--------|----------|
| Base-12 composite score | 0.5126 (winner) | ✅ Exact rational |
| Base-60 terminating fractions | 34% (vs 20%/15%) | ✅ Computed |
| Base-60 just intonation | 11/11 intervals terminate | ✅ Computed |
| 5-smooth FFT speedup | 2.7x–4.5x faster | ✅ Executed (9 targets) |
| Delta τ(n) mod 60 cycle | REFUTED (509/940) | ✅ Executed |
| Partition congruences | All three CONFIRMED | ✅ Executed (n≤500) |
| No float internal arithmetic | Confirmed | ✅ Grep verified |

---

## Test Commands
```bash
# Full test suite with coverage gate
pytest --cov=src/base60lab --cov-fail-under=95 -v

# Run all experiments
for f in experiments/01_*.py experiments/02_*.py ... experiments/36_*.py; do python "$f"; done

# Verify specific claims
python verify_partition_congruence.py
python verify_smooth_fft_claim.py
python verify_delta_mod60.py

# Build paper
pandoc RESEARCH_PAPER.md -o RESEARCH_PAPER.html --standalone --toc --css=https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
python3 -c "
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# ... (see RESEARCH_PAPER.md for full script)
"
```

---

## Keywords for Search

**Core**: `rational`, `exact-arithmetic`, `base60`, `base12`, `base10`, `sexagesimal`, `duodecimal`, `decimal`

**Applications**: `signal-processing`, `fft`, `ntt`, `cordic`, `rns`, `pqc`, `quantum`, `qft`, `qec`, `finance`, `education`, `music`, `geometry`, `wave-equation`, `synchronization`, `cryptography`, `history`, `education`

**Properties**: `exact`, `verified`, `refuted`, `neutral`, `good`, `bad`, `breakthrough`, `implementation`, `visualization`, `wasm`, `reproducible`

---

*See `INDEX_ENHANCED.md` for full alphabetical keyword index and cross-reference matrix.*