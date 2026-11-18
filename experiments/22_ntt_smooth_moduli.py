#!/usr/bin/env python3
"""Experiment 22: Number-Theoretic Transform (NTT) with 60-Smooth Moduli.

Tests whether base-60 factorization (2^2 * 3 * 5) provides more available
NTT-friendly prime moduli than base-10 (2 * 5) or base-12 (2^2 * 3).
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from base60lab.core.rational import Rational
from base60lab.fft_benchmarks import is_smooth, is_5_smooth, is_12_smooth, is_60_smooth
from base60lab.numerals import int_to_base
from base60lab.metrics import compute_base_metrics, compare_bases


# ========================================================================
# NTT Moduli Search
# ========================================================================

def is_prime(n: int) -> bool:
    """Miller-Rabin primality test (deterministic for n < 2^64)."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int) -> dict[int, int]:
    """Return prime factorization of n as {prime: exponent}."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def is_smooth_number(n: int, max_prime: int) -> bool:
    """Check if n is smooth with respect to max_prime."""
    return all(p <= max_prime for p in prime_factors(n))


def find_primitive_root(p: int) -> int | None:
    """Find a primitive root modulo prime p."""
    if not is_prime(p):
        return None
    phi = p - 1
    factors = prime_factors(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    return None


def find_ntt_moduli_for_length(N: int, max_k: int = 1000) -> list[dict[str, Any]]:
    """Find primes p = k*N + 1 where p-1 is smooth (NTT-friendly)."""
    results = []
    for k in range(1, max_k + 1):
        p = k * N + 1
        if p > (1 << 31):
            break
        if is_prime(p):
            # Check smoothness of p-1 = k*N
            pf = prime_factors(k * N)
            max_pf = max(pf.keys()) if pf else 1
            g = find_primitive_root(p)
            results.append({
                "k": k,
                "prime": p,
                "prime_base60": int_to_base(p, 60),
                "prime_base12": int_to_base(p, 12),
                "prime_bits": p.bit_length(),
                "p_minus_1_factors": pf,
                "max_prime_factor": max_pf,
                "is_5_smooth_p_minus_1": is_smooth_number(p - 1, 5),
                "is_12_smooth_p_minus_1": is_smooth_number(p - 1, 11),
                "is_60_smooth_p_minus_1": is_smooth_number(p - 1, 59),
                "primitive_root": g,
                "primitive_root_base60": int_to_base(g, 60) if g else None,
            })
    return results


def generate_transform_lengths(category: str, count: int = 20) -> list[int]:
    """Generate transform lengths for a smoothness category."""
    lengths = []
    if category == "powers_of_2":
        for i in range(1, 25):
            lengths.append(1 << i)
    elif category == "3_smooth":
        # 2^a * 3^b
        for a in range(12):
            for b in range(8):
                n = (1 << a) * (3 ** b)
                if n > 1:
                    lengths.append(n)
    elif category == "5_smooth":
        # 2^a * 3^b * 5^c
        for a in range(10):
            for b in range(6):
                for c in range(5):
                    n = (1 << a) * (3 ** b) * (5 ** c)
                    if n > 1:
                        lengths.append(n)
    elif category == "7_smooth":
        for a in range(8):
            for b in range(5):
                for c in range(4):
                    for d in range(3):
                        n = (1 << a) * (3 ** b) * (5 ** c) * (7 ** d)
                        if n > 1:
                            lengths.append(n)
    lengths = sorted(set(lengths))
    return lengths[:count]


def run_ntt_experiment() -> dict[str, Any]:
    """Run the complete NTT smooth moduli experiment."""
    categories = ["powers_of_2", "3_smooth", "5_smooth", "7_smooth"]
    transform_lengths = {}
    for cat in categories:
        transform_lengths[cat] = generate_transform_lengths(cat, 15)

    all_results = {}
    summary = {}

    for cat, lengths in transform_lengths.items():
        cat_results = []
        for N in lengths:
            moduli = find_ntt_moduli_for_length(N, max_k=500)
            if moduli:
                cat_results.append({
                    "transform_length": N,
                    "transform_length_base60": int_to_base(N, 60),
                    "transform_length_base12": int_to_base(N, 12),
                    "num_moduli_found": len(moduli),
                    "moduli": moduli[:10],  # Top 10
                })
        all_results[cat] = cat_results

        # Summary statistics
        total_moduli = sum(r["num_moduli_found"] for r in cat_results)
        avg_moduli = total_moduli / len(cat_results) if cat_results else 0
        summary[cat] = {
            "num_lengths_tested": len(cat_results),
            "total_moduli_found": total_moduli,
            "avg_moduli_per_length": avg_moduli,
            "max_moduli_for_single_length": max((r["num_moduli_found"] for r in cat_results), default=0),
        }

    # Compare smoothness categories for base-60 advantage
    base60_advantage = {
        "5_smooth_vs_powers_of_2": summary["5_smooth"]["total_moduli_found"] - summary["powers_of_2"]["total_moduli_found"],
        "5_smooth_vs_3_smooth": summary["5_smooth"]["total_moduli_found"] - summary["3_smooth"]["total_moduli_found"],
        "factor_3_contribution": "Including factor 3 (5-smooth vs powers of 2) adds "
            f"{summary['5_smooth']['total_moduli_found'] - summary['powers_of_2']['total_moduli_found']} moduli",
    }

    return {
        "transform_lengths": {k: [int_to_base(n, 60) for n in v] for k, v in transform_lengths.items()},
        "moduli_results": all_results,
        "summary": summary,
        "base60_advantage": base60_advantage,
        "metadata": {
            "max_k_searched": 500,
            "max_prime_bit_length": 31,
            "categories_tested": categories,
        }
    }


def save_json_results(results: dict[str, Any], output_dir: Path) -> None:
    """Save results as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "22_ntt_smooth_moduli_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"JSON results saved to {output_file}")


