"""Lissajous figures — exact phase closure analysis using rational arithmetic.

2D Lissajous figures: x(t) = sin(fx*t), y(t) = sin(fy*t + phase)
3D Lissajous figures: x(t) = sin(fx*t), y(t) = sin(fy*t + phase_xy), z(t) = sin(fz*t + phase_xz)

All internal arithmetic uses exact rational numbers. Floating-point only for plotting.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from .core.rational import Rational


@dataclass(frozen=True)
class LissajousParameters:
    """Parameters defining a 2D Lissajous figure."""
    freq_x: Rational  # frequency in x direction (a)
    freq_y: Rational  # frequency in y direction (b)
    phase: Rational   # phase difference δ (in radians as rational multiple of π)
    amplitude_x: Rational = Rational(1)  # A
    amplitude_y: Rational = Rational(1)  # B

    def frequency_ratio(self) -> Rational:
        """Return the exact frequency ratio a/b."""
        return self.freq_x / self.freq_y

    def reduced_ratio(self) -> tuple[int, int]:
        """Return the frequency ratio as reduced (numerator, denominator)."""
        ratio = self.frequency_ratio()
        return ratio.numerator, ratio.denominator


@dataclass(frozen=True)
class ClosureInfo:
    """Information about geometric closure of a 2D Lissajous figure."""
    is_closed: bool
    closure_period: int | None  # number of periods of the slower oscillation to close
    numerator: int
    denominator: int
    factorization: dict[int, int]  # prime factorization of denominator
    prime_class: str  # "2_3_5_smooth" or "prime_7_11_13" or "mixed"

    def __str__(self) -> str:
        if self.is_closed:
            return (f"Closed: period={self.closure_period}, "
                    f"ratio={self.numerator}/{self.denominator}, "
                    f"factors={self.factorization}, class={self.prime_class}")
        return "Not closed (irrational frequency ratio)"


# =====================================================================
# 3D Lissajous Figures (Trajectories on 3-Torus)
# =====================================================================

@dataclass(frozen=True)
class Lissajous3DParameters:
    """Parameters defining a 3D Lissajous figure (trajectory on 3-torus)."""
    freq_x: Rational  # frequency in x direction
    freq_y: Rational  # frequency in y direction
    freq_z: Rational  # frequency in z direction
    phase_xy: Rational = Rational(0)  # phase difference between x and y
    phase_xz: Rational = Rational(0)  # phase difference between x and z
    amplitude_x: Rational = Rational(1)  # A_x
    amplitude_y: Rational = Rational(1)  # A_y
    amplitude_z: Rational = Rational(1)  # A_z

    def frequency_ratios(self) -> tuple[Rational, Rational]:
        """Return the exact frequency ratios (fx/fy, fx/fz)."""
        return self.freq_x / self.freq_y, self.freq_x / self.freq_z

    def all_ratios_rational(self) -> bool:
        """Check if all pairwise frequency ratios are rational."""
        # With exact rational arithmetic, all ratios are rational by construction
        return True


@dataclass(frozen=True)
class ClosureInfo3D:
    """Information about geometric closure of a 3D Lissajous figure on 3-torus."""
    is_closed: bool
    closure_period: int | None  # number of fundamental periods to close
    ratios: tuple[Rational, Rational]  # (fx/fy, fx/fz)
    denominators: tuple[int, int]  # (denom of fx/fy, denom of fx/fz)
    lcm_denominator: int  # LCM of the two denominators
    factorization: dict[int, int]  # prime factorization of LCM denominator
    prime_class: str  # "2_3_5_smooth", "prime_7_11_13", or "mixed"
    diophantine_quality: float | None  # measure of how well frequencies can be approximated by rationals

    def __str__(self) -> str:
        if self.is_closed:
            return (f"Closed on 3-torus: period={self.closure_period}, "
                    f"ratios={self.ratios[0]}/{self.ratios[1]}, "
                    f"LCM denom={self.lcm_denominator}, "
                    f"factors={self.factorization}, class={self.prime_class}")
        return "Not closed (at least one irrational frequency ratio)"


def prime_factors(n: int) -> dict[int, int]:
    """Return the prime factorization of n as a dict {prime: exponent}."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2  # skip even numbers after 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def classify_denominator(denominator: int) -> str:
    """Classify denominator by its prime factors.
    
    Returns:
        "2_3_5_smooth" if only prime factors are 2, 3, 5
        "prime_7_11_13" if only prime factors are 7, 11, 13
        "mixed" otherwise
    """
    factors = prime_factors(denominator)
    if not factors:
        return "2_3_5_smooth"  # 1 has no prime factors
    
    primes = set(factors.keys())
    if primes.issubset({2, 3, 5}):
        return "2_3_5_smooth"
    if primes.issubset({7, 11, 13}):
        return "prime_7_11_13"
    return "mixed"


