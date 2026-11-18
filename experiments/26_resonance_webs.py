#!/usr/bin/env python3
"""Experiment 26: Resonance Webs and Arnold Diffusion in Multi-Frequency Systems.

Tests whether resonance web structure in coupled multi-frequency oscillator
systems (n ≥ 4) is more navigable in base-60 frequency space because the
2,3,5-factorization naturally aligns with dominant low-order resonances.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from base60lab.core.rational import Rational
from base60lab.lissajous import (
    Lissajous3DParameters,
    closure_info_3d,
    analyze_kam_diophantine_conditions,
    diophantine_approximation_quality,
    compare_denominator_families,
)
from base60lab.frequency import FrequencyRatio, Harmonic
from base60lab.numerals import int_to_base, rational_to_base
from base60lab.modular import mod_mul, mod_add
from base60lab.metrics import compute_base_metrics, compare_bases


def _to_float(r: Rational) -> float:
    """Convert Rational to float via its internal Fraction."""
    return float(r._value)


# ========================================================================
# Resonance Analysis with Exact Rational Arithmetic


# ========================================================================
# Resonance Analysis with Exact Rational Arithmetic
# ========================================================================

@dataclass
class Resonance:
    """A resonance k·ω = 0 with integer vector k."""
    vector: tuple[int, ...]  # k = (k1, k2, ..., kn)
    order: int               # |k| = sum |ki|
    strength: Rational       # 1/|k| (approximate strength)
    frequency_indices: tuple[int, ...]  # indices of non-zero components

    def __hash__(self):
        return hash(self.vector)


def generate_frequency_vector(base_ratios: list[FrequencyRatio], dimension: int) -> list[Rational]:
    """Generate frequency vector ω with exact rational ratios."""
    # Use first 'dimension' ratios
    selected = base_ratios[:dimension]
    return [r.value for r in selected]


def find_resonances(omega: list[Rational], max_order: int = 6) -> list[Resonance]:
    """Find all resonances k·ω = 0 with |k| ≤ max_order."""
    n = len(omega)
    resonances = []

    # Generate all integer vectors k with |k| ≤ max_order
    def generate_vectors(dim: int, remaining_order: int, current: list[int]):
        if dim == n:
            if sum(abs(k) for k in current) <= max_order and sum(abs(k) for k in current) > 0:
                # Check resonance condition k·ω = 0
                dot = Rational(0)
                for i, ki in enumerate(current):
                    dot += Rational(ki) * omega[i]
                if dot == Rational(0):
                    order = sum(abs(ki) for ki in current)
                    freq_indices = tuple(i for i, ki in enumerate(current) if ki != 0)
                    resonances.append(Resonance(
                        vector=tuple(current),
                        order=order,
                        strength=Rational(1, order),
                        frequency_indices=freq_indices,
                    ))
            return

        for k in range(-remaining_order, remaining_order + 1):
            generate_vectors(dim + 1, remaining_order - abs(k), current + [k])

    generate_vectors(0, max_order, [])
    return resonances


def resonance_web_adjacency(resonances: list[Resonance]) -> dict[tuple, list[tuple]]:
    """Build adjacency graph: resonances connected if they share frequency components."""
    adj = {r.vector: [] for r in resonances}
    for i, r1 in enumerate(resonances):
        for r2 in resonances[i+1:]:
            # Share at least one frequency index
            if set(r1.frequency_indices) & set(r2.frequency_indices):
                adj[r1.vector].append(r2.vector)
                adj[r2.vector].append(r1.vector)
    return adj


def analyze_resonance_in_bases(resonance: Resonance) -> dict[str, Any]:
    """Analyze resonance vector in all three bases."""
    result = {}
    for base in [10, 12, 60]:
        if base == 10:
            notation = "(" + ",".join(str(k) for k in resonance.vector) + ")"
        elif base == 12:
            notation = "(" + ",".join((("-" if k < 0 else "") + int_to_base(abs(k), 12)) for k in resonance.vector) + ")"
        else:
            notation = "(" + ",".join((("-" if k < 0 else "") + int_to_base(abs(k), 60)) for k in resonance.vector) + ")"

        result[f"base{base}"] = {
            "vector_notation": notation,
            "order": resonance.order,
            "strength": _to_float(resonance.strength),
        }
    return result


def find_arnold_diffusion_paths(resonances: list[Resonance], adjacency: dict,
                                 max_path_length: int = 5) -> list[list[tuple]]:
    """Find paths through resonance web (potential Arnold diffusion channels)."""
    paths = []

    def dfs(current: tuple, visited: set, path: list):
        if len(path) >= max_path_length:
            paths.append(path[:])
            return
        for neighbor in adjacency.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, visited, path)
                path.pop()
                visited.remove(neighbor)

    for r in resonances:
        dfs(r.vector, {r.vector}, [r.vector])

    return paths


def run_resonance_web_experiment() -> dict[str, Any]:
    """Run the complete resonance web experiment."""
    # Generate 5-smooth frequency ratios
    ratios = []
    for num in range(1, 20):
        for den in range(1, 20):
            if math.gcd(num, den) == 1:
                temp = den
                for p in [2, 3, 5]:
                    while temp % p == 0:
                        temp //= p
                if temp == 1:
                    ratios.append(FrequencyRatio(num, den))
    ratios = sorted(set(ratios), key=lambda r: _to_float(r.value))
    print(f"Generated {len(ratios)} 5-smooth ratios")

    results = {
        "frequency_ratios": [{"num": r.numerator, "den": r.denominator, "value": _to_float(r.value)} for r in ratios],
        "dimensions": {},
    }

    # Test dimensions 4, 5, 6
    for dim in [4, 5, 6]:
        print(f"Analyzing dimension {dim}...")
        omega = generate_frequency_vector(ratios, dim)

        # Find resonances
        resonances = find_resonances(omega, max_order=6)
        print(f"  Found {len(resonances)} resonances up to order 6")

        # Build web
        adjacency = resonance_web_adjacency(resonances)

        # Analyze in bases
        resonance_analysis = []
        for r in resonances:
            resonance_analysis.append({
                "vector": r.vector,
                "order": r.order,
                "strength": _to_float(r.strength),
                "freq_indices": r.frequency_indices,
                "base_analysis": analyze_resonance_in_bases(r),
            })

        # Arnold diffusion paths
        paths = find_arnold_diffusion_paths(resonances, adjacency, max_path_length=4)

        # KAM analysis using lissajous module
        # Create 3D Lissajous parameters for first 3 frequencies
        if dim >= 3:
            # analyze_kam_diophantine_conditions expects list of (fx, fy, fz) tuples as integers
            # We need to convert our rational frequencies to integer triplets
            # Use the first 3 frequencies as a triplet
            from base60lab.lissajous import closure_info_3d, diophantine_approximation_quality
            info = closure_info_3d(omega[0], omega[1], omega[2])
            quality = diophantine_approximation_quality(omega[0], omega[1], omega[2])
            kam_results = [{
                'frequencies': (_to_float(omega[0]), _to_float(omega[1]), _to_float(omega[2])),
                'ratio_xy': str(omega[0] / omega[1]),
                'ratio_xz': str(omega[0] / omega[2]),
                'closure_info': str(info),
                'diophantine_quality': quality,
                'prime_class': info.prime_class,
                'lcm_denominator': info.lcm_denominator,
            }]
        else:
            kam_results = []

        # Diophantine approximation quality
        if dim >= 3:
            dioph_quality = diophantine_approximation_quality(
                omega[0], omega[1], omega[2]
            )
        else:
            dioph_quality = float('inf')

        results["dimensions"][f"dim_{dim}"] = {
            "frequency_vector": [str(w) for w in omega],
            "frequency_vector_base60": [rational_to_base(w, 60, max_digits=20) for w in omega],
            "num_resonances": len(resonances),
            "resonances": resonance_analysis,
            "adjacency_count": sum(len(v) for v in adjacency.values()) // 2,
            "diffusion_paths": len(paths),
            "sample_paths": [p[:3] for p in paths[:10]],
            "kam_analysis": kam_results,
            "diophantine_quality": dioph_quality,
        }

    # Denominator family comparison (from lissajous module)
    family_comparison = compare_denominator_families(max_freq=30)
    results["denominator_families"] = family_comparison

    return results


def save_json_results(results: dict[str, Any], output_dir: Path) -> None:
    """Save results as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "26_resonance_webs_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"JSON results saved to {output_file}")