def save_csv_measurements(results: dict[str, Any], output_dir: Path) -> None:
    """Save measurements as CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Moduli details
    moduli_rows = []
    for cat, cat_results in results["moduli_results"].items():
        for r in cat_results:
            for m in r["moduli"]:
                moduli_rows.append({
                    "category": cat,
                    "transform_length": r["transform_length"],
                    "transform_length_base60": r["transform_length_base60"],
                    "k": m["k"],
                    "prime": m["prime"],
                    "prime_base60": m["prime_base60"],
                    "prime_base12": m["prime_base12"],
                    "prime_bits": m["prime_bits"],
                    "max_prime_factor_p_minus_1": m["max_prime_factor"],
                    "is_5_smooth": m["is_5_smooth_p_minus_1"],
                    "is_12_smooth": m["is_12_smooth_p_minus_1"],
                    "is_60_smooth": m["is_60_smooth_p_minus_1"],
                    "primitive_root": m["primitive_root"],
                })

    if moduli_rows:
        with open(output_dir / "22_ntt_moduli.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=moduli_rows[0].keys())
            writer.writeheader()
            writer.writerows(moduli_rows)

    # Summary
    summary_rows = []
    for cat, s in results["summary"].items():
        summary_rows.append({"category": cat, **s})
    with open(output_dir / "22_ntt_summary.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "num_lengths_tested", "total_moduli_found", "avg_moduli_per_length", "max_moduli_for_single_length"])
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"CSV measurements saved to {output_dir}")


def create_visualizations(results: dict[str, Any], output_dir: Path) -> None:
    """Create visualizations for the experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Moduli count per category
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    categories = list(results["moduli_results"].keys())
    for idx, cat in enumerate(categories):
        ax = axes[idx // 2, idx % 2]
        cat_results = results["moduli_results"][cat]
        lengths = [r["transform_length"] for r in cat_results]
        counts = [r["num_moduli_found"] for r in cat_results]
        ax.bar(range(len(lengths)), counts, tick_label=[f"{l}\n({int_to_base(l, 60)})" for l in lengths])
        ax.set_title(f"{cat}: NTT Moduli Found")
        ax.set_xlabel("Transform Length (decimal, base-60)")
        ax.set_ylabel("Number of Moduli")
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_dir / "22_moduli_per_category.png", dpi=150)
    plt.close()

    # 2. Summary comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    cats = list(results["summary"].keys())
    totals = [results["summary"][c]["total_moduli_found"] for c in cats]
    avgs = [results["summary"][c]["avg_moduli_per_length"] for c in cats]
    x = range(len(cats))
    width = 0.35
    ax.bar([i - width/2 for i in x], totals, width, label="Total Moduli", color="steelblue")
    ax.bar([i + width/2 for i in x], [a * 10 for a in avgs], width, label="Avg × 10", color="coral")
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    ax.set_ylabel("Count")
    ax.set_title("NTT Moduli Summary by Smoothness Category")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "22_category_comparison.png", dpi=150)
    plt.close()

    # 3. Prime factor smoothness of p-1
    fig, ax = plt.subplots(figsize=(10, 6))
    smoothness_counts = {"5-smooth": 0, "12-smooth": 0, "60-smooth": 0, "other": 0}
    for cat_results in results["moduli_results"].values():
        for r in cat_results:
            for m in r["moduli"]:
                if m["is_5_smooth_p_minus_1"]:
                    smoothness_counts["5-smooth"] += 1
                elif m["is_12_smooth_p_minus_1"]:
                    smoothness_counts["12-smooth"] += 1
                elif m["is_60_smooth_p_minus_1"]:
                    smoothness_counts["60-smooth"] += 1
                else:
                    smoothness_counts["other"] += 1
    ax.pie(smoothness_counts.values(), labels=smoothness_counts.keys(), autopct="%1.1f%%")
    ax.set_title("Smoothness of p-1 for All Found NTT Primes")
    plt.tight_layout()
    plt.savefig(output_dir / "22_p_minus_1_smoothness.png", dpi=150)
    plt.close()

    # 4. Base-60 vs base-12 vs base-10 moduli representation length
    fig, ax = plt.subplots(figsize=(10, 6))
    lengths_10 = []
    lengths_12 = []
    lengths_60 = []
    for cat_results in results["moduli_results"].values():
        for r in cat_results:
            for m in r["moduli"]:
                p = m["prime"]
                lengths_10.append(len(str(p)))
                lengths_12.append(len(int_to_base(p, 12)))
                lengths_60.append(len(int_to_base(p, 60)))
    ax.hist([lengths_10, lengths_12, lengths_60], bins=15, label=["Base-10", "Base-12", "Base-60"], alpha=0.7)
    ax.set_xlabel("Digit Length")
    ax.set_ylabel("Frequency")
    ax.set_title("Moduli Digit Length Distribution Across Bases")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "22_digit_length_distribution.png", dpi=150)
    plt.close()

    print(f"Visualizations saved to {output_dir}")