# --- 2D functions ---

def is_closed(freq_x: int | Rational, freq_y: int | Rational) -> bool:
    """Determine if a 2D Lissajous figure with given frequencies is geometrically closed.
    
    A figure is closed iff the frequency ratio is rational.
    Since we use exact rational arithmetic, any rational ratio yields a closed figure.
    
    Args:
        freq_x: frequency in x direction
        freq_y: frequency in y direction
        
    Returns:
        True if the figure is closed, False otherwise.
    """
    if isinstance(freq_x, int):
        freq_x = Rational(freq_x)
    if isinstance(freq_y, int):
        freq_y = Rational(freq_y)

    if freq_y == 0:
        raise ValueError("Frequency in y direction cannot be zero")

    # Any rational ratio gives a closed Lissajous figure
    ratio = freq_x / freq_y
    return ratio.denominator != 0


def closure_info(freq_x: int | Rational, freq_y: int | Rational) -> ClosureInfo:
    """Compute detailed closure information for a 2D Lissajous figure.
    
    Args:
        freq_x: frequency in x direction
        freq_y: frequency in y direction
        
    Returns:
        ClosureInfo with closure status, period, and prime classification.
    """
    if isinstance(freq_x, int):
        freq_x = Rational(freq_x)
    if isinstance(freq_y, int):
        freq_y = Rational(freq_y)

    if freq_y == 0:
        raise ValueError("Frequency in y direction cannot be zero")

    ratio = freq_x / freq_y
    num, den = ratio.numerator, ratio.denominator

    # The closure period is the denominator of the reduced ratio
    # (number of y-periods to complete one full cycle)
    closure_period = den

    factors = prime_factors(den)
    prime_class = classify_denominator(den)

    return ClosureInfo(
        is_closed=True,
        closure_period=closure_period,
        numerator=num,
        denominator=den,
        factorization=factors,
        prime_class=prime_class,
    )


def generate_lissajous_points(params: LissajousParameters, num_points: int = 1000) -> tuple[np.ndarray, np.ndarray]:
    """Generate x, y coordinates for a 2D Lissajous figure.
    
    Args:
        params: LissajousParameters defining the figure
        num_points: number of points to generate
        
    Returns:
        Tuple of (x_array, y_array) as numpy arrays.
    """
    t = np.linspace(0, 2 * np.pi * params.freq_y.to_float(), num_points)
    x = params.amplitude_x.to_float() * np.sin(params.freq_x.to_float() * t + params.phase.to_float() * np.pi)
    y = params.amplitude_y.to_float() * np.sin(params.freq_y.to_float() * t)
    return x, y


def plot_lissajous(
    params: LissajousParameters,
    output_path: str | None = None,
    title: str | None = None,
    num_points: int = 1000,
) -> plt.Figure:
    """Plot a 2D Lissajous figure and optionally save to file.
    
    Args:
        params: LissajousParameters defining the figure
        output_path: optional path to save the figure
        title: optional title
        num_points: number of points to generate
        
    Returns:
        matplotlib Figure object.
    """
    x, y = generate_lissajous_points(params, num_points)
    info = closure_info(params.freq_x, params.freq_y)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x, y, 'b-', alpha=0.7, linewidth=1)
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True, alpha=0.3)
    
    if title:
        ax.set_title(title)
    else:
        ax.set_title(
            f"Lissajous: fx={params.freq_x}, fy={params.freq_y}, "
            f"phase={params.phase}, Closed: {info.is_closed}, "
            f"Period={info.closure_period}"
        )
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {output_path}")
    
    return fig


