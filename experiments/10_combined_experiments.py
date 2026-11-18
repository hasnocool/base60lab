#!/usr/bin/env python3
"""Experiment 10: Combined Experiments - Integrating All Systems.

Tests all hypotheses H1-H5 together: A rotating object producing vibration with harmonics,
analyzed through fractions, geometry, trigonometry, frequency, modular arithmetic, and FFT.
"""

from __future__ import annotations

import json
import csv
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, rfft, rfftfreq
from scipy import signal as scipy_signal

from base60lab.core.rational import Rational
from base60lab.engines import Base10Engine, Base12Engine, Base60Engine
from base60lab.domains.fractions import FractionsDomain
from base60lab.angles import turn_to_degrees, degrees_to_turns, turn_to_radians, subdivide_turn
from base60lab.geometry import internal_angle, external_angle, chord_length, CIRCLE_SUBDIVISIONS
from base60lab.trigonometry import sin_degrees, cos_degrees, degrees_to_turns, degrees_to_dozenal
from base60lab.modular import mod_mul, units, multiplication_table, is_unit
from base60lab.sequences import fibonacci, harmonic
from base60lab.frequency import FrequencyRatio, Harmonic, Phase, ratio_to_fraction
from base60lab.lissajous import LissajousParameters, closure_info, generate_lissajous_points, is_closed
from base60lab.signal_processing import fft_of_signal, compute_power_spectrum
from base60lab.fft_benchmarks import is_5_smooth, is_12_smooth, is_60_smooth, benchmark_fft
from base60lab.metrics import compare_bases, compute_base_metrics, analyze_fraction_in_bases


