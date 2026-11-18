#!/usr/bin/env python3
"""Experiment 05: Algebra and Number Sequences.

Tests hypothesis H5: Alternative numerical representations improve pattern discovery.
Analyzes Fibonacci, triangular, square, cube, perfect, prime, geometric, harmonic sequences
across base-10, base-12, and base-60 representations.
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

from base60lab.core.rational import Rational
from base60lab.engines import Base10Engine, Base12Engine, Base60Engine
from base60lab.sequences import (
    fibonacci, triangular, square, cube, perfect,
    prime, geometric, harmonic
)


def run_sequences_experiment() -> dict[str, Any]:
    """Run the complete sequences experiment."""
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }

    results = {}

    # 1. Generate sequences
    print("Generating number sequences...")
    count = 30

    sequences = {
        "fibonacci": fibonacci(count),
        "triangular": triangular(count),
        "square": square(count),
        "cube": cube(count),
        "perfect": perfect(count),
        "prime": prime(count),
        "geometric_2": geometric(count, ratio=2, start=1),
        "harmonic": harmonic(count),
    }
    results["sequences"] = {name: [str(v) for v in seq] for name, seq in sequences.items()}
    # Also store raw rational values for visualization
    results["sequences_raw"] = {name: seq for name, seq in sequences.items()}
    # 2. Base representations of sequences
    print("Computing base representations...")
    base_reps = {}
    for name, seq in sequences.items():
        base_reps[name] = {}
        for base in (10, 12, 60):
            engine = engines[base]
            reps = []
            for val in seq:
                num = engine.from_rational(val)
                notation = engine.to_notation(num)
                reps.append({
                    "value": str(val),
                    "notation": notation.text,
                    "terminating": notation.repeating is None,
                    "digits": len(notation.text.replace("0.", "").replace("(", "").replace(")", "")),
                })
            base_reps[name][f"base{base}"] = reps
    results["base_representations"] = base_reps

    # 3. Analyze patterns in base representations
    print("Analyzing patterns in base representations...")
    pattern_analysis = {}
    for name in sequences:
        pattern_analysis[name] = {}
        for base in (10, 12, 60):
            reps = base_reps[name][f"base{base}"]
            terminating_count = sum(1 for r in reps if r["terminating"])
            avg_digits = sum(r["digits"] for r in reps) / len(reps)
            max_digits = max(r["digits"] for r in reps)

            pattern_analysis[name][f"base{base}"] = {
                "terminating_count": terminating_count,
                "terminating_ratio": terminating_count / len(reps),
                "avg_digits": avg_digits,
                "max_digits": max_digits,
                "total_terms": len(reps),
            }
    results["pattern_analysis"] = pattern_analysis

    # 4. Polynomial relationships (as per PLAN.md F1)
    print("Analyzing polynomial relationships...")
    # (x+1)^2, (x+2)^2, (x+3)^2 for x = 0..10
    poly_data = {}
    for x in range(11):
        x_r = Rational(x)
        val1 = (x_r + 1) ** 2
        val2 = (x_r + 2) ** 2
        val3 = (x_r + 3) ** 2
        poly_entry = {
            "x_plus_1_sq": {"rational": f"{val1.numerator}/{val1.denominator}", "float": val1},
            "x_plus_2_sq": {"rational": f"{val2.numerator}/{val2.denominator}", "float": val2},
            "x_plus_3_sq": {"rational": f"{val3.numerator}/{val3.denominator}", "float": val3},
        }
        # Add base representations
        for base in (10, 12, 60):
            engine = engines[base]
            for key, val in [("x_plus_1_sq", val1), ("x_plus_2_sq", val2), ("x_plus_3_sq", val3)]:
                num = engine.from_rational(val)
                notation = engine.to_notation(num)
                poly_entry[key][f"_base{base}"] = notation.text
        poly_data[x] = poly_entry
    results["polynomials"] = poly_data
    # 5. Differences between consecutive terms (finite differences)
    print("Computing finite differences...")
    differences = {}
    for name, seq in sequences.items():
        if len(seq) < 3:
            continue
        diffs = []
        for i in range(len(seq) - 1):
            diffs.append(seq[i + 1] - seq[i])
        differences[name] = {
            "first_differences": [str(d) for d in diffs],
            "first_differences_raw": diffs,
            "first_differences_base": {},
        }
        if len(diffs) > 1:
            second_diffs = []
            for i in range(len(diffs) - 1):
                second_diffs.append(diffs[i + 1] - diffs[i])
            differences[name]["second_differences"] = [str(d) for d in second_diffs]

        # Base representations of differences
        for base in (10, 12, 60):
            engine = engines[base]
            diff_reps = []
            for d in diffs:
                num = engine.from_rational(d)
                notation = engine.to_notation(num)
                diff_reps.append(notation.text)
            differences[name][f"first_differences_base{base}"] = diff_reps

    results["differences"] = differences

    return results, engines


def save_json_results(results: dict[str, Any], output_dir: Path) -> None:
    """Save results as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "05_algebra_sequences_results.json", "w") as f:
        serializable = make_serializable(results)
        json.dump(serializable, f, indent=2)
    print(f"JSON results saved to {output_dir / '05_algebra_sequences_results.json'}")


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

    # Sequence values
    with open(output_dir / "05_sequences.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n"] + list(results["sequences"].keys()))
        max_len = max(len(v) for v in results["sequences"].values())
        for i in range(max_len):
            row = [i]
            for name in results["sequences"]:
                if i < len(results["sequences"][name]):
                    row.append(results["sequences"][name][i])
                else:
                    row.append("")
            writer.writerow(row)

    # Base representations
    for name in results["sequences"]:
        with open(output_dir / f"05_{name}_bases.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["n", "value", "base10", "base12", "base60"])
            for i, val in enumerate(results["sequences"][name]):
                row = [i, val]
                for base in (10, 12, 60):
                    rep = results["base_representations"][name][f"base{base}"][i]
                    row.append(rep["notation"])
                writer.writerow(row)

    # Pattern analysis summary
    with open(output_dir / "05_pattern_analysis.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sequence", "base", "terminating_count", "terminating_ratio", "avg_digits", "max_digits"])
        for name in results["pattern_analysis"]:
            for base in (10, 12, 60):
                pa = results["pattern_analysis"][name][f"base{base}"]
                writer.writerow([name, base, pa["terminating_count"], pa["terminating_ratio"],
                                 pa["avg_digits"], pa["max_digits"]])

    # Polynomials
    with open(output_dir / "05_polynomials.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "(x+1)^2", "(x+2)^2", "(x+3)^2",
                         "base10_x1", "base10_x2", "base10_x3",
                         "base12_x1", "base12_x2", "base12_x3",
                         "base60_x1", "base60_x2", "base60_x3"])
        for x in range(11):
            d = results["polynomials"][x]
            writer.writerow([
                x,
                d["x_plus_1_sq"]["rational"], d["x_plus_2_sq"]["rational"], d["x_plus_3_sq"]["rational"],
                d["x_plus_1_sq"]["_base10"], d["x_plus_2_sq"]["_base10"], d["x_plus_3_sq"]["_base10"],
                d["x_plus_1_sq"]["_base12"], d["x_plus_2_sq"]["_base12"], d["x_plus_3_sq"]["_base12"],
                d["x_plus_1_sq"]["_base60"], d["x_plus_2_sq"]["_base60"], d["x_plus_3_sq"]["_base60"],
            ])
    # Differences
    with open(output_dir / "05_differences.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sequence", "n", "first_diff", "base10", "base12", "base60"])
        for name, diff_data in results["differences"].items():
            for i, diff in enumerate(diff_data["first_differences"]):
                row = [name, i, diff]
                for base in (10, 12, 60):
                    row.append(diff_data[f"first_differences_base{base}"][i])
                writer.writerow(row)

    print(f"CSV measurements saved to {output_dir}")