def compare_frequency_ratios(
    freq_pairs: list[tuple[int | Rational, int | Rational]]
) -> list[ClosureInfo]:
    """Compare closure properties for multiple frequency ratios.
    
    Args:
        freq_pairs: list of (freq_x, freq_y) tuples
        
    Returns:
        List of ClosureInfo objects.
    """
    results = []
    for fx, fy in freq_pairs:
        results.append(closure_info(fx, fy))
    return results


def analyze_prime_factor_effects(
    max_denominator: int = 60,
) -> dict[str, list[ClosureInfo]]:
    """Analyze how different prime factors affect closure periods.
    
    Args:
        max_denominator: maximum denominator to test
        
    Returns:
        Dictionary mapping prime class to list of ClosureInfo.
    """
    from collections import defaultdict
    classes = defaultdict(list)
    
    for den in range(1, max_denominator + 1):
        for num in range(1, den + 1):
            if math.gcd(num, den) == 1:  # reduced fractions only
                info = closure_info(num, den)
                classes[info.prime_class].append(info)
    
    return dict(classes)


def save_closure_analysis(
    output_dir: str = ".",
    max_denominator: int = 60,
) -> None:
    """Generate and save closure analysis plots and summary.
    
    Args:
        max_denominator: maximum denominator to analyze
        output_dir: directory to save outputs
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    results = analyze_prime_factor_effects(max_denominator)
    
    # Save summary CSV
    summary_path = os.path.join(output_dir, "lissajous_closure_summary.csv")
    with open(summary_path, 'w') as f:
        f.write("ratio,numerator,denominator,closed,period,prime_class,factorization\n")
        for class_name, infos in results.items():
            for info in infos:
                factors_str = ';'.join(f"{p}^{e}" for p, e in info.factorization.items())
                f.write(f"{info.numerator}:{info.denominator},{info.numerator},{info.denominator},"
                       f"{info.is_closed},{info.closure_period},{info.prime_class},{factors_str}\n")
    
    # Plot: closure period vs denominator by class
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, (class_name, infos) in enumerate(results.items()):
        ax = axes[idx]
        denoms = [info.denominator for info in infos]
        periods = [info.closure_period for info in infos]
        ax.scatter(denoms, periods, alpha=0.6, s=20)
        ax.set_xlabel('Denominator')
        ax.set_ylabel('Closure Period')
        ax.set_title(f'{class_name} ({len(infos)} ratios)')
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        ax.set_yscale('log')
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "lissajous_closure_by_class.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Analysis saved to {summary_path}")
    # Save summary markdown
    md_path = os.path.join(output_dir, "lissajous-phase-closure.md")
    with open(md_path, 'w') as f:
        f.write("# Lissajous Phase Closure Analysis\n\n")
        f.write(f"Max denominator analyzed: {max_denominator}\n\n")
        for class_name, infos in results.items():
            f.write(f"## {class_name} ({len(infos)} ratios)\n\n")
            for info in infos[:5]:
                f.write(f"- {info.numerator}:{info.denominator} → period {info.closure_period}, factors: {info.factorization}\n")
            if len(infos) > 5:
                f.write(f"- ... and {len(infos) - 5} more\n")
            f.write("\n")

    # Save SVG plots (re-render for SVG format)
    for class_name, infos in results.items():
        fig, ax = plt.subplots(figsize=(8, 5))
        denoms = [info.denominator for info in infos]
        periods = [info.closure_period for info in infos]
        ax.scatter(denoms, periods, alpha=0.6, s=20)
        ax.set_xlabel('Denominator')
        ax.set_ylabel('Closure Period')
        ax.set_title(f'{class_name.replace("_", " ").title()} ({len(infos)} ratios)')
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        ax.set_yscale('log')
        svg_path = os.path.join(output_dir, f"lissajous_{class_name}.svg")
        fig.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close(fig)



# --- 3D functions ---

def is_closed_3d(freq_x: int | Rational, freq_y: int | Rational, freq_z: int | Rational) -> bool:
    """Determine if a 3D Lissajous figure is geometrically closed on the 3-torus.
    
    A 3D Lissajous figure closes iff all pairwise frequency ratios are rational.
    With exact rational arithmetic, this is always true for Rational inputs.
    
    Args:
        freq_x: frequency in x direction
        freq_y: frequency in y direction
        freq_z: frequency in z direction
        
    Returns:
        True if the figure is closed, False otherwise.
    """
    if isinstance(freq_x, int):
        freq_x = Rational(freq_x)
    if isinstance(freq_y, int):
        freq_y = Rational(freq_y)
    if isinstance(freq_z, int):
        freq_z = Rational(freq_z)

    if freq_y == 0 or freq_z == 0:
        raise ValueError("Frequencies in y and z directions cannot be zero")

    # All pairwise ratios must be rational
    ratio_xy = freq_x / freq_y
    ratio_xz = freq_x / freq_z
    return ratio_xy.denominator != 0 and ratio_xz.denominator != 0


def closure_info_3d(
    freq_x: int | Rational, 
    freq_y: int | Rational, 
    freq_z: int | Rational
) -> ClosureInfo3D:
    """Compute detailed closure information for a 3D Lissajous figure.
    
    The trajectory closes when all three coordinates simultaneously return
    to their starting values. The period is the LCM of the pairwise denominators.
    
    Args:
        freq_x: frequency in x direction
        freq_y: frequency in y direction
        freq_z: frequency in z direction
        
    Returns:
        ClosureInfo3D with closure status, period, and prime classification.
    """
    if isinstance(freq_x, int):
        freq_x = Rational(freq_x)
    if isinstance(freq_y, int):
        freq_y = Rational(freq_y)
    if isinstance(freq_z, int):
        freq_z = Rational(freq_z)

    if freq_y == 0 or freq_z == 0:
        raise ValueError("Frequencies in y and z directions cannot be zero")

    ratio_xy = freq_x / freq_y
    ratio_xz = freq_x / freq_z
    
    den_xy = ratio_xy.denominator
    den_xz = ratio_xz.denominator
    
    # The closure period is the LCM of the two denominators
    lcm_den = math.lcm(den_xy, den_xz)
    closure_period = lcm_den
    
    factors = prime_factors(lcm_den)
    prime_class = classify_denominator(lcm_den)
    
    return ClosureInfo3D(
        is_closed=True,
        closure_period=closure_period,
        ratios=(ratio_xy, ratio_xz),
        denominators=(den_xy, den_xz),
        lcm_denominator=lcm_den,
        factorization=factors,
        prime_class=prime_class,
        diophantine_quality=None,
    )


def diophantine_approximation_quality(
    freq_x: int | Rational, 
    freq_y: int | Rational, 
    freq_z: int | Rational,
    max_denominator: int = 1000
) -> float:
    """Compute a measure of how well the frequency ratios can be approximated by rationals.
    
    This implements a KAM-style Diophantine condition check.
    For a 3D torus, we measure the minimum distance from the frequency vector
    to rational vectors with denominator <= max_denominator.
    
    Args:
        freq_x, freq_y, freq_z: frequencies
        max_denominator: maximum denominator for rational approximations
        
    Returns:
        A quality measure: smaller = better approximable by rationals = more "resonant"
    """
    if isinstance(freq_x, int):
        freq_x = Rational(freq_x)
    if isinstance(freq_y, int):
        freq_y = Rational(freq_y)
    if isinstance(freq_z, int):
        freq_z = Rational(freq_z)
    
    # Normalize frequencies (divide by gcd or by one of them)
    # Use fx as reference
    if freq_x == 0:
        return float('inf')
    
    # Compute the frequency vector on the torus
    # We want to find the best rational approximation to (fy/fx, fz/fx)
    ratio_y = freq_y / freq_x
    ratio_z = freq_z / freq_x
    
    # For each denominator q up to max_denominator, find closest rational
    min_distance = float('inf')
    for q in range(1, max_denominator + 1):
        # Best p for ratio_y
        p_y = round(ratio_y.to_float() * q)
        # Best p for ratio_z
        p_z = round(ratio_z.to_float() * q)
        
        # Distance on 2-torus
        err_y = abs(ratio_y.to_float() - p_y / q)
        err_z = abs(ratio_z.to_float() - p_z / q)
        distance = math.sqrt(err_y**2 + err_z**2)
        
        if distance < min_distance:
            min_distance = distance
    
    return min_distance


def generate_lissajous_3d_points(
    params: Lissajous3DParameters, 
    num_points: int = 2000
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate x, y, z coordinates for a 3D Lissajous figure.
    
    Args:
        params: Lissajous3DParameters defining the figure
        num_points: number of points to generate
        
    Returns:
        Tuple of (x_array, y_array, z_array) as numpy arrays.
    """
    # Time spans LCM period of all frequencies
    # Use freq_y as reference for the time range
    t = np.linspace(0, 2 * np.pi * params.freq_y.to_float(), num_points)
    
    x = params.amplitude_x.to_float() * np.sin(
        params.freq_x.to_float() * t
    )
    y = params.amplitude_y.to_float() * np.sin(
        params.freq_y.to_float() * t + params.phase_xy.to_float() * np.pi
    )
    z = params.amplitude_z.to_float() * np.sin(
        params.freq_z.to_float() * t + params.phase_xz.to_float() * np.pi
    )
    return x, y, z


