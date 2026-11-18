# Base60Research — Enhanced Project Index with Keywords & Cross-References

## Quick Navigation

### By Research Domain
| Domain | Keywords | Primary Files |
|--------|----------|---------------|
| **Exact Arithmetic** | `rational`, `exact`, `no-float`, `verified` | `src/base60lab/core/rational.py`, `core-rational.md` |
| **Base Conversion** | `base10`, `base12`, `base60`, `conversion`, `decimal-intermediate` | `src/base60lab/numerals.py`, `experiment-17-direct-base-conversion.md` |
| **Harmonics & Music** | `just-intonation`, `intervals`, `cents`, `harmonics`, `temperament`, `phase` | `src/base60lab/frequency.py`, `experiment-06-harmonic-analysis.md`, `experiment-15-babylonian-reciprocals.md` |
| **Signal Processing** | `fft`, `ntt`, `cordic`, `filter`, `spectral`, `5-smooth`, `mixed-radix` | `src/base60lab/signal_processing.py`, `src/base60lab/fft_benchmarks.py`, `experiment-08-fft-benchmarks.md`, `experiment-09-real-world-signals.md` |
| **Wave Physics** | `wave-equation`, `kuramoto`, `synchronization`, `lissajous`, `phase-space`, `knot-theory` | `src/base60lab/wave.py`, `src/base60lab/lissajous.py`, `experiment-20-lissajous-3d.md`, `experiment-24-synchronization.md` |
| **Quantum Computing** | `qudit`, `qft`, `qec`, `stabilizer`, `phase-estimation`, `mixed-radix` | `src/base60lab/quantum.py`, `experiment-27-qft-circuit.md`, `experiment-36-ntt-pqc.md` |
| **Cryptography** | `pqc`, `kyber`, `dilithium`, `falcon`, `rns`, `ntt`, `post-quantum`, `moduli` | `src/base60lab/rns_ntt.py`, `experiment-29-rns-pqc.md`, `experiment-36-ntt-pqc.md` |
| **Number Theory** | `modular-forms`, `partition`, `congruence`, `ramanujan`, `delta`, `tau-function` | `experiment-18-modular-forms.md`, `experiment-16-smooth-fft-prediction.md` |
| **Geometry & Trigonometry** | `circle`, `subdivision`, `polygon`, `trigonometry`, `exact-values`, `angles` | `src/base60lab/geometry.py`, `src/base60lab/trigonometry.py`, `experiment-02-geometry-analysis.md`, `experiment-03-trigonometry-analysis.md` |
| **Financial Computing** | `time-series`, `interest`, `compound-interest`, `amortization`, `exact-finance` | `src/base60lab/timeseries.py`, `experiment-31-timeseries.md` |
| **Education** | `babylonian`, `visualization`, `fraction`, `plimpton322`, `ybc7290`, `wasm` | `experiments/wasm/`, `experiment-15-babylonian-reciprocals.md`, `experiment-32-education.md` |
| **Cognitive Science** | `notation`, `cognitive-load`, `usability`, `dozenal`, `human-factors` | `experiment-21-cognitive-load.md`, `experiment-21-cognitive-load-mitigation.md` |
| **Historical Reconstruction** | `babylonian`, `plimpton322`, `ybc7290`, `sexagesimal`, `history-of-math` | `experiment-15-babylonian-reciprocals.md`, `experiment-23-babylonian-pi.md`, `experiment-25-constructible-polygons.md` |

### By Artifact Type
| Type | Keywords | Location |
|------|----------|----------|
| **Source Modules** | `module`, `implementation`, `api`, `src` | `src/base60lab/` (11 modules) |
| **Experiments** | `experiment`, `script`, `reproducible`, `verification` | `experiments/` (36 scripts) |
| **Tests** | `test`, `verification`, `coverage`, `pytest` | `tests/` (761 tests, 97.92% coverage) |
| **Finding Reports** | `finding`, `assessment`, `good/bad/neutral`, `breakthrough` | `docs/findings/` (51 files) |
| **Documentation** | `docs`, `protocol`, `plan`, `results` | `docs/` (5 files + findings/) |
| **Research Paper** | `paper`, `markdown`, `html`, `pdf`, `publication` | `RESEARCH_PAPER.{md,html,pdf}` |
| **Visualizations** | `svg`, `png`, `plot`, `figure`, `results` | `results/experiment_XX/`, `docs/findings/*.svg` |
| **Build/Config** | `config`, `build`, `pyproject`, `venv` | `pyproject.toml`, `.gitignore` |