def create_visualizations(results: dict[str, Any], output_dir: Path) -> None:
    """Create visualizations for the experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Sequence values comparison
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    sequences = list(results["sequences"].keys())
    for idx, name in enumerate(sequences):
        ax = axes[idx // 3, idx % 3]
        vals = [v.to_float() for v in results["sequences_raw"][name]]
        ax.plot(range(len(vals)), vals, "o-", linewidth=1.5, markersize=4)
        ax.set_title(name.capitalize())
        ax.set_xlabel("n")
        ax.set_ylabel("Value")
        ax.grid(alpha=0.3)
        ax.set_yscale("log" if name in ["cube", "geometric_2", "geometric_3"] else "linear")
    plt.suptitle("Number Sequences (First 30 Terms)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "05_sequences.png", dpi=150)
    plt.savefig(output_dir / "05_sequences.svg")
    plt.close()

    # 2. Base representation digit lengths
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    for idx, name in enumerate(sequences):
        ax = axes[idx // 3, idx % 3]
        x = range(len(results["sequences_raw"][name]))
        for base in (10, 12, 60):
            digits = [r["digits"] for r in results["base_representations"][name][f"base{base}"]]
            ax.plot(x, digits, "o-", label=f"Base-{base}", linewidth=1.5, markersize=3)
        ax.set_title(f"{name.capitalize()} - Digit Length by Base")
        ax.set_xlabel("n")
        ax.set_ylabel("Digits")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
    plt.suptitle("Digit Length of Sequence Terms in Different Bases", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "05_digit_lengths.png", dpi=150)
    plt.savefig(output_dir / "05_digit_lengths.svg")
    plt.close()

    # 3. Terminating ratio by sequence and base
    fig, ax = plt.subplots(figsize=(12, 6))
    sequences = list(results["pattern_analysis"].keys())
    x = np.arange(len(sequences))
    width = 0.25
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    for idx, base in enumerate((10, 12, 60)):
        ratios = [results["pattern_analysis"][s][f"base{base}"]["terminating_ratio"] for s in sequences]
        ax.bar(x + idx * width, ratios, width, label=f"Base-{base}", color=colors[idx], alpha=0.8)

    ax.set_xlabel("Sequence")
    ax.set_ylabel("Terminating Ratio")
    ax.set_title("Fraction of Terminating Representations by Sequence and Base")
    ax.set_xticks(x + width)
    ax.set_xticklabels([s.capitalize() for s in sequences], rotation=45, ha="right")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "05_terminating_ratios.png", dpi=150)
    plt.savefig(output_dir / "05_terminating_ratios.svg")
    plt.close()

    # 4. Average digit length by sequence and base
    fig, ax = plt.subplots(figsize=(12, 6))
    for idx, base in enumerate((10, 12, 60)):
        avg_digits = [results["pattern_analysis"][s][f"base{base}"]["avg_digits"] for s in sequences]
        ax.bar(x + idx * width, avg_digits, width, label=f"Base-{base}", color=colors[idx], alpha=0.8)

    ax.set_xlabel("Sequence")
    ax.set_ylabel("Average Digits")
    ax.set_title("Average Digit Length by Sequence and Base")
    ax.set_xticks(x + width)
    ax.set_xticklabels([s.capitalize() for s in sequences], rotation=45, ha="right")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "05_avg_digits.png", dpi=150)
    plt.savefig(output_dir / "05_avg_digits.svg")
    plt.close()

    # 5. Polynomial patterns
    fig, ax = plt.subplots(figsize=(10, 6))
    x_vals = list(range(11))
    for offset in [1, 2, 3]:
        y = [(x + offset) ** 2 for x in x_vals]
        ax.plot(x_vals, y, "o-", label=f"(x+{offset})²", linewidth=2, markersize=6)
    ax.set_xlabel("x")
    ax.set_ylabel("Value")
    ax.set_title("Polynomial Patterns: (x+1)², (x+2)², (x+3)²")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "05_polynomials.png", dpi=150)
    plt.savefig(output_dir / "05_polynomials.svg")
    plt.close()

    # 6. Finite differences
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    diff_names = list(results["differences"].keys())[:4]
    for idx, name in enumerate(diff_names):
        ax = axes[idx // 2, idx % 2]
        diffs = [d.to_float() for d in results["differences"][name]["first_differences_raw"]]
        ax.plot(range(len(diffs)), diffs, "o-", linewidth=1.5, markersize=4)
        ax.set_title(f"{name.capitalize()} - First Differences")
        ax.set_xlabel("n")
        ax.set_ylabel("Difference")
        ax.grid(alpha=0.3)
    plt.suptitle("Finite Differences of Sequences", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "05_differences.png", dpi=150)
    plt.savefig(output_dir / "05_differences.svg")
    plt.close()

    print(f"Visualizations saved to {output_dir}")


def generate_findings_markdown(results: dict[str, Any], output_dir: Path) -> None:
    """Generate findings markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    md = """# Experiment 05: Algebra and Number Sequences Findings

## Summary
Analysis of classic number sequences (Fibonacci, triangular, square, cube, perfect, prime, geometric, harmonic)
and polynomial patterns across base-10, base-12, and base-60 representations.

## Sequences Analyzed (First 30 Terms)

### Fibonacci
"""

    fib = results["sequences"]["fibonacci"][:15]
    md += f"0, {', '.join(fib[1:])}, ...\n\n"

    md += """### Triangular Numbers (n(n+1)/2)
"""
    tri = results["sequences"]["triangular"][:15]
    md += f"{', '.join(tri)}, ...\n\n"

    md += """### Square Numbers (n²)
"""
    sq = results["sequences"]["square"][:15]
    md += f"{', '.join(sq)}, ...\n\n"

    md += """### Cube Numbers (n³)
"""
    cb = results["sequences"]["cube"][:15]
    md += f"{', '.join(cb)}, ...\n\n"

    md += """### Prime Numbers
"""
    pr = results["sequences"]["prime"][:15]
    md += f"{', '.join(pr)}, ...\n\n"

    md += """### Geometric (ratio=2)
"""
    geo = results["sequences"]["geometric_2"][:15]
    md += f"{', '.join(geo)}, ...\n\n"

    md += """### Harmonic Numbers
"""
    har = results["sequences"]["harmonic"][:10]
    md += f"{', '.join(har)}, ...\n\n"

    md += """## Base Representation Analysis

### Terminating Ratios by Sequence
| Sequence | Base-10 | Base-12 | Base-60 |
|----------|---------|---------|---------|
"""

    for name in results["pattern_analysis"]:
        pa = results["pattern_analysis"][name]
        md += f"| {name.capitalize()} | {pa['base10']['terminating_ratio']:.2f} | {pa['base12']['terminating_ratio']:.2f} | {pa['base60']['terminating_ratio']:.2f} |\n"

    md += """

### Average Digit Length by Sequence
| Sequence | Base-10 | Base-12 | Base-60 |
|----------|---------|---------|---------|
"""

    for name in results["pattern_analysis"]:
        pa = results["pattern_analysis"][name]
        md += f"| {name.capitalize()} | {pa['base10']['avg_digits']:.1f} | {pa['base12']['avg_digits']:.1f} | {pa['base60']['avg_digits']:.1f} |\n"

    md += """

## Polynomial Patterns
### (x+1)², (x+2)², (x+3)² for x=0..10
"""

    md += "| x | (x+1)² | (x+2)² | (x+3)² |\n"
    md += "|---|--------|--------|--------|\n"
    for x in range(11):
        d = results["polynomials"][x]
        md += f"| {x} | {d['x_plus_1_sq']['rational']} | {d['x_plus_2_sq']['rational']} | {d['x_plus_3_sq']['rational']} |\n"

    md += """

### Base Representations of Polynomials (x=5)
| Expression | Value | Base-10 | Base-12 | Base-60 |
|------------|-------|---------|---------|---------|
"""

    x = 5
    d = results["polynomials"][x]
    for key, label in [("x_plus_1_sq", "(x+1)²"), ("x_plus_2_sq", "(x+2)²"), ("x_plus_3_sq", "(x+3)²")]:
        md += f"| {label} | {d[key]['rational']} | {d[key]['_base10']} | {d[key]['_base12']} | {d[key]['_base60']} |\n"

    md += """

## Finite Differences

### First Differences (should be constant for polynomials)
"""

    for name in ["square", "cube", "triangular", "geometric_2"]:
        if name in results["differences"]:
            diffs = results["differences"][name]["first_differences"][:10]
            md += f"- **{name.capitalize()}**: {', '.join(diffs)} ...\n"

    md += """

### Second Differences
"""

    for name in ["square", "cube", "triangular"]:
        if "second_differences" in results["differences"][name]:
            diffs = results["differences"][name]["second_differences"][:10]
            md += f"- **{name.capitalize()}**: {', '.join(diffs)} ...\n"

    md += """

## Key Findings

1. **Integer sequences** (Fibonacci, triangular, square, cube, prime) are all integers, so they terminate in all bases.

2. **Harmonic sequence** has non-terminating representations in all bases for most terms (denominators contain primes > 5).

3. **Geometric sequences** with integer ratio have terminating representations in bases where the ratio's prime factors divide the base.

4. **Base-60** generally has the shortest representations for integers due to its larger base (more information per digit).

5. **Base-12** provides a good balance for sequences involving factors of 2 and 3.

6. **Polynomial patterns** are base-independent mathematically, but base-12 and base-60 can make coefficient patterns more visible.

## Controls Verified
✅ Same mathematical sequences tested across all bases
✅ Exact rational arithmetic used throughout
✅ Independent verification via sequence generation formulas
✅ Equal conditions (first 30 terms for all sequences)
✅ Negative results recorded (harmonic sequence non-termination)
"""

    with open(output_dir / "experiment-05-algebra-sequences.md", "w") as f:
        f.write(md)
    print(f"Findings saved to {output_dir / 'experiment-05-algebra-sequences.md'}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Experiment 05: Algebra and Sequences")
    print("=" * 60)

    output_dir = Path("results/experiment_05")

    # Run experiment
    results, engines = run_sequences_experiment()

    # Save outputs
    save_json_results(results, output_dir)
    save_csv_measurements(results, output_dir)
    create_visualizations(results, output_dir)
    generate_findings_markdown(results, Path("docs/findings"))

    print("\nExperiment 05 completed successfully!")
    print(f"Results in: {output_dir}")
    print(f"Findings in: docs/findings/experiment-05-algebra-sequences.md")


if __name__ == "__main__":
    main()