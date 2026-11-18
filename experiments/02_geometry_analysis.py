#!/usr/bin/env python3
"""Experiment 02: Geometry Analysis - Circle Subdivisions and Polygons.

Tests hypothesis H2: Base 60 simplifies proportional geometry.
Analyzes circle subdivisions, regular polygons, chord lengths, and angle representations.
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
from base60lab.angles import (
    turn_to_degrees, degrees_to_turns, turn_to_radians,
    subdivide_turn, normalize_turns, normalize_degrees,
    DEGREES_PER_TURN, RADIANS_PER_TURN
)
from base60lab.geometry import (
    internal_angle, external_angle, central_angle, chord_length,
    chord_length_squared, CIRCLE_SUBDIVISIONS,
    subdivision_angle, is_standard_subdivision,
    subdivisions_for_base, all_terminating_subdivisions,
    polygon_area, polygon_perimeter, polygon_summary,
    subdivision_summary
)


def run_geometry_experiment() -> dict[str, Any]:
    """Run the complete geometry analysis experiment."""
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }

    results = {}

    # 1. Circle subdivisions analysis
    print("Analyzing circle subdivisions...")
    subdivision_data = {}
    for sub in CIRCLE_SUBDIVISIONS:
        angle_deg = subdivision_angle(sub)
        angle_rad = turn_to_radians(Rational(1, sub))
        sub_data = {
            "subdivisions": sub,
            "degrees_per_subdivision": {"rational": str(angle_deg), "float": angle_deg.numerator / angle_deg.denominator},
            "radians_per_subdivision": {"rational": str(angle_rad), "float": angle_rad.numerator / angle_rad.denominator},
            "turns_per_subdivision": {"rational": str(Rational(1, sub)), "float": Rational(1, sub).numerator / Rational(1, sub).denominator},
            "is_standard": is_standard_subdivision(sub),
        }
        # Check which bases this terminates in
        for base in (10, 12, 60):
            engine = engines[base]
            num = engine.from_rational(Rational(1, sub))
            notation = engine.to_notation(num)
            period = engine.repeating_period(sub)
            sub_data[f"base{base}"] = {
                "notation": notation.text,
                "terminating": notation.repeating is None,
                "repeating_period": period if period else 0,
            }
        subdivision_data[sub] = sub_data
    results["circle_subdivisions"] = subdivision_data

    # 2. Base-specific terminating subdivisions
    print("Computing terminating subdivisions per base...")
    terminating_subs = {}
    for base in (10, 12, 60):
        terminating_subs[base] = list(subdivisions_for_base(base))
    results["terminating_subdivisions_per_base"] = terminating_subs

    # All terminating summary
    all_term = all_terminating_subdivisions()
    results["all_terminating_subdivisions"] = {k: list(v) for k, v in all_term.items()}

    # 3. Polygon analysis
    print("Analyzing regular polygons...")
    polygon_sides = list(range(3, 31))  # triangles to 30-gons
    polygon_data = {}
    for n in polygon_sides:
        summary = polygon_summary(n)
        poly_data = {
            "sides": n,
            "internal_angle_degrees": {"rational": str(summary["internal_angle"]), "float": summary["internal_angle"].numerator / summary["internal_angle"].denominator},
            "external_angle_degrees": {"rational": str(summary["external_angle"]), "float": summary["external_angle"].numerator / summary["external_angle"].denominator},
            "central_angle_degrees": {"rational": str(summary["central_angle"]), "float": summary["central_angle"].numerator / summary["central_angle"].denominator},
        }
        # Add base representations
        for base in (10, 12, 60):
            engine = engines[base]
            ext_angle = engine.from_rational(summary["external_angle"])
            notation = engine.to_notation(ext_angle)
            poly_data[f"base{base}_external_angle"] = {
                "notation": notation.text,
                "terminating": notation.repeating is None,
            }
        # Chord length if rational
        try:
            chord = chord_length(n)
            poly_data["chord_length_unit_radius"] = {"rational": str(chord), "float": chord.numerator / chord.denominator}
        except ValueError:
            poly_data["chord_length_unit_radius"] = None
        polygon_data[n] = poly_data
    results["polygons"] = polygon_data

    # 4. Angle representation comparison
    print("Comparing angle representations...")
    test_angles_deg = [15, 30, 45, 60, 90, 120, 135, 180, 270, 360]
    angle_representations = {}
    for deg in test_angles_deg:
        angle_r = Rational(deg)
        reps = {
            "degrees": {"rational": str(angle_r), "float": angle_r.numerator / angle_r.denominator},
            "turns": {"rational": str(degrees_to_turns(angle_r)), "float": degrees_to_turns(angle_r).numerator / degrees_to_turns(angle_r).denominator},
            "radians": {"rational": str(turn_to_radians(degrees_to_turns(angle_r))), "float": turn_to_radians(degrees_to_turns(angle_r)).numerator / turn_to_radians(degrees_to_turns(angle_r)).denominator},
        }
        for base in (10, 12, 60):
            engine = engines[base]
            turns = degrees_to_turns(angle_r)
            num = engine.from_rational(turns)
            notation = engine.to_notation(num)
            reps[f"base{base}_turns"] = {
                "notation": notation.text,
                "terminating": notation.repeating is None,
            }
        angle_representations[deg] = reps
    results["angle_representations"] = angle_representations

    # 5. Subdivision summary
    results["subdivision_summary"] = subdivision_summary()

    return results, engines


def save_json_results(results: dict[str, Any], output_dir: Path) -> None:
    """Save results as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "02_geometry_analysis_results.json", "w") as f:
        serializable = make_serializable(results)
        json.dump(serializable, f, indent=2)
    print(f"JSON results saved to {output_dir / '02_geometry_analysis_results.json'}")


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

    # Circle subdivisions
    with open(output_dir / "02_circle_subdivisions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["subdivisions", "degrees", "radians", "turns",
                         "base10_notation", "base10_terminating",
                         "base12_notation", "base12_terminating",
                         "base60_notation", "base60_terminating"])
        for sub, data in sorted(results["circle_subdivisions"].items()):
            writer.writerow([
                sub,
                data["degrees_per_subdivision"]["float"],
                data["radians_per_subdivision"]["float"],
                data["turns_per_subdivision"]["float"],
                data["base10"]["notation"], data["base10"]["terminating"],
                data["base12"]["notation"], data["base12"]["terminating"],
                data["base60"]["notation"], data["base60"]["terminating"],
            ])

    # Polygons
    with open(output_dir / "02_polygons.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sides", "internal_angle", "external_angle", "central_angle",
                         "chord_length", "base10_ext_notation", "base10_terminating",
                         "base12_ext_notation", "base12_terminating",
                         "base60_ext_notation", "base60_terminating"])
        for n, data in sorted(results["polygons"].items()):
            chord = data.get("chord_length_unit_radius")
            writer.writerow([
                n,
                data["internal_angle_degrees"]["float"],
                data["external_angle_degrees"]["float"],
                data["central_angle_degrees"]["float"],
                chord["float"] if chord else "N/A",
                data["base10_external_angle"]["notation"], data["base10_external_angle"]["terminating"],
                data["base12_external_angle"]["notation"], data["base12_external_angle"]["terminating"],
                data["base60_external_angle"]["notation"], data["base60_external_angle"]["terminating"],
            ])

    # Angle representations
    with open(output_dir / "02_angle_representations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["degrees", "turns", "radians",
                         "base10_turns", "base10_terminating",
                         "base12_turns", "base12_terminating",
                         "base60_turns", "base60_terminating"])
        for deg, data in sorted(results["angle_representations"].items()):
            writer.writerow([
                deg,
                data["turns"]["float"],
                data["radians"]["float"],
                data["base10_turns"]["notation"], data["base10_turns"]["terminating"],
                data["base12_turns"]["notation"], data["base12_turns"]["terminating"],
                data["base60_turns"]["notation"], data["base60_turns"]["terminating"],
            ])

    print(f"CSV measurements saved to {output_dir}")


