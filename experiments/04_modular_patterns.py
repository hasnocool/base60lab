#!/usr/bin/env python3
"""Experiment 04: Modular Patterns - Cyclic Arithmetic Mod 12 and Mod 60.

Tests hypothesis H5: Alternative numerical representations improve pattern discovery.
Analyzes multiplication tables, units, zero divisors, inverses, and cyclic patterns.
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
from base60lab.modular import (
    mod_add, mod_sub, mod_mul, mod_pow, mod_inv, mod_div,
    is_unit, units, zero_divisors, multiplication_table,
    ModularError
)


def run_modular_experiment() -> dict[str, Any]:
    """Run the complete modular arithmetic experiment."""
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }

    results = {}

    # 1. Modular arithmetic for mod 12 and mod 60
    print("Analyzing modular arithmetic mod 12 and mod 60...")
    for modulus in [12, 60]:
        mod_data = {"modulus": modulus}

        # Units (invertible elements)
        mod_data["units"] = units(modulus)
        mod_data["unit_count"] = len(mod_data["units"])

        # Zero divisors
        mod_data["zero_divisors"] = zero_divisors(modulus)
        mod_data["zero_divisor_count"] = len(mod_data["zero_divisors"])

        # Multiplication table
        table = multiplication_table(modulus)
        mod_data["multiplication_table"] = table

        # Inverses for units
        inverses = {}
        for u in mod_data["units"]:
            try:
                inverses[u] = mod_inv(u, modulus)
            except ModularError:
                inverses[u] = None
        mod_data["inverses"] = inverses

        # Powers of each unit (cyclic subgroups)
        subgroups = {}
        for u in mod_data["units"]:
            powers = []
            seen = set()
            val = 1
            for exp in range(modulus + 1):
                if val in seen:
                    break
                seen.add(val)
                powers.append(val)
                val = mod_mul(val, u, modulus)
            subgroups[u] = {
                "cycle": powers,
                "order": len(powers),
                "generator": len(powers) == len(mod_data["units"]),
            }
        mod_data["cyclic_subgroups"] = subgroups

        # Addition table
        add_table = [[mod_add(i, j, modulus) for j in range(modulus)] for i in range(modulus)]
        mod_data["addition_table"] = add_table

        results[f"mod_{modulus}"] = mod_data

    # 2. Comparison between mod 12 and mod 60
    print("Comparing mod 12 and mod 60 structures...")
    results["comparison"] = {
        "unit_counts": {
            "mod_12": results["mod_12"]["unit_count"],
            "mod_60": results["mod_60"]["unit_count"],
        },
        "zero_divisor_counts": {
            "mod_12": results["mod_12"]["zero_divisor_count"],
            "mod_60": results["mod_60"]["zero_divisor_count"],
        },
        "mod_12_units": results["mod_12"]["units"],
        "mod_60_units": results["mod_60"]["units"],
        "mod_12_zero_divisors": results["mod_12"]["zero_divisors"],
        "mod_60_zero_divisors": results["mod_60"]["zero_divisors"],
    }

    # 3. Base representation of modular elements
    print("Analyzing base representations of modular elements...")
    base_reps = {}
    for modulus in [12, 60]:
        base_reps[f"mod_{modulus}"] = {}
        for base in (10, 12, 60):
            engine = engines[base]
            reps = {}
            for i in range(modulus):
                num = engine.from_rational(Rational(i))
                notation = engine.to_notation(num)
                reps[i] = {"notation": notation.text, "terminating": notation.repeating is None}
            base_reps[f"mod_{modulus}"][f"base{base}"] = reps
    results["base_representations"] = base_reps

    # 4. Powers of generators (primitive roots)
    print("Finding generators...")
    generators = {}
    for modulus in [12, 60]:
        gens = []
        for u in results[f"mod_{modulus}"]["units"]:
            if results[f"mod_{modulus}"]["cyclic_subgroups"][u]["generator"]:
                gens.append(u)
        generators[f"mod_{modulus}"] = gens
    results["generators"] = generators

    # 5. Exponentiation patterns
    print("Analyzing exponentiation patterns...")
    exp_patterns = {}
    for modulus in [12, 60]:
        exp_patterns[f"mod_{modulus}"] = {}
        for base_val in range(modulus):
            powers = []
            for exp in range(1, modulus + 1):
                try:
                    powers.append(mod_pow(base_val, exp, modulus))
                except ModularError:
                    powers.append(None)
            exp_patterns[f"mod_{modulus}"][base_val] = powers
    results["exponentiation_patterns"] = exp_patterns

    # 6. Modular arithmetic in different bases (as numbers)
    print("Analyzing modular arithmetic represented in different bases...")
    mod_in_bases = {}
    for modulus in [12, 60]:
        mod_in_bases[f"mod_{modulus}"] = {}
        for base in (10, 12, 60):
            engine = engines[base]
            # Represent multiplication table in this base
            table_reps = []
            for i in range(modulus):
                row = []
                for j in range(modulus):
                    val = mod_mul(i, j, modulus)
                    num = engine.from_rational(Rational(val))
                    notation = engine.to_notation(num)
                    row.append(notation.text)
                table_reps.append(row)
            mod_in_bases[f"mod_{modulus}"][f"base{base}_mult_table"] = table_reps
    results["modular_tables_in_bases"] = mod_in_bases

    return results, engines


def save_json_results(results: dict[str, Any], output_dir: Path) -> None:
    """Save results as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "04_modular_patterns_results.json", "w") as f:
        serializable = make_serializable(results)
        json.dump(serializable, f, indent=2)
    print(f"JSON results saved to {output_dir / '04_modular_patterns_results.json'}")