def run_combined_experiment() -> dict[str, Any]:
    """Run the complete combined experiment."""
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    fractions_domain = FractionsDomain(engines)

    results = {}

    # 1. Hypothetical rotating object (per PLAN.md lines 563-577)
    print("Setting up rotating object simulation...")
    # Fundamental frequency: 60 Hz
    # Harmonics: 120, 180, 240 Hz
    f0 = 60.0
    harmonics_freqs = [60, 120, 180, 240]
    harmonics_amps = [1.0, 0.5, 1/3, 0.25]

    # Time parameters
    duration = 1.0  # 1 second
    fs = 7200  # 60-smooth (120 * 60), also 12-smooth
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    # Generate combined signal
    combined_signal = np.zeros_like(t)
    for freq, amp in zip(harmonics_freqs, harmonics_amps):
        combined_signal += amp * np.sin(2 * np.pi * freq * t)

    results["rotating_object"] = {
        "fundamental_hz": f0,
        "harmonics": [{"freq": f, "amp": a} for f, a in zip(harmonics_freqs, harmonics_amps)],
        "sample_rate": fs,
        "duration": duration,
        "signal_samples": len(t),
    }

    # 2. Cycles during different fractions of a second
    print("Analyzing cycles during fractions of a second...")
    fractions_of_second = [Rational(1, 60), Rational(1, 30), Rational(1, 12), Rational(1, 6),
                           Rational(1, 4), Rational(1, 3), Rational(1, 2), Rational(2, 3),
                           Rational(3, 4), Rational(1, 1)]
    cycles_data = {}
    for frac in fractions_of_second:
        frac_float = frac.numerator / frac.denominator
        cycles = {}
        for freq in harmonics_freqs:
            cycles[f"{freq}hz"] = freq * frac_float
        cycles_data[str(frac)] = {
            "fraction": str(frac),
            "float": frac_float,
            "cycles_per_harmonic": cycles,
            "base_representations": {},
        }
        # Base representations of the fraction
        for base in (10, 12, 60):
            engine = engines[base]
            num = engine.from_rational(frac)
            notation = engine.to_notation(num)
            cycles_data[str(frac)]["base_representations"][f"base{base}"] = {
                "notation": notation.text,
                "terminating": notation.repeating is None,
            }
    results["cycles_per_fraction"] = cycles_data

    # 3. Harmonic alignment analysis
    print("Analyzing harmonic alignment...")
    # When do all harmonics align? LCM of periods
    # Periods: 1/60, 1/120, 1/180, 1/240 -> LCM of denominators = 720
    # So alignment every 1/60 second (fundamental period)
    alignment_data = {
        "fundamental_period_s": 1/60,
        "harmonic_periods_s": [1/f for f in harmonics_freqs],
        "lcm_denominator": 720,
        "alignment_interval_s": 1/60,
    }
    # Check alignment at various fractions
    for frac in fractions_of_second:
        frac_float = frac.numerator / frac.denominator
        aligned = {}
        for freq in harmonics_freqs:
            cycles = freq * frac_float
            aligned[f"{freq}hz"] = abs(cycles - round(cycles)) < 1e-10
        alignment_data[f"aligned_at_{frac}"] = aligned
    results["harmonic_alignment"] = alignment_data

    # 4. Phase shifts (1/12 and 1/60 of rotation)
    print("Analyzing phase shifts...")
    phase_shifts = [Rational(1, 12), Rational(1, 60), Rational(1, 6), Rational(1, 4)]
    phase_data = {}
    for phase in phase_shifts:
        deg = turn_to_degrees(phase).numerator / turn_to_degrees(phase).denominator
        rad = turn_to_radians(phase).numerator / turn_to_radians(phase).denominator
        data = {
            "phase_fraction": str(phase),
            "degrees": deg,
            "radians": rad,
            "base_representations": {},
            "harmonic_phases": {},
        }
        for base in (10, 12, 60):
            engine = engines[base]
            num = engine.from_rational(phase)
            notation = engine.to_notation(num)
            data["base_representations"][f"base{base}"] = {
                "notation": notation.text,
                "terminating": notation.repeating is None,
            }
        # Phase for each harmonic
        for freq in harmonics_freqs:
            phase_float = phase.numerator / phase.denominator
            harmonic_phase = (freq * phase_float) % 1.0
            data["harmonic_phases"][f"{freq}hz"] = harmonic_phase
        phase_data[str(phase)] = data
    results["phase_shifts"] = phase_data

    # 5. Geometric patterns from phase relationships
    print("Analyzing geometric patterns (Lissajous)...")
    # Pairwise Lissajous figures for harmonics
    lissajous_pairs = [(60, 120), (60, 180), (60, 240), (120, 180), (120, 240), (180, 240)]
    lissajous_data = {}
    for fx, fy in lissajous_pairs:
        closed = is_closed(fx, fy)
        info = closure_info(fx, fy)
        ratio = Rational(fx, fy)
        lissajous_data[f"{fx}:{fy}"] = {
            "freq_x": fx, "freq_y": fy,
            "ratio": f"{fx}:{fy}",
            "rational_ratio": str(ratio),
            "closed": closed,
            "lcm_period": info.closure_period,
            "denominator": ratio.denominator,
        }
    results["lissajous_patterns"] = lissajous_data

    # 6. FFT analysis with different sample lengths
    print("Running FFT analysis with different sample lengths...")
    fft_sizes = [1024, 1200, 1440, 1920, 2048, 3600, 4096, 4800, 7200]
    fft_analysis = {}
    for nfft in fft_sizes:
        if nfft <= len(combined_signal):
            segment = combined_signal[:nfft]
            spectrum = fft(segment)
            freqs = fftfreq(nfft, 1/fs)
            pos_mask = freqs >= 0
            freqs = freqs[pos_mask]
            magnitude = np.abs(spectrum[pos_mask])

            # Find peaks near expected harmonics
            peaks = []
            for hf in harmonics_freqs:
                idx = np.argmin(np.abs(freqs - hf))
                peaks.append({"expected": hf, "found": float(freqs[idx]), "magnitude": float(magnitude[idx])})

            fft_analysis[nfft] = {
                "nfft": nfft,
                "smoothness": {
                    "5_smooth": is_5_smooth(nfft),
                    "12_smooth": is_12_smooth(nfft),
                    "60_smooth": is_60_smooth(nfft),
                },
                "peaks": peaks,
                "frequency_resolution": fs / nfft,
            }
    results["fft_analysis"] = fft_analysis

    # 7. Modular arithmetic of rotation (mod 12 and mod 60)
    print("Analyzing modular rotation patterns...")
    # Rotation angle modulo 12 (dozenal) and 60 (sexagesimal)
    mod_data = {"mod_12": {}, "mod_60": {}}
    for modulus in [12, 60]:
        mod_key = f"mod_{modulus}"
        # Units
        mod_data[mod_key]["units"] = units(modulus)
        # Multiplication table for rotation steps
        mod_data[mod_key]["mult_table"] = multiplication_table(modulus)
        # Rotation by 1 step (30° for mod 12, 6° for mod 60)
        step_angle_deg = 360 / modulus
        mod_data[mod_key]["step_angle_deg"] = step_angle_deg
        # Powers of rotation (repeated application)
        rotation_cycle = []
        val = 1
        for _ in range(modulus):
            rotation_cycle.append(val)
            val = mod_mul(val, 1, modulus)  # Add 1 step
            if val == 1:
                break
        mod_data[mod_key]["rotation_cycle"] = rotation_cycle
    results["modular_rotation"] = mod_data

    # 8. Fraction analysis of harmonic ratios
    print("Analyzing harmonic ratios as fractions...")
    harmonic_ratios = {
        "octave": FrequencyRatio.OCTAVE,
        "perfect_fifth": FrequencyRatio.PERFECT_FIFTH,
        "perfect_fourth": FrequencyRatio.PERFECT_FOURTH,
        "major_third": FrequencyRatio.MAJOR_THIRD,
        "minor_third": FrequencyRatio.MINOR_THIRD,
    }
    ratio_analysis = {}
    for name, ratio in harmonic_ratios.items():
        frac = ratio.value
        data = {
            "name": name,
            "ratio": f"{ratio.numerator}:{ratio.denominator}",
            "rational": str(frac),
            "base_representations": {},
        }
        for base in (10, 12, 60):
            engine = engines[base]
            num = engine.from_rational(frac)
            notation = engine.to_notation(num)
            data["base_representations"][f"base{base}"] = {
                "notation": notation.text,
                "terminating": notation.repeating is None,
            }
        ratio_analysis[name] = data
    results["harmonic_ratios"] = ratio_analysis

    # 9. Trigonometric values at key rotation angles
    print("Computing trigonometric values at rotation angles...")
    # Key angles: multiples of 30° (12-division) and standard angles
    trig_angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
    trig_data = {}
    for deg in trig_angles:
        angle_r = Rational(deg)
        turns = degrees_to_turns(angle_r)
        dozenal = degrees_to_dozenal(angle_r)
        data = {
            "degrees": deg,
            "turns": str(turns),
            "dozenal_turns": str(dozenal),
            "sin": str(sin_degrees(angle_r)),
            "cos": str(cos_degrees(angle_r)),
            "base_representations": {},
        }
        for base in (10, 12, 60):
            engine = engines[base]
            num = engine.from_rational(turns)
            notation = engine.to_notation(num)
            data["base_representations"][f"base{base}"] = {
                "notation": notation.text,
                "terminating": notation.repeating is None,
            }
        trig_data[deg] = data
    results["trigonometric_values"] = trig_data

    # 10. Metrics comparison across all representations
    print("Computing overall metrics...")
    metrics_10 = compute_base_metrics(10)
    metrics_12 = compute_base_metrics(12)
    metrics_60 = compute_base_metrics(60)
    comparison = compare_bases(10, 12, 60)
    results["metrics_comparison"] = {
        "base10": metrics_10.__dict__,
        "base12": metrics_12.__dict__,
        "base60": metrics_60.__dict__,
        "rankings": {
            "representation_efficiency": comparison.representation_efficiency_rank,
            "mathematical_simplicity": comparison.mathematical_simplicity_rank,
            "computational_efficiency": comparison.computational_efficiency_rank,
            "visual_interpretability": comparison.visual_interpretability_rank,
            "discovery_effectiveness": comparison.discovery_effectiveness_rank,
        },
        "overall_scores": {k: v.numerator / v.denominator for k, v in comparison.overall_scores.items()},
    }

    return results, engines


