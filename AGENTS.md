# AGENTS.md — Base-12 / Base-60 Mathematical Research Laboratory

> **Scope:** Project-specific operational contract for the `base12-base60-laboratory` Python package.
> **Root workspace:** `/home/hyperion/Projects/Base60Research` (kept clean — no build artifacts, no temp files)
> **Project folder:** `/home/hyperion/Projects/Base60Research/base12-base60-laboratory`
> **Required reference:** Global `/home/hyperion/.agents/AGENTS.md` and project `RULES.md` (this file).

---

## Project Overview

**Project:** Base-12 / Base-60 Mathematical Research Laboratory (`base60lab`)
**Location:** `/home/hyperion/Projects/Base60Research/base12-base60-laboratory`
**Root workspace:** `/home/hyperion/Projects/Base60Research` (kept clean — only docs, downloads, research papers, `.omo/` state)

### Project Structure
```
base12-base60-laboratory/
├── src/base60lab/          # Python package (11 modules)
│   ├── core/               # rational.py, types.py, unknowns.py
│   ├── engines/            # base10_engine.py, base12_engine.py, base60_engine.py
│   ├── domains/            # fractions.py
│   ├── angles.py, geometry.py, trigonometry.py, modular.py, sequences.py
│   ├── frequency.py, lissajous.py, signal_processing.py, fft_benchmarks.py, metrics.py, numerals.py
├── tests/                  # 823 tests, 98% coverage
│   ├── test_core/, test_engines/, test_domains/
├── experiments/            # 16 experiment scripts (01-10, 15-18, 20-21)
├── docs/                   # Documentation + findings (35 files)
│   ├── findings/           # 35 finding files with YAML frontmatter
├── docs/findings/          # 35 finding files with YAML frontmatter
├── RESEARCH_PAPER.md/html/pdf  # Research paper (3 formats)
├── pyproject.toml          # Package config (Python 3.12+, pytest, sympy, numpy, scipy, mpmath, matplotlib, pandas)
├── .gitignore              # Ignores build artifacts, venv, data/, results/
├── .coverage               # Coverage data
└── .pytest_cache/
```

---

## Project-Specific Rules

### 1. Code Standards
- **Exact rational arithmetic only** — No floating-point in internal arithmetic. Use `fractions.Fraction` via `src/base60lab/core/rational.Rational`.
- **No floating-point internal arithmetic** — `float()` only for display/debugging and NumPy/SciPy boundaries.
- **Exact rational throughout** — All metrics, conversions, and computations use `Rational`.
- **Type hints required** — All public functions must have type hints.

### 2. Experiment Protocol
Each experiment script in `experiments/` must:
- Run end-to-end with `python experiments/XX_*.py`
- Produce: JSON results, CSV measurements, PNG/SVG visualizations, findings markdown
- Honor controls: same quantity, exact arithmetic, independent verification, equal conditions, negative results matter
- Output to `results/experiment_XX/` and `docs/findings/experiment-XX-*.md`

### 3. Finding Files
- All finding files in `docs/findings/` must have YAML frontmatter:
  ```yaml
  ---
  title: "..."
  category: "fractions|geometry|trigonometry|..."
  status: "proven|conjecture|open|refuted"
  version: "MAJOR.MINOR.PATCH"
  ---
  ```

### 3. Testing
- `pytest --cov=src/base60lab --cov-fail-under=95 -v` must pass
- All modules must maintain ≥95% coverage
- 823 tests currently passing (98.07% coverage)

### 4. Verification Protocol
- Claims must be verified by executing code, not judgment
- `verify_*.py` scripts in root for contested claims
- `grep -rn "float(" src/base60lab/ || echo "NO FLOAT USAGE - PASS"` must pass

---

## Workspace Boundaries

### Root Workspace (`/home/hyperion/Projects/Base60Research`) — KEPT CLEAN
**Allowed:**
- `base12-base60-laboratory/` (project folder)
- `docs/` (reference papers, downloaded PDFs)
- `downloads/` (downloaded papers)
- `research/` (research notes, experiment designs)
- `downloads/` (paper PDFs)
- `.omo/` (operational state)
- `.oml/` (if exists)

**NOT ALLOWED in root:**
- Build artifacts, `__pycache__`, `.pytest_cache/`
- Virtual environments (`.venv/`, `venv/`)
- Build artifacts (`build/`, `dist/`, `*.egg-info/`)
- Temporary files, logs, caches
- Results directories (`results/`, `data/`) — these live in project folder