---

## 🏷️ Keyword Index (Alphabetical)

### A
- **algebraic-sequences** → `sequences-number-patterns.md`, `experiment-05-algebra-sequences.md`, `src/base60lab/sequences.py`
- **amortization** → `experiment-31-timeseries.md`, `src/base60lab/timeseries.py`
- **angles** → `angles-circle-subdivisions.md`, `src/base60lab/angles.py`, `experiment-02-geometry-analysis.md`
- **arbitrary-precision** → `core-rational.md`, `src/base60lab/core/rational.py`
- **api** → `src/base60lab/__init__.py`, all module `__init__.py`

### B
- **babylonian** → `experiment-15-babylonian-reciprocals.md`, `experiment-23-babylonian-pi.md`, `experiment-25-constructible-polygons.md`, `experiments/wasm/`
- **base-conversion** → `numerals-base-conversion.md`, `experiment-17-direct-base-conversion.md`, `src/base60lab/numerals.py`
- **base10** → `engines-base10.md`, `src/base60lab/engines/base10_engine.py`
- **base12** → `engines-base12.md`, `src/base60lab/engines/base12_engine.py`
- **base60** → `engines-base60.md`, `src/base60lab/engines/base60_engine.py`
- **beat-frequencies** → `experiment-06-harmonic-analysis.md`, `src/base60lab/frequency.py`
- **breakthrough-ideas** → All finding files (section: Breakthrough Ideas)

### C
- **carry-free** → `experiment-29-rns-pqc.md`, `experiment-34-rns-mrud.md`, `src/base60lab/rns_ntt.py`
- **cellular-automata** → (planned) 
- **chord** → `frequency-ratios-harmonics.md`, `experiment-06-harmonic-analysis.md`
- **circular-membrane** → `experiment-30-wave-solver.md`, `src/base60lab/wave.py`
- **clifford-algebra** → (planned)
- **cognitive-load** → `experiment-21-cognitive-load.md`, `experiment-21-cognitive-load-mitigation.md`
- **compound-interest** → `experiment-31-timeseries.md`, `src/base60lab/timeseries.py`
- **continued-fractions** → `experiment-23-babylonian-pi.md`, `src/base60lab/trigonometry.py`
- **cordic** → `experiment-28-cordic-edge.md`, `experiment-35-cordic.md`, `src/base60lab/cordic.py`
- **crypto** → `experiment-29-rns-pqc.md`, `experiment-36-ntt-pqc.md`, `experiment-32-education.md` (perfect secrecy)
- **cyclic-groups** → `modular-arithmetic-cyclic.md`, `src/base60lab/modular.py`

### D
- **delta-function** → `experiment-18-modular-forms.md`, `verify_delta_mod60.py`
- **diophantine** → `experiment-20-lissajous-3d.md`, `experiment-26-resonance-webs.md`
- **discrete-fourier** → `experiment-08-fft-benchmarks.md`, `experiment-16-smooth-fft-prediction.md`

### E
- **education** → `experiment-32-education.md`, `experiments/wasm/`
- **engines** → `engines-base10.md`, `engines-base12.md`, `engines-base60.md`, `src/base60lab/engines/`
- **equal-temperament** → `experiment-06-harmonic-analysis.md`, `frequency-ratios-harmonics.md`
- **exact-arithmetic** → `core-rational.md`, `core-types.md`, `src/base60lab/core/rational.py`
- **experiments** → `experiments/` (36 scripts)

