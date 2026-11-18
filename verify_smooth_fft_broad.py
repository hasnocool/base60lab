#!/usr/bin/env python3
"""
Broader verification of Schumacher 2016 claim across multiple target sizes.
Tests multiple target ranges to ensure the result is general.
"""

import sys
import time
import math
import random
from typing import List, Tuple, Dict

import numpy as np
from scipy import fft


# ============================================================
# 5-smooth number generation
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


def test_target(target: int, num_each: int = 8, iterations: int = 10, warmup: int = 3, radius_factor: float = 0.02) -> Dict:
    """Test a single target size."""
    search_radius = max(500, int(target * radius_factor))

    smooth_sizes = find_5smooth_near(target, search_radius, num_each)
    arbitrary_sizes = generate_arbitrary_near(target, num_each, search_radius)

    if len(smooth_sizes) == 0:
        return {"target": target, "verdict": "NO_SMOOTH", "detail": "No 5-smooth numbers in range"}

    smooth_times = [benchmark_fft(s, iterations, warmup) for s in smooth_sizes]
    arbitrary_times = [benchmark_fft(s, iterations, warmup) for s in arbitrary_sizes]

    smooth_median = np.median(smooth_times)
    arbitrary_median = np.median(arbitrary_times)
    median_ratio = arbitrary_median / smooth_median

    if median_ratio > 1.05:
        verdict = "CONFIRMED"
    elif median_ratio < 0.95:
        verdict = "REFUTED"
    else:
        verdict = "PARTIAL"

    return {
        "target": target,
        "verdict": verdict,
        "median_ratio": median_ratio,
        "smooth_median_ns": smooth_median,
        "arbitrary_median_ns": arbitrary_median,
        "smooth_sizes": smooth_sizes,
        "arbitrary_sizes": arbitrary_sizes,
        "smooth_times": smooth_times,
        "arbitrary_times": arbitrary_times,
    }


def main():
    print("=" * 70)
    print("Broad Verification: 5-smooth FFT Performance Across Targets")
    print("=" * 70)
    print(f"Python: {sys.version.split()[0]}")
    print(f"NumPy: {np.__version__}")
    print("=" * 70)

    # Test multiple target sizes
    targets = [1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000, 1000000]

    all_results = []
    for target in targets:
        print(f"\n--- Target: {target} ---")
        result = test_target(target, num_each=8, iterations=10, warmup=3)
        all_results.append(result)

        print(f"  5-smooth sizes: {result.get('smooth_sizes', 'N/A')}")
        print(f"  Arbitrary sizes: {result.get('arbitrary_sizes', 'N/A')[:5]}...")
        if result["verdict"] != "NO_SMOOTH":
            print(f"  5-smooth median: {result['smooth_median_ns']/1e6:.3f} ms")
            print(f"  Arbitrary median: {result['arbitrary_median_ns']/1e6:.3f} ms")
            print(f"  Ratio: {result['median_ratio']:.2f}x")
            print(f"  Verdict: {result['verdict']}")
        else:
            print(f"  Verdict: {result['verdict']}")

    # Overall summary
    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)

    confirmed = sum(1 for r in all_results if r["verdict"] == "CONFIRMED")
    refuted = sum(1 for r in all_results if r["verdict"] == "REFUTED")
    partial = sum(1 for r in all_results if r["verdict"] == "PARTIAL")
    no_smooth = sum(1 for r in all_results if r["verdict"] == "NO_SMOOTH")

    print(f"Targets tested: {len(targets)}")
    print(f"CONFIRMED: {confirmed}")
    print(f"REFUTED: {refuted}")
    print(f"PARTIAL: {partial}")
    print(f"NO_SMOOTH: {no_smooth}")

    # Overall verdict
    if confirmed > 0 and refuted == 0:
        overall = "CONFIRMED"
    elif refuted > 0 and confirmed == 0:
        overall = "REFUTED"
    else:
        overall = "PARTIAL"

    print(f"\nOVERALL VERDICT: {overall}")

    # Show detail for each
    print("\nDetailed results:")
    for r in all_results:
        if r["verdict"] != "NO_SMOOTH":
            print(f"  {r['target']:>8d}: ratio={r['median_ratio']:.2f}x  {r['verdict']}")

    return overall


if __name__ == "__main__":
    verdict = main()
    if verdict == "CONFIRMED":
        sys.exit(0)
    elif verdict == "REFUTED":
        sys.exit(1)
    else:
        sys.exit(2)