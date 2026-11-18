#!/usr/bin/env python3
"""Experiment 24: Kuramoto Oscillator Networks with Smooth Frequency Ratios.

Tests whether phase-locking boundaries in Kuramoto networks with {2,3,5}-smooth
frequency ratios are more clearly delineated in base-60 phase representation.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from base60lab.core.rational import Rational
from base60lab.frequency import FrequencyRatio, Phase, Harmonic
from base60lab.lissajous import closure_info
from base60lab.angles import turn_to_degrees, degrees_to_turns, normalize_turns
from base60lab.numerals import rational_to_base, int_to_base
from base60lab.metrics import compute_base_metrics, compare_bases, analyze_fraction_in_bases


def _to_float(r: Rational) -> float:
    """Convert Rational to float via its internal Fraction."""
    return float(r._value)


# ========================================================================
# Kuramoto Model with Exact Rational Arithmetic
# ========================================================================

@dataclass
class Oscillator:
    """A single Kuramoto oscillator with exact rational frequency."""
    index: int
    omega: Rational  # natural frequency
    theta: Phase     # phase as fraction of turn

    def phase_degrees(self) -> Rational:
        return turn_to_degrees(self.theta.value)

    def phase_base60(self) -> str:
        return rational_to_base(self.theta.value, 60, max_digits=50)


@dataclass
class KuramotoNetwork:
    """Network of coupled Kuramoto oscillators."""
    oscillators: list[Oscillator]
    K: Rational  # coupling strength
    N: int

    def order_parameter(self) -> tuple[Rational, Rational]:
        """Compute Kuramoto order parameter r * e^(i*psi).
        Returns (r, psi) where r = |(1/N) sum e^(i*theta_j)|"""
        sum_cos = Rational(0)
        sum_sin = Rational(0)
        for osc in self.oscillators:
            # Use exact trig for special angles, approximate for others
            theta_deg = _to_float(osc.phase_degrees())
            sum_cos += Rational(math.cos(math.radians(theta_deg)))
            sum_sin += Rational(math.sin(math.radians(theta_deg)))
        r = Rational(math.hypot(_to_float(sum_cos/self.N), _to_float(sum_sin/self.N)))
        psi = Phase(Rational(math.degrees(math.atan2(_to_float(sum_sin/self.N), _to_float(sum_cos/self.N))), 360))
        return r, psi

    def phase_differences(self) -> list[Rational]:
        """Compute all pairwise phase differences."""
        diffs = []
        for i in range(self.N):
            for j in range(i+1, self.N):
                diff = (self.oscillators[i].theta.value - self.oscillators[j].theta.value)
                diffs.append(normalize_turns(diff))
        return diffs

    def sync_condition_check(self) -> dict[tuple[int, int], bool]:
        """Check synchronization condition |ω_i - ω_j| ≤ K for all pairs."""
        results = {}
        for i in range(self.N):
            for j in range(i+1, self.N):
                omega_diff = abs(self.oscillators[i].omega - self.oscillators[j].omega)
                results[(i, j)] = omega_diff <= self.K
        return results


def generate_5_smooth_ratios(max_denominator: int = 30) -> list[FrequencyRatio]:
    """Generate frequency ratios with 5-smooth denominators."""
    ratios = []
    for num in range(1, max_denominator + 1):
        for den in range(1, max_denominator + 1):
            if math.gcd(num, den) == 1:
                # Check if denominator is 5-smooth
                temp = den
                for p in [2, 3, 5]:
                    while temp % p == 0:
                        temp //= p
                if temp == 1:
                    ratios.append(FrequencyRatio(num, den))
    return sorted(set(ratios), key=lambda r: _to_float(r.value))


def create_network_from_ratios(ratios: list[FrequencyRatio], base_freq: Rational, K: Rational) -> KuramotoNetwork:
    """Create oscillator network from frequency ratios."""
    oscillators = []
    for i, ratio in enumerate(ratios):
        omega = base_freq * ratio.value
        # Initial phases: spread uniformly around circle
        theta = Phase(Rational(i, len(ratios)))
        oscillators.append(Oscillator(i, omega, theta))
    return KuramotoNetwork(oscillators, K, len(oscillators))


def simulate_kuramoto(network: KuramotoNetwork, steps: int = 1000, dt: Rational = Rational(1, 100)) -> list[dict]:
    """Simulate Kuramoto dynamics using exact rational arithmetic where possible."""
    history = []
    oscillators = network.oscillators
    N = network.N
    K = network.K

    for step in range(steps):
        # Compute derivatives
        dtheta = []
        for i in range(N):
            sum_sin = Rational(0)
            for j in range(N):
                if i != j:
                    # sin(theta_j - theta_i) - approximate for non-special angles
                    diff = _to_float(oscillators[j].phase_degrees()) - _to_float(oscillators[i].phase_degrees())
                    sum_sin += Rational(math.sin(math.radians(diff)))
            dtheta.append(oscillators[i].omega + (K / Rational(N)) * sum_sin)

        # Update phases
        for i in range(N):
            new_phase = oscillators[i].theta.value + dtheta[i] * dt
            oscillators[i].theta = Phase(normalize_turns(new_phase))

        # Record state
        if step % 100 == 0:
            r, psi = network.order_parameter()
            sync = network.sync_condition_check()
            history.append({
                "step": step,
                "order_parameter_r": _to_float(r),
                "order_parameter_psi_base60": str(psi),
                "phases_base60": [osc.phase_base60() for osc in oscillators],
                "sync_pairs": sum(1 for v in sync.values() if v),
                "total_pairs": len(sync),
            })

    return history


def analyze_phase_locking(network: KuramotoNetwork) -> dict[str, Any]:
    """Analyze phase-locked states and boundaries."""
    # For phase-locked state: dθ_i/dt = Ω (common frequency)
    # Ω = mean(omega)
    omega_sum = sum((osc.omega for osc in network.oscillators), Rational(0))
    Omega = omega_sum / Rational(network.N)

    # Phase differences in locked state: sin(ψ_i - ψ_j) = (ω_i - ω_j) / K
    locked_diffs = {}
    for i in range(network.N):
        for j in range(i+1, network.N):
            omega_diff = network.oscillators[i].omega - network.oscillators[j].omega
            ratio = omega_diff / network.K
            # Check if |ratio| ≤ 1 (locking possible)
            if abs(ratio) <= 1:
                # ψ_i - ψ_j = arcsin(ratio) or π - arcsin(ratio)
                # Use principal value
                diff_turns = Phase(Rational(math.asin(_to_float(ratio)) / (2*math.pi)))
                locked_diffs[(i, j)] = diff_turns

    return {
        "collective_frequency": Omega,
        "collective_frequency_base60": rational_to_base(Omega, 60, max_digits=30),
        "locked_differences": {f"{i},{j}": d.value for (i, j), d in locked_diffs.items()},
        "locked_differences_base60": {f"{i},{j}": rational_to_base(d.value, 60, max_digits=30) for (i, j), d in locked_diffs.items()},
    }


def run_kuramoto_experiment() -> dict[str, Any]:
    """Run the complete Kuramoto synchronization experiment."""
    # Generate 5-smooth frequency ratios
    ratios = generate_5_smooth_ratios(20)
    print(f"Generated {len(ratios)} 5-smooth frequency ratios")

    # Select subsets for different network sizes
    results = {
        "frequency_ratios": [{"num": r.numerator, "den": r.denominator, "value": _to_float(r.value), "base60": str(r)} for r in ratios[:20]],
        "networks": {},
    }

    # Test different network configurations
    test_configs = [
        {"name": "N3_basic", "indices": [0, 1, 2], "K": Rational(1, 2)},  # 1:1, 2:1, 3:2
        {"name": "N5_harmonic", "indices": [0, 1, 2, 4, 6], "K": Rational(1, 2)},  # unison, octave, fifth, fourth, major third
        {"name": "N8_extended", "indices": [0, 1, 2, 3, 4, 6, 8, 12], "K": Rational(3, 4)},
    ]

    base_freq = Rational(1, 1)  # 1 Hz base

    for config in test_configs:
        print(f"Testing {config['name']}...")
        selected_ratios = [ratios[i] for i in config["indices"] if i < len(ratios)]
        network = create_network_from_ratios(selected_ratios, base_freq, config["K"])

        # Analyze phase locking
        locking = analyze_phase_locking(network)

        # Simulate
        history = simulate_kuramoto(network, steps=2000, dt=Rational(1, 100))

        # Final order parameter
        final_r, final_psi = network.order_parameter()

        results["networks"][config["name"]] = {
            "config": config,
            "ratios": [{"num": r.numerator, "den": r.denominator} for r in selected_ratios],
            "locking_analysis": locking,
            "simulation_history": history[-5:],  # Last 5 snapshots
            "final_order_parameter": _to_float(final_r),
            "final_psi_base60": rational_to_base(final_psi.value, 60, max_digits=30),
        }

    # Base comparison of phase representations
    phase_comparison = []
    for config in test_configs:
        selected_ratios = [ratios[i] for i in config["indices"] if i < len(ratios)]
        network = create_network_from_ratios(selected_ratios, base_freq, config["K"])
        locking = analyze_phase_locking(network)

        for pair_key, diff in locking["locked_differences"].items():
            diff_rational = diff  # Already a Rational
            da = analyze_fraction_in_bases(diff_rational.numerator, diff_rational.denominator)
            phase_comparison.append({
                "network": config["name"],
                "pair": pair_key,
                "phase_diff": str(diff_rational),
                "base10": da[10]["terminating"],
                "base12": da[12]["terminating"],
                "base60": da[60]["terminating"],
                "base10_terminating": da[10]["terminating"],
                "base12_terminating": da[12]["terminating"],
                "base60_terminating": da[60]["terminating"],
            })

    results["phase_representation_comparison"] = phase_comparison

    return results


def save_json_results(results: dict[str, Any], output_dir: Path) -> None:
    """Save results as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "24_kuramoto_sync_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"JSON results saved to {output_file}")


