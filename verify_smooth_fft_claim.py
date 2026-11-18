#!/usr/bin/env python3
"""
Verify Schumacher 2016 claim: 5-smooth (base-60) FFT sizes provide
performance benefits over arbitrary sizes.

This is a minimal, self-contained test that:
1. Generates 5-smooth numbers near a target (default: 100000)
2. Generates nearby arbitrary (poorly-factored) sizes for comparison
3. Benchmarks scipy.fft on both sets
4. Reports CONFIRMED / REFUTED / PARTIAL
"""

import sys
import time
import math
import random
from typing import List, Tuple

import numpy as np
from scipy import fft


# ============================================================
# 5-smooth number generation (from smooth_fft_sizes.py)
# ============================================================

LOG2 = math.log(2)
LOG3 = math.log(3)
LOG5 = math.log(5)


def generate_5smooth(limit: int) -> List[int]:
    """Generate all 5-smooth numbers <= limit (sorted)."""
    result = []
    max_p = int(math.log(limit) / LOG2) + 1
    max_q = int(math.log(limit) / LOG3) + 1
    max_r = int(math.log(limit) / LOG5) + 1

    for p in range(max_p + 1):
        pow2 = 2 ** p
        if pow2 > limit:
            break
        for q in range(max_q + 1):
            pow23 = pow2 * (3 ** q)
            if pow23 > limit:
                break
            for r in range(max_r + 1):
                val = pow23 * (5 ** r)
                if val > limit:
                    break
                result.append(val)
    return sorted(result)