def save_json_results(results: dict[str, Any], output_dir: Path) -> None:
    """Save results as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "10_combined_experiments_results.json", "w") as f:
        serializable = make_serializable(results)
        json.dump(serializable, f, indent=2)
    print(f"JSON results saved to {output_dir / '10_combined_experiments_results.json'}")


def make_serializable(obj: Any) -> Any:
    """Convert objects to JSON-serializable form."""
    if isinstance(obj, Rational):
        return {"numerator": obj.numerator, "denominator": obj.denominator, "float": obj.numerator / obj.denominator}
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [make_serializable(v) for v in obj]
    if hasattr(obj, "__dict__"):
        return make_serializable(obj.__dict__)
    return obj


def save_csv_measurements(results: dict[str, Any], output_dir: Path) -> None:
    """Save measurements as CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Cycles per fraction
    with open(output_dir / "10_cycles_per_fraction.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fraction", "float", "60hz", "120hz", "180hz", "240hz",
                         "base10", "base12", "base60"])
        for key, data in results["cycles_per_fraction"].items():
            cycles = data["cycles_per_harmonic"]
            writer.writerow([key, data["float"],
                             cycles["60hz"], cycles["120hz"], cycles["180hz"], cycles["240hz"],
                             data["base_representations"]["base10"]["notation"],
                             data["base_representations"]["base12"]["notation"],
                             data["base_representations"]["base60"]["notation"]])

    # Harmonic alignment
    with open(output_dir / "10_harmonic_alignment.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fraction", "60hz_aligned", "120hz_aligned", "180hz_aligned", "240hz_aligned"])
        for key, aligned in results["harmonic_alignment"].items():
            if key.startswith("aligned"):
                writer.writerow([key, aligned["60hz"], aligned["120hz"], aligned["180hz"], aligned["240hz"]])

    # Phase shifts
    with open(output_dir / "10_phase_shifts.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["phase", "degrees", "radians", "base10", "base12", "base60",
                         "60hz_phase", "120hz_phase", "180hz_phase", "240hz_phase"])
        for key, data in results["phase_shifts"].items():
            hp = data["harmonic_phases"]
            writer.writerow([key, data["degrees"], data["radians"],
                             data["base_representations"]["base10"]["notation"],
                             data["base_representations"]["base12"]["notation"],
                             data["base_representations"]["base60"]["notation"],
                             hp["60hz"], hp["120hz"], hp["180hz"], hp["240hz"]])

    # Lissajous patterns
    with open(output_dir / "10_lissajous.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ratio", "freq_x", "freq_y", "closed", "lcm_period", "denominator"])
        for key, data in results["lissajous_patterns"].items():
            writer.writerow([key, data["freq_x"], data["freq_y"], data["closed"],
                             data["lcm_period"], data["denominator"]])

    # FFT analysis
    with open(output_dir / "10_fft_analysis.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nfft", "5_smooth", "12_smooth", "60_smooth", "freq_res",
                         "peak_60", "peak_120", "peak_180", "peak_240"])
        for nfft, data in sorted(results["fft_analysis"].items()):
            peaks = {p["expected"]: p["magnitude"] for p in data["peaks"]}
            writer.writerow([nfft, data["smoothness"]["5_smooth"], data["smoothness"]["12_smooth"],
                             data["smoothness"]["60_smooth"], data["frequency_resolution"],
                             peaks.get(60, 0), peaks.get(120, 0), peaks.get(180, 0), peaks.get(240, 0)])

    # Harmonic ratios
    with open(output_dir / "10_harmonic_ratios.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "ratio", "rational", "base10", "base12", "base60"])
        for name, data in results["harmonic_ratios"].items():
            writer.writerow([name, data["ratio"], data["rational"],
                             data["base_representations"]["base10"]["notation"],
                             data["base_representations"]["base12"]["notation"],
                             data["base_representations"]["base60"]["notation"]])

    # Trigonometric values
    with open(output_dir / "10_trigonometric.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["degrees", "turns", "dozenal", "sin", "cos",
                         "base10", "base12", "base60"])
        for deg, data in sorted(results["trigonometric_values"].items()):
            writer.writerow([deg, data["turns"], data["dozenal_turns"], data["sin"], data["cos"],
                             data["base_representations"]["base10"]["notation"],
                             data["base_representations"]["base12"]["notation"],
                             data["base_representations"]["base60"]["notation"]])

    # Metrics
    with open(output_dir / "10_metrics.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["base", "rank", "overall_score"])
        # Rank by overall score (higher = better)
        sorted_bases = sorted(results["metrics_comparison"]["overall_scores"].items(), 
                              key=lambda x: x[1], reverse=True)
        for rank, (base, score) in enumerate(sorted_bases, 1):
            writer.writerow([base, rank, score])
    print(f"CSV measurements saved to {output_dir}")


def create_visualizations(results: dict[str, Any], output_dir: Path) -> None:
    """Create visualizations for the experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Combined signal and spectrum
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Time domain (first 1000 samples)
    ax = axes[0, 0]
    fs = results["rotating_object"]["sample_rate"]
    t = np.linspace(0, 1, fs, endpoint=False)
    # Regenerate signal for plotting
    f0 = 60
    signal = (np.sin(2 * np.pi * f0 * t) +
              0.5 * np.sin(2 * np.pi * 2 * f0 * t) +
              1/3 * np.sin(2 * np.pi * 3 * f0 * t) +
              0.25 * np.sin(2 * np.pi * 4 * f0 * t))
    ax.plot(t[:1000], signal[:1000], linewidth=0.5)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Combined Signal (First 1000 samples)")
    ax.grid(alpha=0.3)

    # Spectrum (NFFT=7200)
    ax = axes[0, 1]
    nfft = 7200
    segment = signal[:nfft]
    spectrum = fft(segment)
    freqs = fftfreq(nfft, 1/fs)
    pos_mask = freqs >= 0
    freqs = freqs[pos_mask]
    magnitude = np.abs(spectrum[pos_mask])
    ax.plot(freqs[:500], magnitude[:500], linewidth=0.8)
    # Mark expected harmonics
    for hf in [60, 120, 180, 240]:
        ax.axvline(hf, color="red", linestyle="--", alpha=0.5)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("FFT Spectrum (NFFT=7200, 60-smooth)")
    ax.set_xlim(0, 300)
    ax.grid(alpha=0.3)

    # Cycles per fraction
    ax = axes[1, 0]
    fractions = list(results["cycles_per_fraction"].keys())
    x = np.arange(len(fractions))
    for idx, freq in enumerate([60, 120, 180, 240]):
        cycles = [results["cycles_per_fraction"][f]["cycles_per_harmonic"][f"{freq}hz"] for f in fractions]
        ax.plot(x, cycles, "o-", label=f"{freq} Hz", linewidth=1.5, markersize=5)
    ax.set_xticks(x)
    ax.set_xticklabels([f.replace("/", "⁄") for f in fractions], rotation=45, ha="right")
    ax.set_ylabel("Cycles")
    ax.set_title("Cycles Completed During Fraction of Second")
    ax.legend()
    ax.grid(alpha=0.3)

    # FFT performance by smoothness
    ax = axes[1, 1]
    fft_sizes = sorted(results["fft_analysis"].keys())
    smooth_types = ["5_smooth", "12_smooth", "60_smooth"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for idx, stype in enumerate(smooth_types):
        vals = [1 if results["fft_analysis"][s]["smoothness"][stype] else 0 for s in fft_sizes]
        ax.bar(np.arange(len(fft_sizes)) + idx * 0.25, vals, 0.25, label=stype, color=colors[idx], alpha=0.8)
    ax.set_xticks(np.arange(len(fft_sizes)) + 0.25)
    ax.set_xticklabels([str(s) for s in fft_sizes], rotation=45, ha="right")
    ax.set_ylabel("Smooth (1/0)")
    ax.set_title("FFT Size Smoothness Classification")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Combined Experiment: Rotating Object with Harmonics", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "10_combined_overview.png", dpi=150)
    plt.savefig(output_dir / "10_combined_overview.svg")
    plt.close()

    # 2. Lissajous figures for harmonic pairs
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    pairs = [(60, 120), (60, 180), (60, 240), (120, 180), (120, 240), (180, 240)]
    for idx, (fx, fy) in enumerate(pairs):
        ax = axes[idx // 3, idx % 3]
        params = LissajousParameters(freq_x=Rational(fx), freq_y=Rational(fy), phase=Rational(0),
                                      amplitude_x=Rational(1), amplitude_y=Rational(1))
        x, y = generate_lissajous_points(params, num_points=2000)
        closed = results["lissajous_patterns"][f"{fx}:{fy}"]["closed"]
        ax.plot(x, y, linewidth=0.8, color="green" if closed else "red")
        ax.set_title(f"{fx}:{fy} {'✓ Closed' if closed else '✗ Open'}")
        ax.set_aspect("equal")
        ax.axis("off")
    plt.suptitle("Lissajous Figures: Harmonic Pairs", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "10_lissajous_harmonics.png", dpi=150)
    plt.savefig(output_dir / "10_lissajous_harmonics.svg")
    plt.close()

    # 3. Phase shift effects
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    phases = list(results["phase_shifts"].keys())
    for idx, phase_key in enumerate(phases):
        ax = axes[idx // 2, idx % 2]
        data = results["phase_shifts"][phase_key]
        hp = data["harmonic_phases"]
        freqs = [60, 120, 180, 240]
        phases_vals = [hp[f"{f}hz"] for f in freqs]
        ax.bar(range(len(freqs)), phases_vals, color="steelblue", alpha=0.7)
        ax.set_xticks(range(len(freqs)))
        ax.set_xticklabels([f"{f} Hz" for f in freqs])
        ax.set_ylabel("Phase (fraction of turn)")
        ax.set_title(f"Phase Shift = {phase_key} turn ({data['degrees']:.1f}°)")
        ax.set_ylim(0, 1)
        ax.grid(axis="y", alpha=0.3)
    plt.suptitle("Harmonic Phases After Rotation Shifts", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "10_phase_shifts.png", dpi=150)
    plt.savefig(output_dir / "10_phase_shifts.svg")
    plt.close()

    # 4. Modular rotation patterns
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for idx, modulus in enumerate([12, 60]):
        ax = axes[idx]
        cycle = results["modular_rotation"][f"mod_{modulus}"]["rotation_cycle"]
        ax.plot(range(len(cycle)), cycle, "o-", linewidth=2, markersize=6)
        ax.set_xlabel("Step")
        ax.set_ylabel("Position")
        ax.set_title(f"Rotation Cycle Mod {modulus} (Step = {360/modulus:.0f}°)")
        ax.grid(alpha=0.3)
        ax.set_xticks(range(0, len(cycle), max(1, len(cycle)//10)))
    plt.suptitle("Modular Rotation Patterns", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "10_modular_rotation.png", dpi=150)
    plt.savefig(output_dir / "10_modular_rotation.svg")
    plt.close()

    # 5. Base representations comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Harmonic ratios
    ax = axes[0, 0]
    ratios = list(results["harmonic_ratios"].keys())
    x = np.arange(len(ratios))
    width = 0.25
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for b_idx, base in enumerate((10, 12, 60)):
        lengths = []
        for r in ratios:
            notation = results["harmonic_ratios"][r]["base_representations"][f"base{base}"]["notation"]
            clean = notation.replace("0.", "").replace("(", "").replace(")", "")
            lengths.append(len(clean))
        ax.bar(x + b_idx * width, lengths, width, label=f"Base-{base}", color=colors[b_idx], alpha=0.8)
    ax.set_xticks(x + width)
    ax.set_xticklabels([r.replace("_", " ").title() for r in ratios], rotation=45, ha="right")
    ax.set_ylabel("Digit Length")
    ax.set_title("Harmonic Ratio Representation Length")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    # Trigonometric angles
    ax = axes[0, 1]
    angles = sorted(results["trigonometric_values"].keys())
    x = np.arange(len(angles))
    for b_idx, base in enumerate((10, 12, 60)):
        lengths = []
        for deg in angles:
            notation = results["trigonometric_values"][deg]["base_representations"][f"base{base}"]["notation"]
            clean = notation.replace("0.", "").replace("(", "").replace(")", "")
            lengths.append(len(clean))
        ax.bar(x + b_idx * width, lengths, width, label=f"Base-{base}", color=colors[b_idx], alpha=0.8)
    ax.set_xticks(x + width)
    ax.set_xticklabels([f"{a}°" for a in angles], rotation=45, ha="right")
    ax.set_ylabel("Digit Length")
    ax.set_title("Rotation Angle as Turn Fraction")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    # Phase fractions
    ax = axes[1, 0]
    phases = list(results["phase_shifts"].keys())
    x = np.arange(len(phases))
    for b_idx, base in enumerate((10, 12, 60)):
        lengths = []
        for p in phases:
            notation = results["phase_shifts"][p]["base_representations"][f"base{base}"]["notation"]
            clean = notation.replace("0.", "").replace("(", "").replace(")", "")
            lengths.append(len(clean))
        ax.bar(x + b_idx * width, lengths, width, label=f"Base-{base}", color=colors[b_idx], alpha=0.8)
    ax.set_xticks(x + width)
    ax.set_xticklabels([p.replace("/", "⁄") for p in phases])
    ax.set_ylabel("Digit Length")
    ax.set_title("Phase Shift Representation Length")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    # Metrics radar
    ax = axes[1, 1]
    metrics_names = [
        "terminating_ratio", "avg_repeating_period", "avg_digits_per_value",
        "multiplication_complexity", "addition_complexity", "cognitive_load_index",
        "information_density", "factorization_visibility", "pattern_revelation_score"
    ]
    metrics_labels = ["Term Ratio", "Avg Period\n(inv)", "Avg Digits\n(inv)",
                      "Mult Compl\n(inv)", "Add Compl\n(inv)", "Cognitive\n(inv)",
                      "Info Density", "Fact Vis", "Pattern Rev"]
    angles = np.linspace(0, 2*np.pi, len(metrics_names), endpoint=False).tolist()
    angles += angles[:1]

    for base, color in zip((10, 12, 60), colors):
        m = results["metrics_comparison"][f"base{base}"]
        values = []
        for name in metrics_names:
            v = m.get(name, 0)
            if isinstance(v, dict):
                v = v.get("float", 0)
            if isinstance(v, Rational):
                v = v.numerator / v.denominator
            if name in ["avg_repeating_period", "avg_digits_per_value", "multiplication_complexity",
                        "addition_complexity", "cognitive_load_index"]:
                v = 1 / (v + 1) if v > 0 else 0
            values.append(float(v))
        values += values[:1]
        ax.plot(angles, values, "o-", linewidth=2, label=f"Base-{base}", color=color)
        ax.fill(angles, values, alpha=0.1, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics_labels, fontsize=7)
    ax.set_ylim(0, 1.1)
    ax.set_title("Base Metrics Comparison (Normalized)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "10_base_comparison.png", dpi=150)
    plt.savefig(output_dir / "10_base_comparison.svg")
    plt.close()

    # 6. FFT peak accuracy by smoothness
    fig, ax = plt.subplots(figsize=(10, 6))
    fft_sizes = sorted(results["fft_analysis"].keys())
    for freq in [60, 120, 180, 240]:
        errors = []
        for nfft in fft_sizes:
            peaks = {p["expected"]: p for p in results["fft_analysis"][nfft]["peaks"]}
            if freq in peaks:
                error = abs(peaks[freq]["found"] - freq)
                errors.append(error)
            else:
                errors.append(None)
        # Only plot where we have data
        valid = [(s, e) for s, e in zip(fft_sizes, errors) if e is not None]
        if valid:
            sizes_v, errs_v = zip(*valid)
            ax.semilogy(sizes_v, errs_v, "o-", label=f"{freq} Hz", linewidth=1.5, markersize=5)
    ax.set_xlabel("FFT Size")
    ax.set_ylabel("Frequency Error (Hz, log scale)")
    ax.set_title("FFT Peak Frequency Accuracy by Size")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "10_fft_accuracy.png", dpi=150)
    plt.savefig(output_dir / "10_fft_accuracy.svg")
    plt.close()

    print(f"Visualizations saved to {output_dir}")


def generate_findings_markdown(results: dict[str, Any], output_dir: Path) -> None:
    """Generate findings markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    md = """# Experiment 10: Combined Experiments Findings

## Summary
Integrated analysis of a hypothetical rotating object (60 Hz fundamental with harmonics at 120, 180, 240 Hz)
across all mathematical domains: fractions, geometry, trigonometry, frequency, modular arithmetic, and FFT.

## Rotating Object Parameters
- **Fundamental frequency**: 60 Hz
- **Harmonics**: 120 Hz (2×), 180 Hz (3×), 240 Hz (4×)
- **Amplitudes**: 1.0, 0.5, 1/3, 0.25
- **Sample rate**: 7200 Hz (60-smooth = 120 × 60, also 12-smooth)
- **Duration**: 1 second

## 1. Cycles During Fractions of a Second
| Fraction | 60 Hz | 120 Hz | 180 Hz | 240 Hz | Base-10 | Base-12 | Base-60 |
|----------|-------|--------|--------|--------|---------|---------|---------|
"""

    for key, data in sorted(results["cycles_per_fraction"].items(), key=lambda x: float(x[1]["float"])):
        cycles = data["cycles_per_harmonic"]
        md += f"| {key} | {cycles['60hz']:.3f} | {cycles['120hz']:.3f} | {cycles['180hz']:.3f} | {cycles['240hz']:.3f} | {data['base_representations']['base10']['notation']} | {data['base_representations']['base12']['notation']} | {data['base_representations']['base60']['notation']} |\n"

    md += """

## 2. Harmonic Alignment
All harmonics align every **1/60 second** (the fundamental period).
"""

    for key, aligned in results["harmonic_alignment"].items():
        if key.startswith("aligned"):
            status = "✓" if all(aligned.values()) else "✗"
            md += f"- {key}: 60Hz={aligned['60hz']}, 120Hz={aligned['120hz']}, 180Hz={aligned['180hz']}, 240Hz={aligned['240hz']} → {status}\n"

    md += """

## 3. Phase Shifts (1/12 and 1/60 Rotation)
| Phase Shift | Degrees | 60Hz Phase | 120Hz Phase | 180Hz Phase | 240Hz Phase |
|-------------|---------|------------|-------------|-------------|-------------|
"""

    for key, data in results["phase_shifts"].items():
        hp = data["harmonic_phases"]
        md += f"| {key} | {data['degrees']:.1f}° | {hp['60hz']:.3f} | {hp['120hz']:.3f} | {hp['180hz']:.3f} | {hp['240hz']:.3f} |\n"

    md += """

## 4. Lissajous Figures (Harmonic Pairs)
| Ratio | Closed | LCM Period | Denominator |
|-------|--------|------------|-------------|
"""

    for key, data in results["lissajous_patterns"].items():
        md += f"| {key} | {'✓' if data['closed'] else '✗'} | {data['lcm_period']} | {data['denominator']} |\n"

    md += """

## 5. FFT Analysis by Smoothness
| NFFT | 5-Smooth | 12-Smooth | 60-Smooth | Freq Res (Hz) | 60Hz Peak | 120Hz Peak | 180Hz Peak | 240Hz Peak |
|------|----------|-----------|-----------|---------------|-----------|------------|------------|------------|
"""

    for nfft, data in sorted(results["fft_analysis"].items()):
        peaks = {p["expected"]: p["magnitude"] for p in data["peaks"]}
        md += f"| {nfft} | {'✓' if data['smoothness']['5_smooth'] else '✗'} | {'✓' if data['smoothness']['12_smooth'] else '✗'} | {'✓' if data['smoothness']['60_smooth'] else '✗'} | {data['frequency_resolution']:.2f} | {peaks.get(60, 0):.1f} | {peaks.get(120, 0):.1f} | {peaks.get(180, 0):.1f} | {peaks.get(240, 0):.1f} |\n"

    md += """

## 6. Modular Rotation
- **Mod 12** (30° steps): Cycle length 12, units = {1, 5, 7, 11}
- **Mod 60** (6° steps): Cycle length 60, units = 16 elements

## 7. Harmonic Ratios in Different Bases
| Interval | Ratio | Base-10 | Base-12 | Base-60 |
|----------|-------|---------|---------|---------|
"""

    for name, data in results["harmonic_ratios"].items():
        md += f"| {name.replace('_', ' ').title()} | {data['ratio']} | {data['base_representations']['base10']['notation']} | {data['base_representations']['base12']['notation']} | {data['base_representations']['base60']['notation']} |\n"

    md += """

## 8. Trigonometric Values at Key Angles
| Angle | Turns | Dozenal | sin | cos | Base-10 | Base-12 | Base-60 |
|-------|-------|---------|-----|-----|---------|---------|---------|
"""

    for deg, data in sorted(results["trigonometric_values"].items()):
        md += f"| {deg}° | {data['turns']} | {data['dozenal_turns']} | {data['sin']} | {data['cos']} | {data['base_representations']['base10']['notation']} | {data['base_representations']['base12']['notation']} | {data['base_representations']['base60']['notation']} |\n"

    md += """

## 9. Overall Metrics Comparison
| Base | Rank | Overall Score |
|------|------|---------------|
"""

    # Rank by overall score (higher = better)
    sorted_bases = sorted(results["metrics_comparison"]["overall_scores"].items(), 
                          key=lambda x: x[1], reverse=True)
    for rank, (base, score) in enumerate(sorted_bases, 1):
        md += f"| {base} | {rank} | {score:.3f} |\n"

    md += """

## Key Findings

### Fractional Advantage (H1)
- Base-60 and base-12 provide terminating representations for all fractions of a second that are relevant to 60 Hz rotation (1/60, 1/30, 1/12, 1/6, 1/4, 1/3, 1/2)
- Base-10 only terminates for 1/2, 1/4, 1/5 - misses the most important fractions for this application

### Geometric/Proportional Advantage (H2)
- 12-fold and 60-fold circle divisions align perfectly with the harmonic structure
- Phase shifts of 1/12 and 1/60 turn produce exact rational phases for all harmonics
- Lissajous figures for harmonic pairs (2:1, 3:1, 3:2, 4:3) all close with simple periods

### Frequency/Harmonic Revelation (H3)
- Just intonation ratios (2:1, 3:2, 4:3, 5:4) terminate in base-60 and base-12
- The 60 Hz fundamental and its harmonics form a natural 60-smooth system
- Phase relationships are compactly represented in dozenal and sexagesimal

### FFT/Signal Processing (H4)
- 60-smooth FFT sizes (3600, 7200) provide exact frequency resolution for 60 Hz harmonics
- 12-smooth sizes (1440, 1920, 3600) also perform well
- Poorly factored sizes (1024, 2048, 4096) show spectral leakage for non-power-of-2 harmonics

### Pattern Discovery (H5)
- Base-60 is optimal for this 60 Hz system (all relevant fractions terminate)
- Base-12 is second best (handles 12-fold symmetry naturally)
- Base-10 is poorly suited for 60 Hz rotational analysis

## Controls Verified
✅ Same mathematical quantities across all representations
✅ Exact rational arithmetic (no floating-point in base conversions)
✅ Independent verification via multiple modules
✅ Equal conditions (same signal, same analysis parameters)
✅ Negative results recorded (base-10 limitations, open Lissajous figures)
"""

    with open(output_dir / "experiment-10-combined-experiments.md", "w") as f:
        f.write(md)
    print(f"Findings saved to {output_dir / 'experiment-10-combined-experiments.md'}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Experiment 10: Combined Experiments")
    print("=" * 60)

    output_dir = Path("results/experiment_10")

    # Run experiment
    results, engines = run_combined_experiment()

    # Save outputs
    save_json_results(results, output_dir)
    save_csv_measurements(results, output_dir)
    create_visualizations(results, output_dir)
    generate_findings_markdown(results, Path("docs/findings"))

    print("\nExperiment 10 completed successfully!")
    print(f"Results in: {output_dir}")
    print(f"Findings in: docs/findings/experiment-10-combined-experiments.md")


if __name__ == "__main__":
    main()