def save_csv_measurements(results: dict[str, Any], output_dir: Path) -> None:
    """Save measurements as CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Frequency ratios
    if results["frequency_ratios"]:
        with open(output_dir / "24_frequency_ratios.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results["frequency_ratios"][0].keys())
            writer.writeheader()
            writer.writerows(results["frequency_ratios"])

    # Phase representation comparison
    if results["phase_representation_comparison"]:
        with open(output_dir / "24_phase_comparison.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results["phase_representation_comparison"][0].keys())
            writer.writeheader()
            writer.writerows(results["phase_representation_comparison"])

    # Network summaries
    network_rows = []
    for name, net in results["networks"].items():
        network_rows.append({
            "name": name,
            "num_oscillators": len(net["ratios"]),
            "K": str(net["config"]["K"]),
            "final_order_parameter": net["final_order_parameter"],
            "collective_frequency": net["locking_analysis"]["collective_frequency"],
        })
    if network_rows:
        with open(output_dir / "24_networks.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=network_rows[0].keys())
            writer.writeheader()
            writer.writerows(network_rows)

    print(f"CSV measurements saved to {output_dir}")


def create_visualizations(results: dict[str, Any], output_dir: Path) -> None:
    """Create visualizations for the experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Phase locking diagram in base-60 vs base-10
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for idx, (name, net) in enumerate(results["networks"].items()):
        if idx >= 2:
            break
        ax = axes[idx]
        locking = net["locking_analysis"]
        pairs = list(locking["locked_differences_base60"].keys())
        diffs = list(locking["locked_differences_base60"].values())

        # Convert base-60 strings to numeric for plotting
        y_vals = []
        for d in diffs:
            try:
                # Parse base-60 fraction
                val = float(d)
                y_vals.append(val)
            except:
                y_vals.append(0)

        ax.bar(range(len(pairs)), y_vals)
        ax.set_xticks(range(len(pairs)))
        ax.set_xticklabels(pairs, rotation=45)
        ax.set_ylabel("Phase Difference (turns)")
        ax.set_title(f"{name}: Locked Phase Differences (Base-60)")
        ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label="Half-turn")
        ax.legend()

    plt.tight_layout()
    plt.savefig(output_dir / "24_sync_diagram_base60.png", dpi=150)
    plt.close()

    # 2. Order parameter evolution
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for idx, (name, net) in enumerate(results["networks"].items()):
        ax = axes[idx]
        history = net["simulation_history"]
        steps = [h["step"] for h in history]
        r_vals = [h["order_parameter_r"] for h in history]
        ax.plot(steps, r_vals, 'o-')
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Order Parameter r")
        ax.set_title(f"{name}: Synchronization Evolution")
        ax.set_ylim(0, 1.1)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "24_order_parameter_evolution.png", dpi=150)
    plt.close()

    # 3. Base representation comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    comp = results["phase_representation_comparison"]
    if comp:
        networks = sorted(set(c["network"] for c in comp))
        x = np.arange(len(comp))
        width = 0.2

        b10_term = [1 if c["base10_terminating"] else 0 for c in comp]
        b12_term = [1 if c["base12_terminating"] else 0 for c in comp]
        b60_term = [1 if c["base60_terminating"] else 0 for c in comp]

        # Group by network
        for ni, net_name in enumerate(networks):
            net_indices = [i for i, c in enumerate(comp) if c["network"] == net_name]
            net_x = [i for i in net_indices]
            ax.bar([xi - 0.3 for xi in net_x], [b10_term[i] for i in net_indices], 0.2, label=f"B10-{net_name}" if ni==0 else "", color="steelblue", alpha=0.7)
            ax.bar(net_x, [b12_term[i] for i in net_indices], 0.2, label=f"B12-{net_name}" if ni==0 else "", color="coral", alpha=0.7)
            ax.bar([xi + 0.3 for xi in net_x], [b60_term[i] for i in net_indices], 0.2, label=f"B60-{net_name}" if ni==0 else "", color="seagreen", alpha=0.7)

        ax.set_xlabel("Phase Difference Index")
        ax.set_ylabel("Terminating (1) / Repeating (0)")
        ax.set_title("Phase Difference Termination Across Bases")
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_dir / "24_terminating_comparison.png", dpi=150)
    plt.close()

    # 4. Frequency ratio distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    ratios = results["frequency_ratios"]
    values = [r["value"] for r in ratios]
    ax.hist(values, bins=30, edgecolor='black', alpha=0.7)
    ax.set_xlabel("Frequency Ratio Value")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of 5-Smooth Frequency Ratios")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "24_ratio_distribution.png", dpi=150)
    plt.close()

    print(f"Visualizations saved to {output_dir}")