### Project Folder (`/home/hyperion/Projects/Base60Research/base12-base60-laboratory`)
**Contains:**
- Source code (`src/`)
- Tests (`tests/`)
- Experiments (`experiments/`)
- Results (`results/`)
- Documentation (`docs/`, `docs/findings/`)
- Research paper artifacts (`RESEARCH_PAPER.*`)
- Build artifacts, caches, virtual environments (allowed here)

---

## Development Commands

```bash
# Run all tests with coverage gate
cd /home/hyperion/Projects/Base60Research/base12-base60-laboratory
python -m pytest --cov=src/base60lab --cov-fail-under=95 -v

# Run specific experiment
python experiments/15_babylonian_reciprocals.py

# Run all experiments
for f in experiments/01_*.py experiments/02_*.py ... experiments/21_*.py; do python "$f"; done

# Verify no float usage
grep -rn "float(" src/base60lab/ || echo "NO FLOAT USAGE - PASS"

# Run coverage report
python -m pytest --cov=src/base60lab --cov-report=term-missing --cov-fail-under=95

# Build research paper
cd /home/hyperion/Projects/Base60Research/base12-base60-laboratory
pandoc RESEARCH_PAPER.md -o RESEARCH_PAPER.html --standalone --toc --css=https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
# PDF via reportlab (in RESEARCH_PAPER.md script)
```

---

## Key Paths

| Purpose | Path |
|---------|------|
| Project root | `/home/hyperion/Projects/Base60Research/base12-base60-laboratory` |
| Root workspace | `/home/hyperion/Projects/Base60Research` |
| Source code | `/home/hyperion/Projects/Base60Research/base12-base60-laboratory/src/base60lab/` |
| Tests | `/home/hyperion/Projects/Base60Research/base12-base60-laboratory/tests/` |
| Experiments | `/home/hyperion/Projects/Base60Research/base12-base60-laboratory/experiments/` |
| Results | `/home/hyperion/Projects/Base60Research/base12-base60-laboratory/results/` |
| Findings | `/home/hyperion/Projects/Base60Research/base12-base60-laboratory/docs/findings/` |
| Research paper | `/home/hyperion/Projects/Base60Research/base12-base60-laboratory/RESEARCH_PAPER.*` |
| Plans | `/home/hyperion/Projects/Base60Research/.omo/plans/` |
| Ulw-research state | `/home/hyperion/Projects/Base60Research/.omo/ulw-research/` |
| Global agents config | `/home/hyperion/.agents/AGENTS.md` |

---

## Agent Instructions

When working on this project:
1. **Always** `cd /home/hyperion/Projects/Base60Research/base12-base60-laboratory` first
2. **Never** write build artifacts, caches, or temp files to `/home/hyperion/Projects/Base60Research/`
3. **Always** run tests with coverage gate before claiming completion
4. **Never** write floating-point arithmetic in `src/base60lab/` core modules
5. **Always** verify claims by executing code, not judgment
6. **Update** finding files with YAML frontmatter when adding new findings

---

## Research Paper Maintenance

The research paper (`RESEARCH_PAPER.md/.html/.pdf`) must be updated when:
- New experiments are added (15-21 completed)
- New findings are verified (refuted/confirmed claims)
- New experiment directions are proposed (from literature search)
- Verification results change claim statuses

Formats to maintain: Markdown (source), HTML (pandoc + Bootstrap), PDF (reportlab).

---

## Verification Checklist (Pre-Commit)

- [ ] `cd /home/hyperion/Projects/Base60Research/base12-base60-laboratory`
- [ ] `python -m pytest --cov=src/base60lab --cov-fail-under=95 -q` passes
- [ ] `grep -rn "float(" src/base60lab/ || echo "NO FLOAT USAGE - PASS"` passes
- [ ] All 16 experiments run: `for f in experiments/*.py; do python "$f"; done`
- [ ] All 35 finding files have valid YAML frontmatter (`status`, `version`)
- [ ] `RESEARCH_PAPER.md` updated with new findings
- [ ] `RESEARCH_PAPER.html` regenerated via pandoc
- [ ] `RESEARCH_PAPER.pdf` regenerated via reportlab

---
<local:///home/hyperion/Projects/Base60Research/base12-base60-laboratory/AGENTS_enhanced.md>

*Generated by ulw-research orchestration — Base-12 / Base-60 Mathematical Research Programme*