def plot_lissajous_3d(
    params: Lissajous3DParameters,
    output_path: str | None = None,
    title: str | None = None,
    num_points: int = 2000,
    show_projections: bool = True,
) -> Any:
    """Plot a 3D Lissajous figure with 2D projections.
    
    Args:
        params: Lissajous3DParameters defining the figure
        output_path: optional path to save the figure
        title: optional title
        num_points: number of points to generate
        show_projections: whether to show XY, XZ, YZ projections
        
    Returns:
        matplotlib Figure object.
    """
    x, y, z = generate_lissajous_3d_points(params, num_points)
    info = closure_info_3d(params.freq_x, params.freq_y, params.freq_z)
    
    if show_projections:
        fig = plt.figure(figsize=(14, 10))
        
        # 3D plot
        ax1 = fig.add_subplot(221, projection='3d')
        ax1.plot(x, y, z, 'b-', alpha=0.7, linewidth=0.8)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('3D Lissajous Trajectory')
        
        # XY projection
        ax2 = fig.add_subplot(222)
        ax2.plot(x, y, 'r-', alpha=0.7, linewidth=0.8)
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_title('XY Projection')
        ax2.set_aspect('equal')
        ax2.grid(True, alpha=0.3)
        
        # XZ projection
        ax3 = fig.add_subplot(223)
        ax3.plot(x, z, 'g-', alpha=0.7, linewidth=0.8)
        ax3.set_xlabel('X')
        ax3.set_ylabel('Z')
        ax3.set_title('XZ Projection')
        ax3.set_aspect('equal')
        ax3.grid(True, alpha=0.3)
        
        # YZ projection
        ax4 = fig.add_subplot(224)
        ax4.plot(y, z, 'm-', alpha=0.7, linewidth=0.8)
        ax4.set_xlabel('Y')
        ax4.set_ylabel('Z')
        ax4.set_title('YZ Projection')
        ax4.set_aspect('equal')
        ax4.grid(True, alpha=0.3)
        
        if title:
            fig.suptitle(title, fontsize=14)
        else:
            fig.suptitle(
                f'3D Lissajous: fx={params.freq_x}, fy={params.freq_y}, fz={params.freq_z}\n'
                f'Phase: xy={params.phase_xy}, xz={params.phase_xz}\n'
                f'Closure: {info}',
                fontsize=12
            )
    else:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z, 'b-', alpha=0.7, linewidth=0.8)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title or f'3D Lissajous: {params.freq_x}:{params.freq_y}:{params.freq_z}')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"3D Lissajous plot saved to {output_path}")
    
    return fig