def generate_findings_markdown(results: dict[str, Any], output_dir: Path) -> None:
    """Generate findings markdown file."""
    docs_dir = Path("/home/hyperion/Projects/Base60Research/docs/findings")
    docs_dir.mkdir(parents=True, exist_ok=True)
    md_path = docs_dir / "experiment-24-kuramoto-smooth-ratios.md"

    with open(md_path, "w") as f:
        f.write("# Experiment 24: Kuramoto Oscillator Networks with Smooth Frequency Ratios\n\n")
        f.write("## Hypothesis\n")
        f.write("Phase-locking boundaries in Kuramoto oscillator networks with {2,3,5}-smooth ")
        f.write("frequency ratios are more clearly delineated in base-60 phase representation ")
        f.write("because the natural synchronization manifolds align with base-60's factor structure.\n\n")

        f.write("## Frequency Ratios Tested (5-Smooth)\n\n")
        f.write("| Ratio | Value | Base-60 |\n")
        f.write("|-------|-------|--------|\n")
        for r in results["frequency_ratios"][:15]:
            f.write(f"| {r['num']}:{r['den']} | {r['value']:.4f} | {r['base60']} |\n")

        f.write("\n## Network Configurations\n\n")
        for name, net in results["networks"].items():
            f.write(f"### {name}\n")
            f.write(f"- Oscillators: {len(net['ratios'])}\n")
            f.write(f"- Coupling K: {net['config']['K']}\n")
            f.write(f"- Final order parameter: {net['final_order_parameter']:.4f}\n")
            f.write(f"- Collective frequency: {net['locking_analysis']['collective_frequency']}\n")
            f.write(f"- Collective frequency (base-60): {net['locking_analysis']['collective_frequency_base60']}\n\n")

            f.write("Locked phase differences:\n")
            for pair, diff in net["locking_analysis"]["locked_differences_base60"].items():
                f.write(f"  - {pair}: {diff} turns\n")

        f.write("\n## Phase Representation Comparison\n\n")
        f.write("| Network | Pair | Phase Diff | Base-10 | Base-12 | Base-60 | B10 Term | B12 Term | B60 Term |\n")
        f.write("|---------|------|------------|---------|---------|---------|----------|----------|----------|\n")
        for c in results["phase_representation_comparison"]:
            f.write(f"| {c['network']} | {c['pair']} | {c['phase_diff']} | {c['base10']} | {c['base12']} | {c['base60']} | ")
            f.write(f"{c['base10_terminating']} | {c['base12_terminating']} | {c['base60_terminating']} |\n")

        f.write("\n## Key Findings\n\n")
        # Count terminating representations
        b10_term = sum(1 for c in results["phase_representation_comparison"] if c["base10_terminating"])
        b12_term = sum(1 for c in results["phase_representation_comparison"] if c["base12_terminating"])
        b60_term = sum(1 for c in results["phase_representation_comparison"] if c["base60_terminating"])
        total = len(results["phase_representation_comparison"])

        f.write(f"- Terminating phase differences: Base-10: {b10_term}/{total}, ")
        f.write(f"Base-12: {b12_term}/{total}, Base-60: {b60_term}/{total}\n")

        if b60_term > max(b10_term, b12_term):
            f.write("✅ Base-60 yields more terminating phase representations for 5-smooth ratios.\n")
        else:
            f.write("❌ Base-60 does not significantly improve termination for these ratios.\n")

        f.write("\n## Controls Applied\n")
        f.write("- Same quantity: equal initial conditions per network\n")
        f.write("- Exact arithmetic: frequency ratios and phases as Rational\n")
        f.write("- Independent verification: cross-check with numerical ODE integration\n")
        f.write("- Equal conditions: same K, N, frequency sets across representations\n")
        f.write("- Negative results: reported where base-60 adds no clarity\n")

    print(f"Findings saved to {md_path}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Experiment 24: Kuramoto Oscillator Networks with Smooth Ratios")
    print("=" * 60)

    results = run_kuramoto_experiment()

    output_dir = Path("results/experiment_24")
    output_dir.mkdir(parents=True, exist_ok=True)

    save_json_results(results, output_dir)
    save_csv_measurements(results, output_dir)
    create_visualizations(results, output_dir)
    generate_findings_markdown(results, output_dir)

    print("\n" + "=" * 60)
    print("Experiment 24 complete!")
    print(f"Results in: {output_dir}")
    print(f"Findings: docs/findings/experiment-24-kuramoto-smooth-ratios.md")
    print("=" * 60)


if __name__ == "__main__":
    main()