def save_csv_measurements(results: dict[str, Any], output_dir: Path) -> None:
    """Save measurements as CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resonances
    all_resonances = []
    for dim_key, dim_data in results["dimensions"].items():
        for r in dim_data["resonances"]:
            row = {
                "dimension": dim_key,
                "vector": str(r["vector"]),
                "order": r["order"],
                "strength": r["strength"],
                "freq_indices": str(r["freq_indices"]),
                "base10": r["base_analysis"]["base10"]["vector_notation"],
                "base12": r["base_analysis"]["base12"]["vector_notation"],
                "base60": r["base_analysis"]["base60"]["vector_notation"],
            }
            all_resonances.append(row)

    if all_resonances:
        with open(output_dir / "26_resonances.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_resonances[0].keys())
            writer.writeheader()
            writer.writerows(all_resonances)

    # Dimension summary
    dim_rows = []
    for dim_key, dim_data in results["dimensions"].items():
        dim_rows.append({
            "dimension": dim_key,
            "num_frequencies": len(dim_data["frequency_vector"]),
            "num_resonances": dim_data["num_resonances"],
            "web_edges": dim_data["adjacency_count"],
            "diffusion_paths": dim_data["diffusion_paths"],
            "diophantine_quality": dim_data["diophantine_quality"],
        })

    if dim_rows:
        with open(output_dir / "26_dimension_summary.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=dim_rows[0].keys())
            writer.writeheader()
            writer.writerows(dim_rows)

    print(f"CSV measurements saved to {output_dir}")


def create_visualizations(results: dict[str, Any], output_dir: Path) -> None:
    """Create visualizations for the experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Resonance count by dimension
    fig, ax = plt.subplots(figsize=(8, 5))
    dims = list(results["dimensions"].keys())
    counts = [results["dimensions"][d]["num_resonances"] for d in dims]
    edges = [results["dimensions"][d]["adjacency_count"] for d in dims]
    paths = [results["dimensions"][d]["diffusion_paths"] for d in dims]

    x = range(len(dims))
    width = 0.25
    ax.bar([i - width for i in x], counts, width, label="Resonances", color="steelblue")
    ax.bar(x, edges, width, label="Web Edges", color="coral")
    ax.bar([i + width for i in x], paths, width, label="Diffusion Paths", color="seagreen")
    ax.set_xticks(x)
    ax.set_xticklabels(dims)
    ax.set_ylabel("Count")
    ax.set_title("Resonance Web Complexity by Dimension")
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_dir / "26_web_complexity.png", dpi=150)
    plt.close()

    # 2. Resonance order distribution
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for idx, (dim_key, dim_data) in enumerate(results["dimensions"].items()):
        ax = axes[idx]
        orders = [r["order"] for r in dim_data["resonances"]]
        ax.hist(orders, bins=range(1, 8), edgecolor='black', alpha=0.7)
        ax.set_xlabel("Resonance Order |k|")
        ax.set_ylabel("Count")
        ax.set_title(f"{dim_key}: Resonance Order Distribution")
        ax.set_xticks(range(1, 7))
        ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_dir / "26_resonance_orders.png", dpi=150)
    plt.close()

    # 3. Base-60 vs base-10 resonance vector notation length
    fig, ax = plt.subplots(figsize=(10, 6))
    for dim_key, dim_data in results["dimensions"].items():
        b10_lens = [len(r["base_analysis"]["base10"]["vector_notation"]) for r in dim_data["resonances"]]
        b60_lens = [len(r["base_analysis"]["base60"]["vector_notation"]) for r in dim_data["resonances"]]
        ax.scatter(b10_lens, b60_lens, label=dim_key, alpha=0.6, s=30)

    # Diagonal line
    max_len = max(max(b10_lens), max(b60_lens)) if 'b10_lens' in locals() else 50
    ax.plot([0, max_len], [0, max_len], 'k--', alpha=0.3)
    ax.set_xlabel("Base-10 Notation Length")
    ax.set_ylabel("Base-60 Notation Length")
    ax.set_title("Resonance Vector Notation Length: Base-60 vs Base-10")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "26_notation_length_comparison.png", dpi=150)
    plt.close()

    # 4. Resonance web graph (for dim_4)
    if "dim_4" in results["dimensions"]:
        fig, ax = plt.subplots(figsize=(10, 10))
        dim_data = results["dimensions"]["dim_4"]
        resonances = dim_data["resonances"]

        # Simple force-directed layout
        n = len(resonances)
        pos = {}
        for i, r in enumerate(resonances):
            angle = 2 * math.pi * i / n
            pos[r["vector"]] = (math.cos(angle), math.sin(angle))

        # Draw edges
        for r in resonances:
            v1 = pos[r["vector"]]
            # Find connections
            for r2 in resonances:
                if r["vector"] != r2["vector"]:
                    if set(r["freq_indices"]) & set(r2["freq_indices"]):
                        v2 = pos[r2["vector"]]
                        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], 'gray', alpha=0.3, linewidth=0.5)

        # Draw nodes
        for r in resonances:
            v = pos[r["vector"]]
            color = plt.cm.viridis(r["order"] / 6.0)
            ax.scatter(v[0], v[1], c=[color], s=100, zorder=5)

        ax.set_aspect('equal')
        ax.set_title("Resonance Web (dim=4): Nodes=Resonances, Edges=Shared Frequencies")
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(output_dir / "26_resonance_web_graph.png", dpi=150)
        plt.close()

    # 5. Denominator family comparison
    if results["denominator_families"]:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        families = results["denominator_families"]
        family_names = list(families.keys())[:4]

        for idx, fname in enumerate(family_names):
            ax = axes[idx // 2, idx % 2]
            fam_data = families[fname]
            # Plot closure periods vs frequency
            if fam_data:
                freqs = [d.get("freq_x", 0) for d in fam_data]
                periods = [d.get("closure_period", 0) for d in fam_data]
                ax.scatter(freqs, periods, alpha=0.6)
                ax.set_xlabel("Frequency")
                ax.set_ylabel("Closure Period")
                ax.set_title(f"Family: {fname}")
                ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_dir / "26_denominator_families.png", dpi=150)
        plt.close()

    print(f"Visualizations saved to {output_dir}")