def analyze_kam_diophantine_conditions(
    freq_triplets: list[tuple[int, int, int]],
    max_denominator: int = 1000
) -> list[dict[str, Any]]:
    """Analyze KAM Diophantine conditions for a set of frequency triplets.
    
    For a 3D torus with frequencies (fx, fy, fz), the KAM theorem says
    quasi-periodic orbits persist if the frequency vector satisfies a
    Diophantine condition: |k·ω| >= γ/|k|^τ for all integer vectors k.
    
    We measure how well the ratios can be approximated by rationals
    as a proxy for the Diophantine constant.
    
    Args:
        freq_triplets: list of (fx, fy, fz) tuples
        max_denominator: maximum denominator for rational approximations
        
    Returns:
        List of analysis results with Diophantine quality metrics.
    """
    results = []
    for fx, fy, fz in freq_triplets:
        fx_r, fy_r, fz_r = Rational(fx), Rational(fy), Rational(fz)
        info = closure_info_3d(fx_r, fy_r, fz_r)
        quality = diophantine_approximation_quality(fx_r, fy_r, fz_r, max_denominator)
        
        # Compute resonance web: which small integer relations exactly hold
        resonances = []
        for q in range(1, 20):
            for p_y in range(-q, q+1):
                for p_z in range(-q, q+1):
                    if p_y == 0 and p_z == 0:
                        continue
                    # Check if p_y*fy + p_z*fz = k*fx for some k
                    for k in range(-q, q+1):
                        lhs = Rational(p_y) * fy_r + Rational(p_z) * fz_r
                        rhs = Rational(k) * fx_r
                        if lhs == rhs:
                            resonances.append({
                                "relation": f"{p_y}*fy + {p_z}*fz = {k}*fx",
                                "exact": True
                            })
        results.append({
            "frequencies": (fx, fy, fz),
            "ratio_xy": str(fx_r / fy_r),
            "ratio_xz": str(fx_r / fz_r),
            "closure_info": str(info),
            "diophantine_quality": quality,
            "prime_class": info.prime_class,
            "lcm_denominator": info.lcm_denominator,
            "resonances": resonances,
        })
    return results


