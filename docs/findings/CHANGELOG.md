---
title: "Findings Changelog"
category: changelog
status: proven
version: "1.0.0"
---

# Findings Changelog

All notable changes to the findings documentation are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/) with semantic versioning per finding file.

## Finding Files Index

| File | Module | Status | Version | Category |
|------|--------|--------|---------|----------|
| [angles-circle-subdivisions.md](angles-circle-subdivisions.md) | `angles` | proven | 1.0.0 | geometry |
| [trigonometry-exact-values.md](trigonometry-exact-values.md) | `trigonometry` | proven | 1.0.0 | trigonometry |
| [modular-arithmetic-cyclic.md](modular-arithmetic-cyclic.md) | `modular` | proven | 1.0.0 | number-theory |
| [geometry-polygon-subdivisions.md](geometry-polygon-subdivisions.md) | `geometry` | proven | 1.0.0 | geometry |
| [frequency-ratios-harmonics.md](frequency-ratios-harmonics.md) | `frequency` | proven | 1.0.0 | signal-processing |
| [sequences-number-patterns.md](sequences-number-patterns.md) | `sequences` | proven | 1.0.0 | number-theory |
| [signal-processing-spectral.md](signal-processing-spectral.md) | `signal_processing` | proven | 1.0.0 | signal-processing |
| [fft-benchmarks-performance.md](fft-benchmarks-performance.md) | `fft_benchmarks` | proven | 1.0.0 | performance |
| [lissajous-phase-closure.md](lissajous-phase-closure.md) | `lissajous` | proven | 1.0.0 | geometry |
| [metrics-comparison-report.md](metrics-comparison-report.md) | `metrics` | proven | 1.0.0 | analysis |
| [core-rational.md](core-rational.md) | `core.rational` | proven | 1.0.0 | core |
| [core-types.md](core-types.md) | `core.types` | proven | 1.0.0 | core |
| [core-unknowns.md](core-unknowns.md) | `core.unknowns` | proven | 1.0.0 | core |
| [engines-base10.md](engines-base10.md) | `engines.base10_engine` | proven | 1.0.0 | engines |
| [engines-base12.md](engines-base12.md) | `engines.base12_engine` | proven | 1.0.0 | engines |
| [engines-base60.md](engines-base60.md) | `engines.base60_engine` | proven | 1.0.0 | engines |
| [domains-fractions.md](domains-fractions.md) | `domains.fractions` | proven | 1.0.0 | domains |

## Version History

### [Unreleased]
- Initial creation of all finding files with standardized frontmatter
- Status field standardized to: proven | conjecture | open | refuted
- Version field standardized to MAJOR.MINOR.PATCH format

### [1.0.0] - 2026-11-17

#### Added - Core Modules
- **core-rational.md**: Exact rational arithmetic foundation — proven, v1.0.0
- **core-types.md**: Shared type definitions (BaseNumber, Expression, Notation, Function) — proven, v1.0.0
- **core-unknowns.md**: Registry for tracking expressible-yet-unknown mathematical truths — proven, v1.0.0

#### Added - Engine Modules
- **engines-base10.md**: Decimal representation and arithmetic — proven, v1.0.0
- **engines-base12.md**: Duodecimal representation and arithmetic with unknowns registry — proven, v1.0.0
- **engines-base60.md**: Sexagesimal representation and arithmetic with unknowns registry — proven, v1.0.0

#### Added - Domain Modules
- **domains-fractions.md**: Cross-base fraction analysis via engine delegation — proven, v1.0.0

#### Added - Domain/Application Modules
- **angles-circle-subdivisions.md**: Circle subdivision handling for base-60/base-12 — proven, v1.0.0
- **trigonometry-exact-values.md**: Exact trigonometric values across angle representations — proven, v1.0.0
- **modular-arithmetic-cyclic.md**: Mod 12 and Mod 60 cyclic arithmetic — proven, v1.0.0
- **geometry-polygon-subdivisions.md**: Regular polygon geometry and circle divisions — proven, v1.0.0
- **frequency-ratios-harmonics.md**: Musical frequency ratios and phase as turn fractions — proven, v1.0.0
- **sequences-number-patterns.md**: Number sequences with exact rational arithmetic — proven, v1.0.0
- **signal-processing-spectral.md**: FFT, filters, and spectral analysis with exact rationals — proven, v1.0.0
- **fft-benchmarks-performance.md**: FFT performance across smooth number categories — proven, v1.0.0
- **lissajous-phase-closure.md**: Lissajous figure phase closure analysis — proven, v1.0.0
- **metrics-comparison-report.md**: Base comparison metrics (10, 12, 60) — proven, v1.0.0

## Status Definitions

| Status | Meaning |
|--------|---------|
| **proven** | Mathematically proven or computationally verified to high confidence with exact arithmetic |
| **conjecture** | Strong evidence suggests true, but not yet fully proven |
| **open** | Under investigation; no conclusion yet |
| **refuted** | Proven false or counterexample found |

## Version Format

All finding files use semantic versioning: **MAJOR.MINOR.PATCH**

- **MAJOR**: Incompatible API changes or fundamental finding revisions
- **MINOR**: New findings, significant additions, or status changes
- **PATCH**: Corrections, clarifications, typo fixes

## Verification

All findings verified by:
1. Unit tests: `pytest tests/ -v` (all pass)
2. Manual QA: Python one-liners documented in each finding
3. Exact arithmetic: No floating-point used internally in any module

## Generation

This CHANGELOG is manually maintained. When adding/updating a finding file:
1. Update the finding file's frontmatter (status, version)
2. Add entry to this CHANGELOG under appropriate version
3. Update the Finding Files Index table

---

*Generated for Base60Research project — all computations use exact rational arithmetic only.*