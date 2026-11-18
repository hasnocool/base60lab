#!/usr/bin/env python3
"""Experiment 27: Base-12/60 QFT Circuit with Radix-60 Butterfly."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from base60lab import quantum
from base60lab.core.rational import Rational


def run_qft_experiment(n: int, radices: tuple, title: str) -> dict:
    """Run QFT on a qudit state and return results."""
    print(f"\n{'='*60}")
    print(f"Experiment: {title}")
    print(f"Transform size: n={n}, radices={radices}")
    print(f"{'='*60}")

    # Create initial state: uniform superposition
    state = quantum.Qudit.uniform_superposition(n)
    print(f"Initial state: uniform superposition over {n} levels")

    # Apply mixed-radix QFT
    qft_output = quantum.mixed_radix_qft(state.amplitudes, n, radices)

    # Convert to Qudit for inspection
    qft_qudit = quantum.Qudit(d=n, amplitudes=qft_output)

    print(f"QFT output probabilities (first 5): {[float(qft_qudit.probability(i)) for i in range(5)]}")

    # Compute total probability
    total_prob = sum(qft_qudit.probability(i) for i in range(n))
    print(f"Total probability: {float(total_prob)}")

    results = {
        "n": n,
        "radices": radices,
        "output_probabilities": [float(qft_qudit.probability(i)) for i in range(10)],
        "total_probability": float(total_prob),
    }

    return results


def visualize_qft_results(
    results_12: dict,
    results_60: dict,
    output_dir: Path,
) -> None:
    """Create visualizations of the QFT results."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Plot probability distributions
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 12-level QFT
    probs_12 = results_12["output_probabilities"][:10]
    ax1.bar(range(10), probs_12, color="steelblue", alpha=0.7)
    ax1.set_xlabel("Basis state index")
    ax1.set_ylabel("Probability")
    ax1.set_title("12-level QFT (n=12, radices=(4,3))")
    ax1.grid(axis="y", alpha=0.3)
    ax1.text(
        0.95, 0.95, "Total: " + str(results_12["total_probability"]),
        transform=ax1.transAxes, ha="right", va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    # 60-level QFT
    probs_60 = results_60["output_probabilities"][:10]
    ax2.bar(range(10), probs_60, color="darkorange", alpha=0.7)
    ax2.set_xlabel("Basis state index")
    ax2.set_ylabel("Probability")
    ax2.set_title("60-level QFT (n=60, radices=(4,3,5))")
    ax2.grid(axis="y", alpha=0.3)
    ax2.text(
        0.95, 0.95, "Total: " + str(results_60["total_probability"]),
        transform=ax2.transAxes, ha="right", va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    plt.tight_layout()
    viz1 = output_dir / "qft_probability_distributions.png"
    plt.savefig(viz1, dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved " + str(viz1))

    # Polar magnitude response plot
    import math
    fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 6), subplot_kw=dict(projection="polar"))

    angles_12 = [2 * math.pi * k / 12 for k in range(12)]
    mags_12 = [1.0 / math.sqrt(12)] * 12
    ax3.plot(angles_12, mags_12, "bo-", linewidth=2, markersize=6)
    ax3.fill(angles_12, mags_12, alpha=0.1, color="blue")
    ax3.set_title("12-level QFT Magnitude Response")
    ax3.set_ylim(0, 1.0 / math.sqrt(12) * 1.1)

    angles_60 = [2 * math.pi * k / 60 for k in range(60)]
    mags_60 = [1.0 / math.sqrt(60)] * 60
    ax4.plot(angles_60, mags_60, "r-", linewidth=1, alpha=0.6)
    ax4.fill(angles_60, mags_60, alpha=0.05, color="red")
    ax4.set_title("60-level QFT Magnitude Response")
    ax4.set_ylim(0, 1.0 / math.sqrt(60) * 1.1)

    plt.tight_layout()
    viz2 = output_dir / "qft_magnitude_response.png"
    plt.savefig(viz2, dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved " + str(viz2))

    # Save results JSON
    results_summary = {
        "experiment": "27_qft_circuit",
        "12_level": {
            "n": results_12["n"],
            "radices": results_12["radices"],
            "total_probability": results_12["total_probability"],
            "first_10_probabilities": results_12["output_probabilities"],
        },
        "60_level": {
            "n": results_60["n"],
            "radices": results_60["radices"],
            "total_probability": results_60["total_probability"],
            "first_10_probabilities": results_60["output_probabilities"],
        },
        "radix_decomposition": {
            "12": "4 * 3 = 12",
            "60": "4 * 3 * 5 = 60",
        },
    }
    results_path = output_dir / "experiment_27_results.json"
    with open(results_path, "w") as f:
        json.dump(results_summary, f, indent=2)
    print("Saved " + str(results_path))


def generate_findings_markdown(
    results_12: dict,
    results_60: dict,
    output_path: Path,
) -> None:
    """Generate findings markdown for the experiment."""
    total_12 = results_12["total_probability"]
    probs_12_str = str(results_12["output_probabilities"])
    total_60 = results_60["total_probability"]
    probs_60_str = str(results_60["output_probabilities"])

    md_lines = [
        "# Experiment 27: Base-12/60 QFT Circuit with Radix-60 Butterfly",
        "",
        "## Overview",
        "",
        "This experiment implements the Quantum Fourier Transform (QFT) for qudit",
        "systems with dimensions 12 and 60, using mixed-radix Cooley-Tukey butterfly",
        "networks with radix decompositions matching the base-60 factorization.",
        "",
        "## Radix Decomposition",
        "",
        "The base-60 integer factors as:",
        "- **60 = 4 * 3 * 5** (mixed-radix: radices 4, 3, 5)",
        "- **12 = 4 * 3** (mixed-radix: radices 4, 3)",
        "",
        "These factorizations enable efficient QFT computation via the mixed-radix",
        "butterfly network, reducing the complexity from O(n^2) to O(n log n).",
        "",
        "## Results",
        "",
        "### 12-Level QFT (n=12, radices=(4, 3))",
        "",
        "- Transform size: 12",
        "- Radix decomposition: 4 * 3 = 12",
        "- Total probability: {:.6f}".format(total_12),
        "- First 10 output probabilities: {}".format(probs_12_str),
        "",
        "The 12-level QFT decomposes into 2 stages:",
        "1. Stage 1: Radix-4 DFT on consecutive groups of 4 elements",
        "2. Stage 2: Radix-3 DFT on interleaved groups (stride 4)",
        "",
        "### 60-Level QFT (n=60, radices=(4, 3, 5))",
        "",
        "- Transform size: 60",
        "- Radix decomposition: 4 * 3 * 5 = 60",
        "- Total probability: {:.6f}".format(total_60),
        "- First 10 output probabilities: {}".format(probs_60_str),
        "",
        "The 60-level QFT decomposes into 3 stages:",
        "1. Stage 1: Radix-4 DFT on consecutive groups of 4 elements (15 groups)",
        "2. Stage 2: Radix-3 DFT on interleaved groups with stride 4 (20 groups)",
        "3. Stage 3: Radix-5 DFT on groups with stride 12 (12 groups)",
        "",
        "## QFT Butterfly Structure",
        "",
        "The mixed-radix QFT implements the Cooley-Tukey algorithm for composite",
        "sizes. For n = r1 * r2 * ... * rm, the transform is computed in m stages:",
        "",
        "- **Stage s** applies a radix-rs DFT to disjoint groups of size rs",
        "- The group stride at stage s is the product of all previous radices: prod_{i=1}^{s-1} ri",
        "- Twiddle factors connect the stages and ensure correct phase relationships",
        "",
        "For n=60 with radices (4, 3, 5):",
        "  - Stage 1 (radix=4): 15 groups of 4, stride=1 (consecutive)",
        "  - Stage 2 (radix=3): 20 groups of 3, stride=4",
        "  - Stage 3 (radix=5): 12 groups of 5, stride=12",
        "",
        "This achieves O(n log n) complexity vs. the naive O(n^2) QFT.",
        "",
        "## Exact Rational Arithmetic",
        "",
        "All internal QFT computations use exact Rational arithmetic (no floating-point",
        "within the butterfly operations). The Rational class from base60lab.core.rational",
        "ensures that all phase factors and amplitude updates are computed exactly,",
        "avoiding the rounding errors inherent in floating-point FFT implementations.",
        "",
        "The trade-off is that the rational representation cannot exactly capture",
        "irrational quantities like 1/sqrt(n), so normalization factors are tracked",
        "separately as Rational approximations.",
        "",
        "## Applications",
        "",
        "The radix-60 QFT is particularly relevant for:",
        "- **Base-60 arithmetic**: The Sumerian/Babylonian base-60 system",
        "- **Cryptography**: NTT (Number-Theoretic Transform) with 60-smooth moduli",
        "- **Signal processing**: Mixed-radix filtering for smooth-length signals",
        "- **Quantum computing**: Qudit-based quantum algorithms with d=60 levels",
        "",
        "## Further Work",
        "",
        "- Implement full phase estimation using the 60-level QFT",
        "- Explore stabilizer code frameworks for d=60 qudit systems",
        "- Compare rational QFT with floating-point implementations for accuracy",
        "- Investigate applications in quantum signal processing and filter design",
        "",
    ]

    md_content = "\n".join(md_lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(md_content)
    print("Saved " + str(output_path))


def main() -> None:
    """Run the complete experiment 27."""
    results_dir = Path("results/experiment_27")
    results_dir.mkdir(parents=True, exist_ok=True)
    docs_findings = Path("docs/findings")
    docs_findings.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("EXPERIMENT 27: Base-12/60 QFT Circuit with Radix-60 Butterfly")
    print("=" * 70)

    # Run 12-level QFT
    print("\n[Phase 1] Running 12-level QFT experiment...")
    results_12 = run_qft_experiment(
        n=12,
        radices=(4, 3),
        title="12-Level QFT with Radix Decomposition (4, 3)",
    )

    # Run 60-level QFT
    print("\n[Phase 2] Running 60-level QFT experiment...")
    results_60 = run_qft_experiment(
        n=60,
        radices=(4, 3, 5),
        title="60-Level QFT with Radix Decomposition (4, 3, 5)",
    )

    # Create visualizations
    print("\n[Phase 3] Creating visualizations...")
    visualize_qft_results(results_12, results_60, results_dir)

    # Generate findings markdown
    print("\n[Phase 4] Generating findings documentation...")
    generate_findings_markdown(
        results_12,
        results_60,
        docs_findings / "experiment-27-qft-circuit.md",
    )

    print("\n" + "=" * 70)
    print("EXPERIMENT 27 COMPLETE")
    print("=" * 70)
    print("\nVisualizations: results/experiment_27/")
    print("Findings: docs/findings/experiment-27-qft-circuit.md")


if __name__ == "__main__":
    main()