def compare_denominator_families(
    max_freq: int = 30
) -> dict[str, list[dict[str, Any]]]:
    """Compare closure patterns for different denominator prime factor families.
    
    Generates frequency triplets categorized by the prime factors of their
    LCM denominator.
    
    Args:
        max_freq: maximum frequency value to test
        
    Returns:
        Dictionary mapping prime class to list of results.
    """
    families = {
        "2_3_5_smooth": [],
        "prime_7_11_13": [],
        "mixed": [],
    }
    
    for fx in range(1, max_freq + 1):
        for fy in range(1, max_freq + 1):
            for fz in range(1, max_freq + 1):
                info = closure_info_3d(fx, fy, fz)
                result = {
                    "frequencies": (fx, fy, fz),
                    "ratio_xy": str(Rational(fx) / Rational(fy)),
                    "ratio_xz": str(Rational(fx) / Rational(fz)),
                    "closure_period": info.closure_period,
                    "lcm_denominator": info.lcm_denominator,
                    "factorization": info.factorization,
                    "prime_class": info.prime_class,
                }
                families[info.prime_class].append(result)
    
    return families


__all__ = [
    # 2D
    "LissajousParameters",
    "ClosureInfo",
    "prime_factors",
    "classify_denominator",
    "is_closed",
    "closure_info",
    "generate_lissajous_points",
    "plot_lissajous",
    "compare_frequency_ratios",
    "analyze_prime_factor_effects",
    "save_closure_analysis",
    # 3D
    "Lissajous3DParameters",
    "ClosureInfo3D",
    "is_closed_3d",
    "closure_info_3d",
    "diophantine_approximation_quality",
    "generate_lissajous_3d_points",
    "plot_lissajous_3d",
    "analyze_kam_diophantine_conditions",
    "compare_denominator_families",
]