### F
- **factorization** → All base engines, `metrics-comparison-report.md`
- **fft** → `experiment-08-fft-benchmarks.md`, `experiment-16-smooth-fft-prediction.md`, `src/base60lab/fft_benchmarks.py`
- **finding** → All `docs/findings/*.md` (51 files)
- **finite-element** → `experiment-30-wave-solver.md` (planned)
- **fraction** → `domains-fractions.md`, `experiment-01-fraction-analysis.md`, `src/base60lab/domains/fractions.py`

### G
- **garner-algorithm** → `experiment-29-rns-pqc.md`, `src/base60lab/rns_ntt.py`
- **geometry** → `geometry-polygon-subdivisions.md`, `experiment-02-geometry-analysis.md`, `src/base60lab/geometry.py`
- **guitar** → (planned)

### H
- **harmonic-analysis** → `experiment-06-harmonic-analysis.md`, `frequency-ratios-harmonics.md`
- **harmonics** → `experiment-06-harmonic-analysis.md`, `experiment-10-combined-experiments.md`
- **higher-dimensions** → `experiment-20-lissajous-3d.md`, `experiment-26-resonance-webs.md`
- **historical-math** → `experiment-15-babylonian-reciprocals.md`, `experiment-23-babylonian-pi.md`

### I
- **implementation** → `IMPLEMENTATION_STATUS.md`, `src/base60lab/`
- **interest** → `experiment-31-timeseries.md`, `src/base60lab/timeseries.py`
- **interpolation** → (planned)
- **intervals** → `frequency-ratios-harmonics.md`, `experiment-06-harmonic-analysis.md`

### J
- **just-intonation** → `frequency-ratios-harmonics.md`, `experiment-06-harmonic-analysis.md`, `experiment-15-babylonian-reciprocals.md`

### K
- **knot-theory** → `experiment-20-lissajous-3d.md`, `experiment-26-resonance-webs.md`
- **kuramoto** → `experiment-24-synchronization.md`, `src/base60lab/wave.py`

### L
- **lissajous** → `experiment-07-lissajous-analysis.md`, `experiment-20-lissajous-3d.md`, `src/base60lab/lissajous.py`
- **loan** → `experiment-31-timeseries.md`, `src/base60lab/timeseries.py`

### M
- **machine-learning** → `experiment-34-rns-mrud.md` (ML features for modular forms)
- **metrics** → `metrics-comparison-report.md`, `src/base60lab/metrics.py`
- **micro-angles** → `experiment-35-cordic.md`, `experiment-28-cordic-edge.md`
- **mixed-radix** → `experiment-16-smooth-fft-prediction.md`, `experiment-27-qft-circuit.md`, `experiment-33-mrrope.md`, `experiment-36-ntt-pqc.md`

### N
- **notation** → `experiment-21-cognitive-load.md`, `experiment-21-cognitive-load-mitigation.md`, `experiment-26-resonance-webs.md`
- **ntt** → `experiment-29-rns-pqc.md`, `experiment-36-ntt-pqc.md`, `src/base60lab/rns_ntt.py`
- **number-theory** → `experiment-18-modular-forms.md`, `modular-arithmetic-cyclic.md`

### P
- **phase** → `lissajous-phase-closure.md`, `experiment-07-lissajous-analysis.md`, `experiment-24-synchronization.md`
- **phase-estimation** → `experiment-27-qft-circuit.md`, `src/base60lab/quantum.py`
- **plimpton322** → `experiment-15-babylonian-reciprocals.md`, `experiment-32-education.md`
- **post-quantum** → `experiment-29-rns-pqc.md`, `experiment-36-ntt-pqc.md`
- **prime-factors** → All base engines, `metrics-comparison-report.md`
- **primes** → `experiment-29-rns-pqc.md`, `src/base60lab/rns_ntt.py`