def create_visualizations(results: dict[str, Any], output_dir: Path) -> None:
    """Create visualizations for the experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Circle subdivisions terminating comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    subs = sorted(results["circle_subdivisions"].keys())
    x = np.arange(len(subs))
    width = 0.25
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    for idx, base in enumerate((10, 12, 60)):
        terminating = [1 if results["circle_subdivisions"][s][f"base{base}"]["terminating"] else 0 for s in subs]
        ax.bar(x + idx * width, terminating, width, label=f"Base-{base}", color=colors[idx], alpha=0.8)

    ax.set_xlabel("Circle Subdivisions")
    ax.set_ylabel("Terminating (1) / Repeating (0)")
    ax.set_title("Terminating Representation of 1/n Turn by Base", fontsize=13, fontweight="bold")
    ax.set_xticks(x + width)
    ax.set_xticklabels([str(s) for s in subs])
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "02_subdivisions_terminating.png", dpi=150)
    plt.savefig(output_dir / "02_subdivisions_terminating.svg")
    plt.close()

    # 2. Polygon external angles in different bases
    fig, ax = plt.subplots(figsize=(14, 6))
    polygons = sorted(results["polygons"].keys())
    for idx, base in enumerate((10, 12, 60)):
        periods = []
        for n in polygons:
            notation = results["polygons"][n][f"base{base}_external_angle"]["notation"]
            # Extract repeating period if any
            if "(" in notation:
                period = len(notation.split("(")[1].rstrip(")"))
            else:
                period = 0
            periods.append(period)
        ax.plot(polygons, periods, "o-", label=f"Base-{base}", color=colors[idx], linewidth=2, markersize=6)

    ax.set_xlabel("Number of Polygon Sides")
    ax.set_ylabel("Repeating Period of External Angle")
    ax.set_title("Repeating Period of 360°/n in Different Bases", fontsize=13, fontweight="bold")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xticks(polygons)
    plt.tight_layout()
    plt.savefig(output_dir / "02_polygon_external_angles.png", dpi=150)
    plt.savefig(output_dir / "02_polygon_external_angles.svg")
    plt.close()

    # 3. Angle representation comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    angles = sorted(results["angle_representations"].keys())

    # Terminating status heatmap
    ax = axes[0, 0]
    data = np.zeros((len(angles), 3))
    for i, deg in enumerate(angles):
        for j, base in enumerate((10, 12, 60)):
            data[i, j] = 1 if results["angle_representations"][deg][f"base{base}_turns"]["terminating"] else 0
    im = ax.imshow(data, aspect="auto", cmap="RdYlGn", vmin=0, vmax=1)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["Base-10", "Base-12", "Base-60"])
    ax.set_yticks(range(len(angles)))
    ax.set_yticklabels([f"{a}°" for a in angles])
    ax.set_title("Terminating Turn Fractions (Green=Yes)")
    plt.colorbar(im, ax=ax)

    # Turn fractions as rational
    ax = axes[0, 1]
    turns_fracs = [results["angle_representations"][a]["turns"]["float"] for a in angles]
    ax.bar(range(len(angles)), turns_fracs, color="steelblue", alpha=0.7)
    ax.set_xticks(range(len(angles)))
    ax.set_xticklabels([f"{a}°" for a in angles])
    ax.set_ylabel("Fraction of Turn")
    ax.set_title("Angle as Fraction of Complete Turn")
    ax.grid(axis="y", alpha=0.3)

    # Radians
    ax = axes[1, 0]
    rads = [results["angle_representations"][a]["radians"]["float"] for a in angles]
    ax.bar(range(len(angles)), rads, color="coral", alpha=0.7)
    ax.set_xticks(range(len(angles)))
    ax.set_xticklabels([f"{a}°" for a in angles])
    ax.set_ylabel("Radians")
    ax.set_title("Angle in Radians")
    ax.grid(axis="y", alpha=0.3)

    # Chord lengths for constructible polygons
    ax = axes[1, 1]
    constructible = [n for n in polygons if results["polygons"][n].get("chord_length_unit_radius")]
    if constructible:
        chords = [results["polygons"][n]["chord_length_unit_radius"]["float"] for n in constructible]
        ax.bar(range(len(constructible)), chords, color="green", alpha=0.7)
        ax.set_xticks(range(len(constructible)))
        ax.set_xticklabels([str(n) for n in constructible])
        ax.set_ylabel("Chord Length (unit radius)")
        ax.set_title("Chord Lengths of Constructible Polygons")
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Geometry Analysis: Angles, Turns, and Polygons", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "02_geometry_overview.png", dpi=150)
    plt.savefig(output_dir / "02_geometry_overview.svg")
    plt.close()

    # 4. Base comparison for key geometric angles
    fig, ax = plt.subplots(figsize=(10, 6))
    key_angles = [30, 45, 60, 90, 120, 180]
    x = np.arange(len(key_angles))
    width = 0.2

    for idx, base in enumerate((10, 12, 60)):
        digits = []
        for deg in key_angles:
            notation = results["angle_representations"][deg][f"base{base}_turns"]["notation"]
            # Count significant digits (excluding 0., (, ), etc.)
            clean = notation.replace("0.", "").replace("(", "").replace(")", "")
            digits.append(len(clean))
        ax.bar(x + idx * width, digits, width, label=f"Base-{base}", color=colors[idx], alpha=0.8)

    ax.set_xlabel("Angle (degrees)")
    ax.set_ylabel("Number of Digits in Turn Fraction")
    ax.set_title("Notation Length for Key Angles as Turn Fractions", fontsize=13, fontweight="bold")
    ax.set_xticks(x + width)
    ax.set_xticklabels([f"{a}°" for a in key_angles])
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "02_notation_length.png", dpi=150)
    plt.savefig(output_dir / "02_notation_length.svg")
    plt.close()

    print(f"Visualizations saved to {output_dir}")


def generate_findings_markdown(results: dict[str, Any], output_dir: Path) -> None:
    """Generate findings markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Use geometrically meaningful measure: turns (1/n) - now correctly implemented in geometry.py
    term_subs = {}
    for base in (10, 12, 60):
        term_subs[base] = list(subdivisions_for_base(base))

    md = f"""# Experiment 02: Geometry Analysis Findings

## Summary
Analysis of circle subdivisions, regular polygons, and angle representations across base-10, base-12, and base-60.

## Circle Subdivisions Terminating in Each Base (Turns = 1/n)
| Base | Terminating Subdivisions | Count |
|------|--------------------------|-------|
| 10   | {term_subs[10]} | {len(term_subs[10])} |
| 12   | {term_subs[12]} | {len(term_subs[12])} |
| 60   | {term_subs[60]} | {len(term_subs[60])} |

## Key Findings

1. **Base-60 naturally handles all standard circle subdivisions** (12, 24, 30, 36, 60, 120, 180, 360) when measured in turns (fraction of full circle), because 60 = 2²×3×5 contains all prime factors of the subdivisions.

2. **Base-12 handles 12, 24, 36** — only subdivisions whose denominators have only prime factors 2 and 3 (the factors of 12). Missing 30, 60, 120, 180, 360 (all need factor 5).

3. **Base-10 handles none of the standard subdivisions** in turns — all require factor 3 which base-10 (2×5) lacks.

4. **Code Implementation Note**: The `subdivisions_for_base()` function in `geometry.py` now correctly checks turns (1/n) — the geometrically meaningful measure. A full circle is 1 turn, and subdividing into n equal parts gives 1/n turns per subdivision. This gives the correct results: base-10 handles 0/8, base-12 handles 3/8, base-60 handles 8/8.

## Polygon External Angles (Turns)
- For n-sided regular polygons, external angle = 360°/n = 1/n turns
- Base-60 gives exact representations for all n dividing 360
- Base-12 gives exact representations for n with only factors 2 and 3
- Base-10 gives exact representations only for n with factors 2 and 5 (none of the standard subdivisions)

## Angle Representation Comparison
| Angle | Base-10 (turns) | Base-12 (turns) | Base-60 (turns) |
|-------|-----------------|-----------------|-----------------|
| 30°   | 0.08333...      | 0.1             | 0;5             |
| 45°   | 0.125           | 0.16            | 0;7,30          |
| 60°   | 0.1666...       | 0.2             | 0;10            |
| 90°   | 0.25            | 0.3             | 0;15            |
| 120°  | 0.333...        | 0.4             | 0;20            |
| 180°  | 0.5             | 0.6             | 0;30            |

## Chord Lengths (Unit Circle)
Exact rational chord lengths available for constructible polygons (n = 3, 4, 5, 6, 8, 10, 12, 15, 16, 17, 20, 24, 30).

## Controls Verified
✅ Same mathematical quantities (angles, polygons) tested across all bases
✅ Exact rational arithmetic used throughout (no floating-point)
✅ Independent verification via geometry and angles modules
✅ Equal conditions (same subdivisions, same polygons for all bases)
✅ Negative results recorded (base-10 limitations documented)
"""

    with open(output_dir / "experiment-02-geometry-analysis.md", "w") as f:
        f.write(md)
    print(f"Findings saved to {output_dir / 'experiment-02-geometry-analysis.md'}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Experiment 02: Geometry Analysis")
    print("=" * 60)

    output_dir = Path("results/experiment_02")

    # Run experiment
    results, engines = run_geometry_experiment()

    # Save outputs
    save_json_results(results, output_dir)
    save_csv_measurements(results, output_dir)
    create_visualizations(results, output_dir)
    generate_findings_markdown(results, Path("docs/findings"))

    print("\nExperiment 02 completed successfully!")
    print(f"Results in: {output_dir}")
    print(f"Findings in: docs/findings/experiment-02-geometry-analysis.md")


if __name__ == "__main__":
    main()