def find_optimal_5smooth_near(target: int, search_radius: int = None) -> List[Tuple[int, float]]:
    """Find 5-smooth FFT sizes near target with relative distance."""
    if search_radius is None:
        search_radius = max(1000, target // 100)

    lower = max(1, target - search_radius)
    upper = target + search_radius

    smooth_numbers = generate_5smooth(upper)
    candidates = [n for n in smooth_numbers if lower <= n <= upper]

    results = []
    for n in candidates:
        rel_dist = abs(n - target) / target
        results.append((n, rel_dist))

    return sorted(results, key=lambda x: x[1])


def largest_prime_factor(n: int) -> int:
    """Return the largest prime factor of n."""
    if n <= 1:
        return 1
    largest = 1
    d = 2
    while d * d <= n:
        while n % d == 0:
            largest = d
            n //= d
        d += 1 if d == 2 else 2  # After 2, try only odd numbers
    if n > 1:
        largest = max(largest, n)
    return largest


def is_poorly_factored(n: int, min_large_prime_factor: int = 13) -> bool:
    """Check if n has a large prime factor (poorly factored for FFT)."""
    return largest_prime_factor(n) >= min_large_prime_factor


def generate_arbitrary_near(target: int, count: int, search_radius: int = None) -> List[int]:
    """Generate poorly-factored (arbitrary) sizes near target."""
    if search_radius is None:
        search_radius = max(1000, target // 100)

    lower = max(1, target - search_radius)
    upper = target + search_radius

    candidates = [n for n in range(lower, upper + 1) if is_poorly_factored(n)]
    random.shuffle(candidates)
    return candidates[:count]


# ============================================================
# FFT Benchmark
# ============================================================

def benchmark_fft(size: int, iterations: int = 10, warmup: int = 3) -> float:
    """
    Benchmark FFT for a single size.
    Returns median execution time in nanoseconds.
    """
    # Generate deterministic test signal
    rng = np.random.default_rng(42)
    signal = rng.standard_normal(size) + 1j * rng.standard_normal(size)
    signal = signal.astype(np.complex128)

    # Warmup
    for _ in range(warmup):
        _ = fft.fft(signal)

    # Timed runs
    times = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        _ = fft.fft(signal)
        end = time.perf_counter_ns()
        times.append(end - start)

    return float(np.median(times))


def run_verification(
    target: int = 100000,
    num_5smooth: int = 10,
    num_arbitrary: int = 10,
    iterations: int = 10,
    warmup: int = 3,
    search_radius: int = None,
) -> dict:
    """Run the complete verification experiment."""

    print(f"=" * 70)
    print(f"Schumacher 2016 Claim Verification: 5-smooth FFT Performance")
    print(f"=" * 70)
    print(f"Target size: {target}")
    print(f"Num 5-smooth sizes: {num_5smooth}")
    print(f"Num arbitrary sizes: {num_arbitrary}")
    print(f"Iterations per size: {iterations}")
    print(f"Warmup runs: {warmup}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"NumPy: {np.__version__}")
    print(f"SciPy: {fft.__version__ if hasattr(fft, '__version__') else 'unknown'}")
    print(f"=" * 70)

    # Generate 5-smooth sizes near target
    smooth_candidates = find_optimal_5smooth_near(target, search_radius)
    smooth_sizes = [n for n, _ in smooth_candidates[:num_5smooth]]
    print(f"\n5-smooth sizes selected: {smooth_sizes}")

    # Generate arbitrary sizes near target
    arbitrary_sizes = generate_arbitrary_near(target, num_arbitrary, search_radius)
    print(f"Arbitrary (poorly-factored) sizes selected: {arbitrary_sizes}")

    # Benchmark 5-smooth sizes
    print(f"\n--- Benchmarking 5-smooth sizes ---")
    smooth_results = []
    for size in smooth_sizes:
        t = benchmark_fft(size, iterations, warmup)
        smooth_results.append((size, t))
        print(f"  Size {size:8d}: {t:>12.0f} ns ({t/1e6:.3f} ms)")

    # Benchmark arbitrary sizes
    print(f"\n--- Benchmarking arbitrary sizes ---")
    arbitrary_results = []
    for size in arbitrary_sizes:
        t = benchmark_fft(size, iterations, warmup)
        arbitrary_results.append((size, t))
        print(f"  Size {size:8d}: {t:>12.0f} ns ({t/1e6:.3f} ms)")

    # Statistics
    smooth_times = [t for _, t in smooth_results]
    arbitrary_times = [t for _, t in arbitrary_results]

    smooth_median = np.median(smooth_times)
    arbitrary_median = np.median(arbitrary_times)
    smooth_mean = np.mean(smooth_times)
    arbitrary_mean = np.mean(arbitrary_times)

    print(f"\n--- Summary Statistics ---")
    print(f"5-smooth median:  {smooth_median:>12.0f} ns ({smooth_median/1e6:.3f} ms)")
    print(f"Arbitrary median: {arbitrary_median:>12.0f} ns ({arbitrary_median/1e6:.3f} ms)")
    print(f"5-smooth mean:    {smooth_mean:>12.0f} ns ({smooth_mean/1e6:.3f} ms)")
    print(f"Arbitrary mean:   {arbitrary_mean:>12.0f} ns ({arbitrary_mean/1e6:.3f} ms)")

    # Compare
    median_ratio = arbitrary_median / smooth_median
    mean_ratio = arbitrary_mean / smooth_mean

    print(f"\nMedian ratio (arbitrary/smooth): {median_ratio:.3f}x")
    print(f"Mean ratio (arbitrary/smooth):   {mean_ratio:.3f}x")

    # Determine verdict
    if median_ratio > 1.05:  # 5-smooth at least 5% faster
        verdict = "CONFIRMED"
        detail = f"5-smooth sizes are {median_ratio:.2f}x faster (median)"
    elif median_ratio < 0.95:  # arbitrary at least 5% faster
        verdict = "REFUTED"
        detail = f"Arbitrary sizes are {1/median_ratio:.2f}x faster (median)"
    else:
        verdict = "PARTIAL"
        detail = f"No clear winner (ratio = {median_ratio:.2f}x)"

    print(f"\n{'=' * 70}")
    print(f"VERDICT: {verdict}")
    print(f"Detail: {detail}")
    print(f"{'=' * 70}")

    return {
        "verdict": verdict,
        "detail": detail,
        "target": target,
        "smooth_sizes": smooth_sizes,
        "arbitrary_sizes": arbitrary_sizes,
        "smooth_results": smooth_results,
        "arbitrary_results": arbitrary_results,
        "smooth_median_ns": smooth_median,
        "arbitrary_median_ns": arbitrary_median,
        "smooth_mean_ns": smooth_mean,
        "arbitrary_mean_ns": arbitrary_mean,
        "median_ratio": median_ratio,
        "mean_ratio": mean_ratio,
    }


if __name__ == "__main__":
    # Run with defaults
    result = run_verification(
        target=100000,
        num_5smooth=10,
        num_arbitrary=10,
        iterations=10,
        warmup=3,
    )

    # Exit code based on verdict
    if result["verdict"] == "CONFIRMED":
        sys.exit(0)
    elif result["verdict"] == "REFUTED":
        sys.exit(1)
    else:
        sys.exit(2)