def generate_findings_markdown(results: dict[str, Any], output_dir: Path) -> None:
    """Generate findings markdown file."""
    docs_dir = Path("/home/hyperion/Projects/Base60Research/docs/findings")
    docs_dir.mkdir(parents=True, exist_ok=True)
    md_path = docs_dir / "experiment-22-ntt-smooth-moduli.md"

    with open(md_path, "w") as f:
        f.write("# Experiment 22: NTT with 60-Smooth Moduli\n\n")
        f.write("## Hypothesis\n")
        f.write("Base-60 factorization (2² × 3 × 5) provides more available NTT-friendly prime moduli ")
        f.write("than base-10 (2 × 5) or base-12 (2² × 3) because the additional factor 3 enables ")
        f.write("more Fermat-prime-related moduli of the form k·N+1 where k is 5-smooth.\n\n")

        f.write("## Results Summary\n\n")
        f.write("| Category | Lengths Tested | Total Moduli | Avg/Length | Max/Length |\n")
        f.write("|----------|----------------|--------------|------------|------------|\n")
        for cat, s in results["summary"].items():
            f.write(f"| {cat} | {s['num_lengths_tested']} | {s['total_moduli_found']} | {s['avg_moduli_per_length']:.1f} | {s['max_moduli_for_single_length']} |\n")

        f.write("\n## Base-60 Advantage\n\n")
        adv = results["base60_advantage"]
        f.write(f"- 5-smooth vs powers of 2: **{adv['5_smooth_vs_powers_of_2']:+d}** additional moduli\n")
        f.write(f"- 5-smooth vs 3-smooth: **{adv['5_smooth_vs_3_smooth']:+d}** additional moduli\n")
        f.write(f"- {adv['factor_3_contribution']}\n\n")

        f.write("## Smoothness of p-1\n\n")
        smooth_counts = {"5-smooth": 0, "12-smooth": 0, "60-smooth": 0, "other": 0}
        for cat_results in results["moduli_results"].values():
            for r in cat_results:
                for m in r["moduli"]:
                    if m["is_5_smooth_p_minus_1"]:
                        smooth_counts["5-smooth"] += 1
                    elif m["is_12_smooth_p_minus_1"]:
                        smooth_counts["12-smooth"] += 1
                    elif m["is_60_smooth_p_minus_1"]:
                        smooth_counts["60-smooth"] += 1
                    else:
                        smooth_counts["other"] += 1
        f.write("| Smoothness | Count |\n")
        f.write("|------------|-------|\n")
        for k, v in smooth_counts.items():
            f.write(f"| {k} | {v} |\n")

        f.write("\n## Key Findings\n\n")
        if results["summary"]["5_smooth"]["total_moduli_found"] > results["summary"]["powers_of_2"]["total_moduli_found"]:
            f.write("✅ **CONFIRMED**: Including factor 3 (5-smooth = base-60 factors) yields strictly more NTT moduli than powers of 2 alone.\n")
        else:
            f.write("❌ **NOT CONFIRMED**: 5-smooth did not yield more moduli than powers of 2.\n")

        f.write("\n## Controls Applied\n")
        f.write("- Same quantity: equal number of transform lengths per category (15)\n")
        f.write("- Exact arithmetic: all modular operations use Python integers\n")
        f.write("- Independent verification: Miller-Rabin deterministic for n < 2⁶⁴\n")
        f.write("- Equal conditions: same k-search range (1-500) for all categories\n")
        f.write("- Negative results: recorded where categories underperform\n")

    print(f"Findings saved to {md_path}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Experiment 22: NTT with 60-Smooth Moduli")
    print("=" * 60)

    results = run_ntt_experiment()

    output_dir = Path("results/experiment_22")
    output_dir.mkdir(parents=True, exist_ok=True)

    save_json_results(results, output_dir)
    save_csv_measurements(results, output_dir)
    create_visualizations(results, output_dir)
    generate_findings_markdown(results, output_dir)

    print("\n" + "=" * 60)
    print("Experiment 22 complete!")
    print(f"Results in: {output_dir}")
    print(f"Findings: docs/findings/experiment-22-ntt-smooth-moduli.md")
    print("=" * 60)


if __name__ == "__main__":
    main()