### Q
- **qec** → `experiment-27-qft-circuit.md`, `src/base60lab/quantum.py`
- **qft** → `experiment-27-qft-circuit.md`, `experiment-36-ntt-pqc.md`, `src/base60lab/quantum.py`
- **quantum** → `experiment-27-qft-circuit.md`, `experiment-36-ntt-pqc.md`, `src/base60lab/quantum.py`
- **qudit** → `experiment-27-qft-circuit.md`, `src/base60lab/quantum.py`

### R
- **rational** → `core-rational.md`, `src/base60lab/core/rational.py`
- **resonance** → `experiment-26-resonance-webs.md`, `experiment-20-lissajous-3d.md`
- **rns** → `experiment-29-rns-pqc.md`, `experiment-34-rns-mrud.md`, `src/base60lab/rns_ntt.py`

### S
- **scheduling** → (planned)
- **sequences** → `sequences-number-patterns.md`, `experiment-05-algebra-sequences.md`
- **signal-processing** → `experiment-09-real-world-signals.md`, `src/base60lab/signal_processing.py`
- **signal** → `experiment-09-real-world-signals.md`, `signal-processing-spectral.md`
- **signal-processing** → `signal-processing-spectral.md`, `src/base60lab/signal_processing.py`
- **smooth-numbers** → `experiment-16-smooth-fft-prediction.md`, `experiment-08-fft-benchmarks.md`, `smooth_fft_sizes.py`
- **spectral** → `experiment-08-fft-benchmarks.md`, `experiment-09-real-world-signals.md`
- **subdivisions** → `angles-circle-subdivisions.md`, `geometry-polygon-subdivisions.md`
- **synchronization** → `experiment-24-synchronization.md`, `src/base60lab/wave.py`

### T
- **tag** → All finding files (11-field frontmatter)
- **temperament** → `experiment-06-harmonic-analysis.md`, `frequency-ratios-harmonics.md`
- **time-series** → `experiment-31-timeseries.md`, `src/base60lab/timeseries.py`
- **trigonometry** → `trigonometry-exact-values.md`, `experiment-03-trigonometry-analysis.md`
- **truth** → All findings (verified/refuted/neutral)

### V
- **verification** → `verify_*.py`, `tests/`, `docs/findings/*.md` (assessment field)
- **visualization** → `results/`, `docs/findings/*.svg`, `experiments/wasm/www/`

### W
- **wave** → `experiment-24-synchronization.md`, `experiment-30-wave-solver.md`, `src/base60lab/wave.py`
- **wave-equation** → `experiment-30-wave-solver.md`, `src/base60lab/wave.py`
- **wasm** → `experiments/wasm/`, `experiment-32-education.md`

### Y
- **ybc7290** → `experiment-23-babylonian-pi.md`, `experiment-15-babylonian-reciprocals.md`

---

## 🔗 Cross-Reference Matrix

### Module ↔ Experiment ↔ Finding
| Module | Key Experiments | Core Findings |
|--------|----------------|---------------|
| `rational.py` | All experiments | `core-rational.md` (F-29) |
| `numerals.py` | 01, 17 | `numerals-base-conversion.md` (F-20) |
| `frequency.py` | 06, 07, 10, 15 | `frequency-ratios-harmonics.md` (F-26) |
| `lissajous.py` | 07, 10, 20, 26 | `lissajous-phase-closure.md` (F-27) |
| `signal_processing.py` | 08, 09, 16 | `signal-processing-spectral.md` (F-24) |
| `fft_benchmarks.py` | 08, 16 | `fft-benchmarks-performance.md` (F-36) |
| `modular.py` | 04, 18, 22 | `modular-arithmetic-cyclic.md` (F-28) |
| `wave.py` | 24, 30 | (new finding) |
| `timeseries.py` | 31 | (new finding) |
| `quantum.py` | 27, 36 | (new finding) |
| `cordic.py` | 28, 35 | (new finding) |
| `rns_ntt.py` | 29, 34, 36 | (new finding) |
| `wave.py` | 24, 30 | (new finding) |
| `timeseries.py` | 31 | (new finding) |

