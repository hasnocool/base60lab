# RULES.md — Base60Lab Project Rules

> **Project:** Base-12 / Base-60 Mathematical Research Laboratory
> **Location:** `/home/hyperion/Projects/Base60Research/base12-base60-laboratory`
> **Root workspace:** `/home/hyperion/Projects/Base60Research` (kept clean)

---

## 1. Code Standards

### Mandatory
- **Exact rational arithmetic only** — Use `src/base60lab/core/rational.Rational` (wraps `fractions.Fraction`)
- **No floating-point internal arithmetic** — `float()` ONLY for:
  - Display/debugging output
  - NumPy/SciPy/Matplotlib boundary calls (where libraries require float)
  - JSON serialization of final results
- **Type hints required** on all public functions and methods
- **Docstrings** on all public classes, methods, and functions

### Prohibited
- `float()` in core arithmetic modules (`core/`, `engines/`, `domains/`, `numerals.py`, `geometry.py`, `trigonometry.py`, `modular.py`, `sequences.py`, `frequency.py`, `lissajous.py`, `metrics.py`)
- `numpy.float64` or `np.float64` in internal arithmetic
- `math.` functions on Rational objects (use Rational methods instead)

### Allowed float usage (boundaries only)
- `to_float()` methods for display/debugging
- NumPy/SciPy FFT, signal processing, plotting
- JSON serialization of final results
- Matplotlib plotting

---

## 2. Experiment Protocol

Every experiment in `experiments/` must:

### Required outputs (all must exist after run):
```
results/experiment_XX/
├── experiment_XX_results.json      # Complete results
├── experiment_XX_*.csv             # CSV measurements
├── experiment_XX_*.png             # PNG visualizations
├── experiment_XX_*.svg             # SVG visualizations
└── ...

docs/findings/experiment-XX-*.md    # Findings with YAML frontmatter
```

### Required controls (per PLAN.md):
1. **Same quantity** — Same mathematical quantity across bases
2. **Exact arithmetic** — Rational/symbolic, no floating-point
3. **Independent verification** — Convert back, verify independently
3. **Equal conditions** — Preserve sampling rates, durations, FFT sizes
4. **Negative results matter** — Document when base-60/12 performs worse

### Experiment script template:
```python
#!/usr/bin/env python3
"""Experiment XX: <Name>"""
from base60lab.core.rational import Rational
from base60lab.<module> import <functions>

def main():
    # Exact rational arithmetic only
    results = {}
    # ... computation ...
    # Write JSON, CSV, generate PNG/SVG
    # Write findings markdown with YAML frontmatter

if __name__ == "__main__":
    main()
```

---

## 3. Finding Files

Every `.md` in `docs/findings/` MUST have YAML frontmatter:

```yaml
---
title: "Experiment XX: <Name> Findings"
category: "fractions|geometry|trigonometry|signal-processing|..."
status: "proven|conjecture|open|refuted"
version: "MAJOR.MINOR.PATCH"
---
```

### Status values:
- `proven` — Mathematically proven or computationally verified to high confidence
- `conjecture` — Strong evidence suggests true, but not fully proven
- `open` — Under investigation; no conclusion yet
- `refuted` — Proven false or counterexample found

### Version format: `MAJOR.MINOR.PATCH` (semver)

---

## 4. Testing Standards

### Coverage Requirements
- **Overall:** ≥95% (current: 98.07%)
- **Per module:** ≥95% (all 11 modules currently ≥95%)
- `__init__.py` exception: 88% acceptable (import guard)

### Test Structure
```
tests/
├── test_core/           # core/rational.py, types.py, unknowns.py
├── test_engines/        # base10, base12, base60 engines
├── test_domains/        # fractions domain
└── test_core/test_lissajous_3d.py  # 3D Lissajous tests (54 tests)
```

### Test Principles
- **Deterministic** — Fixed seeds (`np.random.default_rng(42)`)
- **Exact rational verification** — Compare `Rational` objects, not floats
- **Boundary testing** — Zero, negative, large numbers, edge cases
- **Determinism tests** — Repeated calls produce identical results

---

## 4. Verification Protocol

### Before claiming completion:
1. **Run full test suite with coverage gate:**
   ```bash
   python -m pytest --cov=src/base60lab --cov-fail-under=95 -q
   ```

2. **Verify no internal float usage:**
   ```bash
   grep -rn "float(" src/base60lab/ || echo "NO FLOAT USAGE - PASS"
   ```

3. **Run all experiments:**
   ```bash
   for f in experiments/*.py; do python "$f"; done
   ```