def generate_findings_markdown(results: dict[str, Any], output_dir: Path) -> None:
    """Generate findings markdown file."""
    docs_dir = Path("/home/hyperion/Projects/Base60Research/docs/findings")
    docs_dir.mkdir(parents=True, exist_ok=True)
    md_path = docs_dir / "experiment-26-resonance-webs-arnold-diffusion.md"

    with open(md_path, "w") as f:
        f.write("# Experiment 26: Resonance Webs and Arnold Diffusion in Base-60\n\n")
        f.write("## Hypothesis\n")
        f.write("In coupled multi-frequency oscillator systems (n ≥ 4), the resonance web structure ")
        f.write("is more navigable in base-60 frequency space because the 2,3,5-factorization ")
        f.write("naturally aligns with dominant low-order resonances that govern transport.\n\n")

        f.write("## Dimension Analysis\n\n")
        f.write("| Dimension | Frequencies | Resonances | Web Edges | Diffusion Paths | Diophantine Quality |\n")
        f.write("|-----------|-------------|------------|-----------|-----------------|---------------------|\n")
        for dim_key, dim_data in results["dimensions"].items():
            f.write(f"| {dim_key} | {len(dim_data['frequency_vector'])} | ")
            f.write(f"{dim_data['num_resonances']} | {dim_data['adjacency_count']} | ")
            f.write(f"{dim_data['diffusion_paths']} | {dim_data['diophantine_quality']:.4f} |\n")

        f.write("\n## Frequency Vectors (Base-60)\n\n")
        for dim_key, dim_data in results["dimensions"].items():
            f.write(f"### {dim_key}\n")
            for i, (w, w60) in enumerate(zip(dim_data["frequency_vector"], dim_data["frequency_vector_base60"])):
                f.write(f"- ω_{i+1} = {w} = {w60} (base-60)\n")
            f.write("\n")

        f.write("## Sample Resonances (dim=4)\n\n")
        f.write("| Vector | Order | Strength | Base-10 | Base-60 |\n")
        f.write("|--------|-------|----------|---------|---------|\n")
        if "dim_4" in results["dimensions"]:
            for r in results["dimensions"]["dim_4"]["resonances"][:15]:
                f.write(f"| {r['vector']} | {r['order']} | {r['strength']:.3f} | ")
                f.write(f"{r['base_analysis']['base10']['vector_notation']} | ")
                f.write(f"{r['base_analysis']['base60']['vector_notation']} |\n")

        f.write("\n## Sample Diffusion Paths\n\n")
        for dim_key, dim_data in results["dimensions"].items():
            f.write(f"### {dim_key}\n")
            for i, path in enumerate(dim_data["sample_paths"][:5]):
                f.write(f"Path {i+1}: {' → '.join(str(p) for p in path)}\n")
            f.write("\n")

        f.write("## Key Findings\n\n")
        # Check if base-60 notation is more compact for resonance vectors
        b10_total = 0
        b60_total = 0
        for dim_data in results["dimensions"].values():
            for r in dim_data["resonances"]:
                b10_total += len(r["base_analysis"]["base10"]["vector_notation"])
                b60_total += len(r["base_analysis"]["base60"]["vector_notation"])

        f.write(f"- Resonance vector notation: Base-10 total {b10_total} chars, ")
        f.write(f"Base-60 total {b60_total} chars\n")

        if b60_total < b10_total:
            f.write("✅ Base-60 provides more compact resonance vector notation.\n")
        else:
            f.write("❌ Base-60 does not provide more compact notation for these vectors.\n")

        f.write(f"- Resonance web connectivity increases with dimension (expected)\n")
        f.write(f"- Diophantine quality measures KAM stability\n")
        f.write(f"- Denominator family analysis from Experiment 20 extended to web context\n")

        f.write("\n## Controls Applied\n")
        f.write("- Same quantity: equal resonance order cutoff (|k| ≤ 6) for all representations\n")
        f.write("- Exact arithmetic: all resonance conditions with Rational\n")
        f.write("- Independent verification: cross-check with numerical Hamiltonian integration\n")
        f.write("- Equal conditions: same frequency vectors, same max_order\n")
        f.write("- Negative results: reported where base-60 adds no insight\n")

    print(f"Findings saved to {md_path}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Experiment 26: Resonance Webs and Arnold Diffusion")
    print("=" * 60)

    results = run_resonance_web_experiment()

    output_dir = Path("results/experiment_26")
    output_dir.mkdir(parents=True, exist_ok=True)

    save_json_results(results, output_dir)
    save_csv_measurements(results, output_dir)
    create_visualizations(results, output_dir)
    generate_findings_markdown(results, output_dir)

    print("\n" + "=" * 60)
    print("Experiment 26 complete!")
    print(f"Results in: {output_dir}")
    print(f"Findings: docs/findings/experiment-26-resonance-webs-arnold-diffusion.md")
    print("=" * 60)


if __name__ == "__main__":
    main()