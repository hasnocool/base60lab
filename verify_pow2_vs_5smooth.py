#!/usr/bin/env python3
"""
Compare power-of-two FFT sizes vs 5-smooth (non-power-of-two) sizes.
Tests the hypothesis that power-of-two might win on some hardware
due to memory access patterns.
"""

import sys
import time
import math
import random
from typing import List, Dict

import numpy as np
from scipy import fft


# ============================================================
# Size generation
# ============================================================

LOG2 = math.log(2)
LOG3 = math.log(3)
LOG5 = math.log(5)


def generate_5smooth(limit: int) -> List[int]:
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


def find_5smooth_near(target: int, search_radius: int, max_count: int) -> List[int]:
    lower = max(1, target - search_radius)
    upper = target + search_radius
    smooth_numbers = generate_5smooth(upper)
    candidates = [n for n in smooth_numbers if lower <= n <= upper]
    candidates.sort(key=lambda x: abs(x - target))
    return candidates[:max_count]


def is_power_of_2(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def find_pow2_near(target: int, search_radius: int, max_count: int) -> List[int]:
    lower = max(1, target - search_radius)
    upper = target + search_radius
    pow2_numbers = []
    p = 0
    while True:
        val = 2 ** p
        if val > upper:
            break
        if val >= lower:
            pow2_numbers.append(val)
        p += 1
    pow2_numbers.sort(key=lambda x: abs(x - target))
    return pow2_numbers[:max_count]


def find_5smooth_non_pow2_near(target: int, search_radius: int, max_count: int) -> List[int]:
    """Find 5-smooth numbers that are NOT powers of 2."""
    lower = max(1, target - search_radius)
    upper = target + search_radius
    smooth_numbers = generate_5smooth(upper)
    candidates = [n for n in smooth_numbers if lower <= n <= upper and not is_power_of_2(n)]
    candidates.sort(key=lambda x: abs(x - target))
    return candidates[:max_count]


def largest_prime_factor(n: int) -> int:
    if n <= 1:
        return 1
    largest = 1
    d = 2
    while d * d <= n:
        while n % d == 0:
            largest = d
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        largest = max(largest, n)
    return largest


def is_poorly_factored(n: int, min_large_prime_factor: int = 13) -> bool:
    return largest_prime_factor(n) >= min_large_prime_factor


def generate_arbitrary_near(target: int, count: int, search_radius: int) -> List[int]:
    lower = max(1, target - search_radius)
    upper = target + search_radius
    candidates = [n for n in range(lower, upper + 1) if is_poorly_factored(n)]
    random.shuffle(candidates)
    return candidates[:count]


def benchmark_fft(size: int, iterations: int = 10, warmup: int = 3) -> float:
    rng = np.random.default_rng(42)
    signal = rng.standard_normal(size) + 1j * rng.standard_normal(size)
    signal = signal.astype(np.complex128)

    for _ in range(warmup):
        _ = fft.fft(signal)

    times = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        _ = fft.fft(signal)
        end = time.perf_counter_ns()
        times.append(end - start)

    return float(np.median(times))


def test_target(target: int, num_each: int = 6, iterations: int = 10, warmup: int = 3, radius_factor: float = 0.02) -> Dict:
    search_radius = max(500, int(target * radius_factor))

    pow2_sizes = find_pow2_near(target, search_radius, num_each)
    smooth_non_pow2_sizes = find_5smooth_non_pow2_near(target, search_radius, num_each)
    arbitrary_sizes = generate_arbitrary_near(target, num_each, search_radius)

    results = {
        "target": target,
        "pow2_sizes": pow2_sizes,
        "smooth_non_pow2_sizes": smooth_non_pow2_sizes,
        "arbitrary_sizes": arbitrary_sizes,
    }

    if pow2_sizes:
        pow2_times = [benchmark_fft(s, iterations, warmup) for s in pow2_sizes]
        results["pow2_median_ns"] = np.median(pow2_times)
        results["pow2_times"] = pow2_times
    else:
        results["pow2_median_ns"] = None

    if smooth_non_pow2_sizes:
        smooth_times = [benchmark_fft(s, iterations, warmup) for s in smooth_non_pow2_sizes]
        results["smooth_non_pow2_median_ns"] = np.median(smooth_times)
        results["smooth_non_pow2_times"] = smooth_times
    else:
        results["smooth_non_pow2_median_ns"] = None

    if arbitrary_sizes:
        arbitrary_times = [benchmark_fft(s, iterations, warmup) for s in arbitrary_sizes]
        results["arbitrary_median_ns"] = np.median(arbitrary_times)
        results["arbitrary_times"] = arbitrary_times
    else:
        results["arbitrary_median_ns"] = None

    return results


def main():
    print("=" * 70)
    print("Power-of-2 vs 5-smooth (non-pow2) vs Arbitrary FFT Performance")
    print("=" * 70)
    print(f"Python: {sys.version.split()[0]}")
    print(f"NumPy: {np.__version__}")
    print("=" * 70)

    targets = [1000, 5000, 10000, 25000, 50000, 100000, 200000]

    for target in targets:
        print(f"\n--- Target: {target} ---")
        result = test_target(target, num_each=6, iterations=10, warmup=3)

        print(f"  Power-of-2 sizes:      {result['pow2_sizes']}")
        print(f"  5-smooth (non-pow2):   {result['smooth_non_pow2_sizes']}")
        print(f"  Arbitrary sizes:       {result['arbitrary_sizes'][:5]}...")

        if result["pow2_median_ns"] is not None:
            print(f"  Power-of-2 median:     {result['pow2_median_ns']/1e6:.3f} ms")
        if result["smooth_non_pow2_median_ns"] is not None:
            print(f"  5-smooth non-pow2 median: {result['smooth_non_pow2_median_ns']/1e6:.3f} ms")
        if result["arbitrary_median_ns"] is not None:
            print(f"  Arbitrary median:      {result['arbitrary_median_ns']/1e6:.3f} ms")

        # Compare
        if result["pow2_median_ns"] and result["smooth_non_pow2_median_ns"]:
            ratio = result["smooth_non_pow2_median_ns"] / result["pow2_median_ns"]
            if ratio < 1.05:
                winner = "~TIED"
            elif ratio < 1.0:
                winner = "5-smooth non-pow2 WINS"
            else:
                winner = "POWER-OF-2 WINS"
            print(f"  Ratio (smooth_non_pow2/pow2): {ratio:.2f}x  -> {winner}")

        if result["pow2_median_ns"] and result["arbitrary_median_ns"]:
            ratio = result["arbitrary_median_ns"] / result["pow2_median_ns"]
            print(f"  Ratio (arbitrary/pow2): {ratio:.2f}x")

    print("\n" + "=" * 70)
    print("CONCLUSION:")
    print("  If power-of-2 and 5-smooth non-pow2 are similar,")
    print("  it's the smooth factorization (2,3,5) that matters,")
    print("  not specifically power-of-2 memory alignment.")
    print("=" * 70)


if __name__ == "__main__":
    main()