4. **Verify finding files:**
   ```bash
   python3 -c "
   import yaml, glob
   for f in sorted(glob.glob('docs/findings/*.md')):
       with open(f) as fh: c = fh.read()
       assert c.startswith('---\n'), f'{f}: no frontmatter'
       fm = yaml.safe_load(f[4:f.index('\n---\n',4)])
       assert 'status' in fm and 'version' in fm, f'{f}: missing status/version'
   print('ALL OK')
   ```

---

## 5. Research Paper Maintenance

### When to update `RESEARCH_PAPER.md`:
- New experiments added (15-21 completed)
- Claims verified/refuted (Delta mod 60 refuted, partition congruences confirmed)
- New experiment directions proposed (from literature search)
- Verification results change claim statuses

### Formats to maintain:
1. **Markdown** (`RESEARCH_PAPER.md`) — source
2. **HTML** (`RESEARCH_PAPER.html`) — `pandoc RESEARCH_PAPER.md -o RESEARCH_PAPER.html --standalone --toc --css=https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css`
3. **PDF** (`RESEARCH_PAPER.pdf`) — `python3 -c "from reportlab...` (via reportlab script)

### Template structure:
1. Abstract
2. Mathematical Foundations
3. Current Results (all 16 experiments)
4. Composite Score Analysis
4. Verification Results
5. New Experiment Directions
5. Reproducibility
6. Conclusions
6. References

---

## 5. Git Hygiene

### Branch strategy:
- `main` — Stable, all tests passing, coverage ≥95%
- Feature branches for experiments

### Commit messages:
```
<type>(<module>): <description>

- Detail 1
- Detail 2
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `exp`

### Pre-commit checks:
```bash
python -m pytest --cov=src/base60lab --cov-fail-under=95 -q
grep -rn "float(" src/base60lab/ || echo "NO FLOAT USAGE - PASS"
```

---

## 5. Verification Scripts

Maintain these verification scripts in project root:
- `verify_delta_mod60.py` — Delta function mod 60 cycle claim
- `verify_partition_congruence.py` — Ramanujan partition congruences
- `verify_smooth_fft_claim.py` — 5-smooth FFT performance
- `verify_exp02_discrepancy.py` — Experiment 02 finding discrepancy
- `verify_findings.py` — Finding file frontmatter validation

---

## 6. Experiment Registry

| # | Script | Title | Status |
|---|--------|-------|--------|
| 01 | `01_fraction_analysis.py` | Fraction Analysis | ✅ |
| 02 | `02_geometry_analysis.py` | Geometry Analysis | ✅ |
| 03 | `03_trigonometry_analysis.py` | Trigonometry Analysis | ✅ |
| 04 | `04_modular_patterns.py` | Modular Patterns | ✅ |
| 05 | `05_algebra_sequences.py` | Algebra & Sequences | ✅ |
| 06 | `06_harmonic_analysis.py` | Harmonic Analysis | ✅ |
| 07 | `07_lissajous_analysis.py` | Lissajous Analysis | ✅ |
| 08 | `08_fft_benchmarks.py` | FFT Benchmarks | ✅ |
| 09 | `09_real_world_signals.py` | Real-World Signals | ✅ |
| 10 | `10_combined_experiments.py` | Combined Experiments | ✅ |
| 15 | `15_babylonian_reciprocals.py` | Babylonian Reciprocals/Plimpton 322 | ✅ |
| 16 | `16_smooth_fft_prediction.py` | Smooth FFT Prediction | ✅ |
| 17 | `17_direct_base_conversion.py` | Direct Base Conversion | ✅ |
| 18 | `18_modular_forms_qseries.py` | Modular Forms q-Series | ✅ |
| 19 | — | NTT 60-smooth (deprioritized) | ⏸️ |
| 20 | `20_lissajous_3d.py` | 3D Lissajous/Torus | ✅ |
| 21 | `21_cognitive_load_mitigation.py` | Cognitive Load | ✅ |

---

## 8. Workspace Cleanliness Rules

### Root workspace (`/home/hyperion/Projects/Base60Research/`) — KEEP CLEAN
**Allowed:**
- `base12-base60-laboratory/` (project folder)
- `docs/` (reference papers)
- `downloads/` (paper PDFs)
- `research/` (research notes)
- `.omo/` (operational state)
- `downloads/` (paper PDFs)

**NEVER in root:**
- `__pycache__/`, `.pytest_cache/`, `.coverage`
- `.venv/`, `venv/`, `env/`
- `build/`, `dist/`, `*.egg-info/`
- `results/`, `data/`, `experiments/`, `tests/` (these live in project folder)

---

*Rules maintained by ulw-research orchestration — Base-12 / Base-60 Mathematical Research Programme*