### Experiment ↔ Hypothesis ↔ Finding
| Experiment | Tests Hypothesis | Produces Finding |
|------------|-----------------|------------------|
| 01 | H1 (base efficiency) | F-20, F-20 |
| 02 | H2 (circle subdivisions) | F-22 |
| 03 | H2 (trigonometry) | F-23 |
| 04 | H1 (modular patterns) | F-28 |
| 05 | H1 (sequences) | F-25 |
| 06 | H3 (JI termination) | F-26, F-26 |
| 07 | H3 (Lissajous closure) | F-27 |
| 08 | H4 (FFT smoothness) | F-36 |
| 09 | H4 (signal processing) | F-24 |
| 10 | H5 (multi-base) | F-21 |
| 15 | H1 (Babylonian) | F-12 |
| 16 | H4 (FFT prediction) | F-13 |
| 17 | H1 (base conversion) | F-20 |
| 18 | H5 (modular forms) | F-15 |
| 20 | H3 (3D Lissajous) | F-16 |
| 21 | H1 (cognitive load) | F-17, F-26 |
| 22 | H1 (categories) | F-18 |
| 23 | H1 (Babylonian π) | F-19 |
| 24 | H1 (Kuramoto) | F-18 |
| 25 | H1 (17-gon) | F-20 |
| 26 | H3 (resonance) | F-20 |
| 24 | H1 (Kuramoto) | F-18 |
| 27 | H1 (quantum QFT) | F-21 |
| 28 | H1 (CORDIC) | F-22 |
| 29 | H1 (RNS NTT) | F-23 |
| 30 | H1 (wave solver) | F-24 |
| 31 | H1 (timeseries) | F-25 |
| 32 | H1 (education) | F-26 |

---

## 📊 Status Dashboard

### Overall Progress
- ✅ **Source Modules**: 11/11 complete (100%)
- ✅ **Tests**: 761 passing, 97.92% coverage
- ✅ **Experiments**: 36/36 complete (100%)
- ✅ **Findings**: 51/51 complete (all 11 fields)
- ✅ **Research Paper**: MD/HTML/PDF complete
- ✅ **Visualizations**: 98 embedded images
- ✅ **GitHub Repos**: 2 public repos pushed
- ✅ **Documentation**: Complete with keyword index

### Key Metrics
| Metric | Value |
|--------|-------|
| Source Lines | ~15,000 |
| Test Coverage | 97.92% |
| Finding Files | 51 |
| Experiment Scripts | 36 |
| Finding Fields | 11/11 |
| Embedded Images | 98 |
| GitHub Repos | 2 public |

---

## 🔧 Quick Commands

```bash
# Run all tests
pytest --cov=src/base60lab --cov-fail-under=95 -v

# Run specific experiment
python experiments/27_qft_circuit.py

# Verify claims
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

# Find by keyword
grep -r "keyword" docs/findings/ --include="*.md"
grep -r "keyword" src/base60lab/ --include="*.py"
```

---

## 📁 File Locations

```
/home/hyperion/Projects/Base60Research/
├── Base60Research (GitHub repo: github.com/hasnocool/Base60Research)
│   ├── base12-base60-laboratory/  ← Main implementation (GitHub: github.com/hasnocool/base60lab)
│   │   ├── src/base60lab/          # 11 modules
│   │   ├── experiments/            # 36 scripts
│   │   ├── tests/                  # 761 tests
│   │   ├── docs/findings/          # 51 finding files
│   │   ├── results/                # 98 visualizations
│   │   ├── experiments/wasm/       # WASM education app
│   │   ├── RESEARCH_PAPER.*        # Paper in 3 formats
│   │   ├── INDEX_ENHANCED.md       # This file
│   │   ├── IMPLEMENTATION_STATUS.md
│   │   ├── PLAN.md
│   │   └── .omo/ulw-research/      # Research state
│   ├── downloads/                  # Paper PDFs
│   └── .omo/                       # Research state
```

---

*Generated: 2026-11-18 | Base-12/60 Mathematical Research Programme | All 51 findings · 36 experiments · 3 formats · 2 repos*