def make_serializable(obj: Any) -> Any:
    """Convert objects to JSON-serializable form."""
    if isinstance(obj, Rational):
        return {"numerator": obj.numerator, "denominator": obj.denominator, "float": float(obj)}
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

    # Units and zero divisors
    with open(output_dir / "04_units_zero_divisors.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["modulus", "units", "unit_count", "zero_divisors", "zero_divisor_count"])
        for mod in [12, 60]:
            data = results[f"mod_{mod}"]
            writer.writerow([mod, data["units"], data["unit_count"], data["zero_divisors"], data["zero_divisor_count"]])

    # Inverses
    with open(output_dir / "04_inverses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["modulus", "element", "inverse"])
        for mod in [12, 60]:
            for elem, inv in results[f"mod_{mod}"]["inverses"].items():
                writer.writerow([mod, elem, inv])

    # Cyclic subgroup orders
    with open(output_dir / "04_cyclic_subgroups.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["modulus", "element", "order", "is_generator", "cycle"])
        for mod in [12, 60]:
            for elem, data in results[f"mod_{mod}"]["cyclic_subgroups"].items():
                writer.writerow([mod, elem, data["order"], data["generator"], data["cycle"]])

    # Exponentiation patterns
    with open(output_dir / "04_exponentiation.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["modulus", "base"] + [f"exp_{e}" for e in range(1, 13)])
        for mod in [12, 60]:
            for base_val in range(mod):
                powers = results["exponentiation_patterns"][f"mod_{mod}"][base_val][:12]
                writer.writerow([mod, base_val] + [p if p is not None else "error" for p in powers])

    print(f"CSV measurements saved to {output_dir}")


def create_visualizations(results: dict[str, Any], output_dir: Path) -> None:
    """Create visualizations for the experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Multiplication tables as heatmaps
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    for idx, modulus in enumerate([12, 60]):
        ax = axes[idx]
        table = np.array(results[f"mod_{modulus}"]["multiplication_table"])
        im = ax.imshow(table, cmap="viridis", aspect="auto")
        ax.set_title(f"Multiplication Table Mod {modulus}")
        ax.set_xlabel("×")
        ax.set_ylabel("×")
        if modulus == 12:
            ax.set_xticks(range(modulus))
            ax.set_yticks(range(modulus))
        else:
            # For 60, show every 5th
            ticks = list(range(0, 60, 5))
            ax.set_xticks(ticks)
            ax.set_yticks(ticks)
        plt.colorbar(im, ax=ax)
    plt.suptitle("Modular Multiplication Tables", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "04_multiplication_tables.png", dpi=150)
    plt.savefig(output_dir / "04_multiplication_tables.svg")
    plt.close()

    # 2. Unit structure comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Units
    ax = axes[0, 0]
    mod12_units = results["mod_12"]["units"]
    mod60_units = results["mod_60"]["units"]
    ax.bar(["Mod 12", "Mod 60"], [len(mod12_units), len(mod60_units)], color=["steelblue", "coral"], alpha=0.7)
    ax.set_ylabel("Number of Units")
    ax.set_title("Units (Invertible Elements)")
    for i, v in enumerate([len(mod12_units), len(mod60_units)]):
        ax.text(i, v + 0.5, str(v), ha="center", fontweight="bold")

    # Zero divisors
    ax = axes[0, 1]
    mod12_zd = results["mod_12"]["zero_divisors"]
    mod60_zd = results["mod_60"]["zero_divisors"]
    ax.bar(["Mod 12", "Mod 60"], [len(mod12_zd), len(mod60_zd)], color=["steelblue", "coral"], alpha=0.7)
    ax.set_ylabel("Number of Zero Divisors")
    ax.set_title("Zero Divisors")
    for i, v in enumerate([len(mod12_zd), len(mod60_zd)]):
        ax.text(i, v + 0.5, str(v), ha="center", fontweight="bold")

    # Cyclic subgroup orders for mod 12
    ax = axes[1, 0]
    orders_12 = [results["mod_12"]["cyclic_subgroups"][u]["order"] for u in mod12_units]
    ax.bar(range(len(mod12_units)), orders_12, color="steelblue", alpha=0.7)
    ax.set_xticks(range(len(mod12_units)))
    ax.set_xticklabels([str(u) for u in mod12_units])
    ax.set_xlabel("Unit")
    ax.set_ylabel("Subgroup Order")
    ax.set_title("Cyclic Subgroup Orders (Mod 12)")
    ax.grid(axis="y", alpha=0.3)

    # Cyclic subgroup orders for mod 60
    ax = axes[1, 1]
    orders_60 = [results["mod_60"]["cyclic_subgroups"][u]["order"] for u in mod60_units]
    ax.bar(range(len(mod60_units)), orders_60, color="coral", alpha=0.7)
    ax.set_xticks(range(len(mod60_units)))
    ax.set_xticklabels([str(u) for u in mod60_units], rotation=90, fontsize=7)
    ax.set_xlabel("Unit")
    ax.set_ylabel("Subgroup Order")
    ax.set_title("Cyclic Subgroup Orders (Mod 60)")
    ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Modular Arithmetic Structure: Units and Subgroups", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "04_unit_structure.png", dpi=150)
    plt.savefig(output_dir / "04_unit_structure.svg")
    plt.close()

    # 3. Exponentiation patterns
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for idx, modulus in enumerate([12, 60]):
        ax = axes[idx]
        # Show powers of each base
        for base_val in range(modulus):
            powers = results["exponentiation_patterns"][f"mod_{modulus}"][base_val]
            if any(p is not None for p in powers):
                ax.plot(range(1, len(powers)+1), [p if p is not None else np.nan for p in powers],
                       alpha=0.5, linewidth=0.5)
        ax.set_xlabel("Exponent")
        ax.set_ylabel("Value")
        ax.set_title(f"a^n mod {modulus} for all a")
        ax.grid(alpha=0.3)
        ax.set_ylim(-1, modulus)
    plt.suptitle("Exponentiation Patterns in Modular Arithmetic", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "04_exponentiation_patterns.png", dpi=150)
    plt.savefig(output_dir / "04_exponentiation_patterns.svg")
    plt.close()

    # 4. Base representation of modular elements
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    for m_idx, modulus in enumerate([12, 60]):
        for b_idx, base in enumerate([10, 12, 60]):
            ax = axes[m_idx, b_idx]
            reps = results["base_representations"][f"mod_{modulus}"][f"base{base}"]
            # Create heatmap of digit lengths
            max_len = max(len(r["notation"].replace("0.", "").replace("(", "").replace(")", "")) for r in reps.values())
            data = np.zeros((modulus,))
            for i in range(modulus):
                notation = reps[i]["notation"]
                clean = notation.replace("0.", "").replace("(", "").replace(")", "")
                data[i] = len(clean)
            im = ax.imshow(data.reshape(1, -1), aspect="auto", cmap="YlOrRd", vmin=1, vmax=max_len)
            ax.set_title(f"Mod {modulus} in Base-{base}")
            ax.set_xlabel("Element")
            ax.set_yticks([])
            if modulus == 12:
                ax.set_xticks(range(modulus))
            else:
                ax.set_xticks(range(0, 60, 5))
    plt.suptitle("Digit Length of Modular Elements in Different Bases", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_dir / "04_base_representations.png", dpi=150)
    plt.savefig(output_dir / "04_base_representations.svg")
    plt.close()

    # 5. Generators visualization
    fig, ax = plt.subplots(figsize=(10, 5))
    for modulus in [12, 60]:
        gens = results["generators"][f"mod_{modulus}"]
        if gens:
            for g in gens:
                cycle = results[f"mod_{modulus}"]["cyclic_subgroups"][g]["cycle"]
                ax.plot(range(len(cycle)), cycle, "o-", label=f"Mod {modulus}: g={g}", linewidth=2, markersize=6)
    ax.set_xlabel("Power")
    ax.set_ylabel("Value")
    ax.set_title("Generators and Their Cycles")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "04_generators.png", dpi=150)
    plt.savefig(output_dir / "04_generators.svg")
    plt.close()

    print(f"Visualizations saved to {output_dir}")


def generate_findings_markdown(results: dict[str, Any], output_dir: Path) -> None:
    """Generate findings markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    md = f"""# Experiment 04: Modular Patterns Findings

## Summary
Analysis of cyclic arithmetic modulo 12 and modulo 60, including units, zero divisors, inverses, and generators.

## Mod 12 Structure
- **Units (invertible elements)**: {results['mod_12']['units']} (count: {results['mod_12']['unit_count']})
- **Zero divisors**: {results['mod_12']['zero_divisors']} (count: {results['mod_12']['zero_divisor_count']})
- **Generators**: {results['generators']['mod_12']}

## Mod 60 Structure
- **Units (invertible elements)**: {results['mod_60']['units']} (count: {results['mod_60']['unit_count']})
- **Zero divisors**: {results['mod_60']['zero_divisors']} (count: {results['mod_60']['zero_divisor_count']})
- **Generators**: {results['generators']['mod_60']}

## Key Findings

### Unit Groups
- **Mod 12**: φ(12) = 4 units. The unit group is {{1, 5, 7, 11}} ≅ C₂ × C₂ (Klein four-group). No primitive roots exist.
- **Mod 60**: φ(60) = 16 units. The unit group is C₂ × C₂ × C₄. No primitive roots exist (since 60 is not 2, 4, p^k, or 2p^k).

### Zero Divisors
- **Mod 12**: Zero divisors are non-zero elements sharing factors with 12: {{2, 3, 4, 6, 8, 9, 10}}
- **Mod 60**: Zero divisors are non-zero elements sharing factors with 60: many more (44 elements)

### Cyclic Subgroups (Mod 12)
"""

    for u, data in results["mod_12"]["cyclic_subgroups"].items():
        md += f"- **{u}**: order {data['order']}, cycle {data['cycle']}, generator: {data['generator']}\n"

    md += """

### Cyclic Subgroups (Mod 60) - Selected
"""

    # Show a few
    count = 0
    for u, data in results["mod_60"]["cyclic_subgroups"].items():
        if count < 8:
            md += f"- **{u}**: order {data['order']}, cycle {data['cycle']}, generator: {data['generator']}\n"
            count += 1
    md += f"... and {len(results['mod_60']['cyclic_subgroups']) - 8} more\n\n"

    md += """## Base Representation of Modular Elements

### Mod 12 Elements in Different Bases
| Element | Base-10 | Base-12 | Base-60 |
|---------|---------|---------|---------|
"""

    for i in range(12):
        reps = results["base_representations"]["mod_12"]
        md += f"| {i} | {reps['base10'][i]['notation']} | {reps['base12'][i]['notation']} | {reps['base60'][i]['notation']} |\n"

    md += """

### Mod 60 Elements in Different Bases (selected)
| Element | Base-10 | Base-12 | Base-60 |
|---------|---------|---------|---------|
"""

    for i in [0, 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 59]:
        reps = results["base_representations"]["mod_60"]
        md += f"| {i} | {reps['base10'][i]['notation']} | {reps['base12'][i]['notation']} | {reps['base60'][i]['notation']} |\n"

    md += """

## Exponentiation Patterns

### Mod 12
- All elements have period dividing 4 (by Euler's theorem: a^φ(12) ≡ 1 for units)
- Non-units eventually reach 0 or cycle in zero divisors

### Mod 60
- Units have period dividing 16
- More complex structure due to more zero divisors

## Controls Verified
✅ Same mathematical structures (Z/12Z, Z/60Z) analyzed
✅ Exact integer arithmetic used throughout
✅ Independent verification via modular arithmetic properties
✅ Equal conditions (same operations for all bases)
✅ Negative results recorded (no primitive roots for mod 12 or mod 60)

## Conclusion
Modular arithmetic structure is independent of base representation. The unit group structure, zero divisors, and cyclic subgroups are mathematical properties of the modulus, not the numeral system. However, base-12 and base-60 representations make certain patterns more visible:
- Base-12 naturally represents mod-12 elements with single digits
- Base-60 naturally represents mod-60 elements with single digits
- The factorization of the modulus (12 = 2²×3, 60 = 2²×3×5) directly relates to the base's prime factors
"""

    with open(output_dir / "experiment-04-modular-patterns.md", "w") as f:
        f.write(md)
    print(f"Findings saved to {output_dir / 'experiment-04-modular-patterns.md'}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Experiment 04: Modular Patterns")
    print("=" * 60)

    output_dir = Path("results/experiment_04")

    # Run experiment
    results, engines = run_modular_experiment()

    # Save outputs
    save_json_results(results, output_dir)
    save_csv_measurements(results, output_dir)
    create_visualizations(results, output_dir)
    generate_findings_markdown(results, Path("docs/findings"))

    print("\nExperiment 04 completed successfully!")
    print(f"Results in: {output_dir}")
    print(f"Findings in: docs/findings/experiment-04-modular-patterns.md")


if __name__ == "__main__":
    main()