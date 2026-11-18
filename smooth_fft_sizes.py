#!/usr/bin/env python3
"""
Smooth Number FFT Size Selector
Based on Schumacher 2016 (arXiv:1608.06928)

Provides exact counting and enumeration of 3-smooth (base-12) and 5-smooth (base-60) 
FFT sizes, with optimal size selection near target lengths.
"""

import math
from typing import List, Tuple, Optional
from bisect import bisect_left, bisect_right

# Logarithms of small primes
LOG2 = math.log(2)
LOG3 = math.log(3)
LOG5 = math.log(5)
LOG7 = math.log(7)

# ============================================================
# EXACT COUNTING FUNCTIONS (from paper's summation formulas)
# ============================================================

def count_2smooth(x: float) -> int:
    """N_2(x): Count of powers of 2 ≤ x"""
    if x < 1:
        return 0
    return int(math.floor(math.log(x) / LOG2)) + 1

def count_3smooth(x: float) -> int:
    """N_{2,3}(x): Count of 3-smooth numbers (2^p 3^q) ≤ x"""
    if x < 1:
        return 0
    count = 0
    max_q = int(math.floor(math.log(x) / LOG3))
    for q in range(max_q + 1):
        max_p = int(math.floor(math.log(x / (3**q)) / LOG2))
        count += max_p + 1
    return count

def count_5smooth(x: float) -> int:
    """N_{2,3,5}(x): Count of 5-smooth numbers (2^p 3^q 5^r) ≤ x"""
    if x < 1:
        return 0
    count = 0
    max_r = int(math.floor(math.log(x) / LOG5))
    for r in range(max_r + 1):
        x5 = x / (5**r)
        max_q = int(math.floor(math.log(x5) / LOG3))
        for q in range(max_q + 1):
            max_p = int(math.floor(math.log(x5 / (3**q)) / LOG2))
            count += max_p + 1
    return count

def count_7smooth(x: float) -> int:
    """N_{2,3,5,7}(x): Count of 7-smooth numbers ≤ x"""
    if x < 1:
        return 0
    count = 0
    max_f = int(math.floor(math.log(x) / LOG7))
    for f in range(max_f + 1):
        x7 = x / (7**f)
        max_r = int(math.floor(math.log(x7) / LOG5))
        for r in range(max_r + 1):
            x5 = x7 / (5**r)
            max_q = int(math.floor(math.log(x5) / LOG3))
            for q in range(max_q + 1):
                max_p = int(math.floor(math.log(x5 / (3**q)) / LOG2))
                count += max_p + 1
    return count

# ============================================================
# ASYMPTOTIC APPROXIMATIONS (Leading terms from paper)
# ============================================================

def asymptotic_3smooth(x: float) -> float:
    """Ramanujan's leading approximation for N_{2,3}(x)"""
    if x < 1:
        return 0
    return 0.5 * (math.log(2*x) * math.log(3*x)) / (LOG2 * LOG3) + 0.5

def asymptotic_5smooth(x: float) -> float:
    """Ramanujan's leading approximation for N_{2,3,5}(x)"""
    if x < 1:
        return 0
    return (math.sqrt(3) * math.log(x)**3) / (6 * LOG2 * LOG3 * LOG5) + 0.5

def asymptotic_7smooth(x: float) -> float:
    """Leading approximation for N_{2,3,5,7}(x)"""
    if x < 1:
        return 0
    return (math.log(x)**4) / (24 * LOG2 * LOG3 * LOG5 * LOG7) + 0.5

# ============================================================
# ENUMERATION (Generate all smooth numbers up to limit)
# ============================================================

def generate_3smooth(limit: int) -> List[int]:
    """Generate all 3-smooth numbers ≤ limit (sorted)"""
    result = []
    max_q = int(math.floor(math.log(limit) / LOG3))
    for q in range(max_q + 1):
        base = 3**q
        if base > limit:
            break
        max_p = int(math.floor(math.log(limit / base) / LOG2))
        for p in range(max_p + 1):
            val = base * (2**p)
            if val <= limit:
                result.append(val)
    return sorted(result)

def generate_5smooth(limit: int) -> List[int]:
    """Generate all 5-smooth numbers ≤ limit (sorted)"""
    result = []
    max_r = int(math.floor(math.log(limit) / LOG5))
    for r in range(max_r + 1):
        base5 = 5**r
        if base5 > limit:
            break
        max_q = int(math.floor(math.log(limit / base5) / LOG3))
        for q in range(max_q + 1):
            base3 = base5 * (3**q)
            if base3 > limit:
                break
            max_p = int(math.floor(math.log(limit / base3) / LOG2))
            for p in range(max_p + 1):
                val = base3 * (2**p)
                if val <= limit:
                    result.append(val)
    return sorted(result)

def generate_7smooth(limit: int) -> List[int]:
    """Generate all 7-smooth numbers ≤ limit (sorted)"""
    result = []
    max_f = int(math.floor(math.log(limit) / LOG7))
    for f in range(max_f + 1):
        base7 = 7**f
        if base7 > limit:
            break
        max_r = int(math.floor(math.log(limit / base7) / LOG5))
        for r in range(max_r + 1):
            base5 = base7 * (5**r)
            if base5 > limit:
                break
            max_q = int(math.floor(math.log(limit / base5) / LOG3))
            for q in range(max_q + 1):
                base3 = base5 * (3**q)
                if base3 > limit:
                    break
                max_p = int(math.floor(math.log(limit / base3) / LOG2))
                for p in range(max_p + 1):
                    val = base3 * (2**p)
                    if val <= limit:
                        result.append(val)
    return sorted(result)

# ============================================================
# OPTIMAL FFT SIZE SELECTION
# ============================================================

def find_optimal_3smooth_near(target: int, search_radius: Optional[int] = None) -> List[Tuple[int, float]]:
    """
    Find 3-smooth (base-12) FFT sizes near target.
    Returns list of (size, relative_error) sorted by error.
    """
    if search_radius is None:
        search_radius = max(1000, target // 100)
    
    # Generate candidates in range [target - radius, target + radius]
    lower = max(1, target - search_radius)
    upper = target + search_radius
    
    candidates = generate_3smooth(upper)
    candidates = [c for c in candidates if c >= lower]
    
    results = []
    for c in candidates:
        rel_error = abs(c - target) / target
        results.append((c, rel_error))
    
    return sorted(results, key=lambda x: x[1])

def find_optimal_5smooth_near(target: int, search_radius: Optional[int] = None) -> List[Tuple[int, float]]:
    """
    Find 5-smooth (base-60) FFT sizes near target.
    Returns list of (size, relative_error) sorted by error.
    """
    if search_radius is None:
        search_radius = max(1000, target // 100)
    
    lower = max(1, target - search_radius)
    upper = target + search_radius
    
    candidates = generate_5smooth(upper)
    candidates = [c for c in candidates if c >= lower]
    
    results = []
    for c in candidates:
        rel_error = abs(c - target) / target
        results.append((c, rel_error))
    
    return sorted(results, key=lambda x: x[1])

def find_optimal_7smooth_near(target: int, search_radius: Optional[int] = None) -> List[Tuple[int, float]]:
    """Find 7-smooth FFT sizes near target."""
    if search_radius is None:
        search_radius = max(1000, target // 100)
    
    lower = max(1, target - search_radius)
    upper = target + search_radius
    
    candidates = generate_7smooth(upper)
    candidates = [c for c in candidates if c >= lower]
    
    results = []
    for c in candidates:
        rel_error = abs(c - target) / target
        results.append((c, rel_error))
    
    return sorted(results, key=lambda x: x[1])

# ============================================================
# INVERSE: Estimate x given N (k-th smooth number)
# ============================================================

def estimate_x_from_N_3smooth(N: int) -> float:
    """Inverse of leading term: x ≈ exp(√(2 log2 log3 N))"""
    if N <= 0:
        return 1
    return math.exp(math.sqrt(2 * LOG2 * LOG3 * N))

def estimate_x_from_N_5smooth(N: int) -> float:
    """Inverse of leading term: x ≈ exp((6 log2 log3 log5 N)^{1/3})"""
    if N <= 0:
        return 1
    return math.exp((6 * LOG2 * LOG3 * LOG5 * N) ** (1/3))

def estimate_x_from_N_7smooth(N: int) -> float:
    """Inverse of leading term: x ≈ exp((24 log2 log3 log5 log7 N)^{1/4})"""
    if N <= 0:
        return 1
    return math.exp((24 * LOG2 * LOG3 * LOG5 * LOG7 * N) ** (1/4))

def find_kth_3smooth(k: int) -> int:
    """Find the k-th 3-smooth number (1-indexed) via binary search."""
    if k <= 0:
        raise ValueError("k must be positive")
    if k == 1:
        return 1
    
    # Use asymptotic estimate as upper bound
    x_est = estimate_x_from_N_3smooth(k)
    upper = int(x_est * 2) + 100
    lower = 1
    
    while lower < upper:
        mid = (lower + upper) // 2
        if count_3smooth(mid) < k:
            lower = mid + 1
        else:
            upper = mid
    
    # Ensure exact match
    while count_3smooth(lower) < k:
        lower += 1
    while lower > 1 and count_3smooth(lower - 1) >= k:
        lower -= 1
    
    return lower

def find_kth_5smooth(k: int) -> int:
    """Find the k-th 5-smooth number (1-indexed) via binary search."""
    if k <= 0:
        raise ValueError("k must be positive")
    if k == 1:
        return 1
    
    x_est = estimate_x_from_N_5smooth(k)
    upper = int(x_est * 2) + 100
    lower = 1
    
    while lower < upper:
        mid = (lower + upper) // 2
        if count_5smooth(mid) < k:
            lower = mid + 1
        else:
            upper = mid
    
    while count_5smooth(lower) < k:
        lower += 1
    while lower > 1 and count_5smooth(lower - 1) >= k:
        lower -= 1
    
    return lower

# ============================================================
# DENSITY ANALYSIS
# ============================================================

def density_analysis(target: int) -> dict:
    """Analyze smooth number density around target."""
    return {
        "target": target,
        "count_3smooth": count_3smooth(target),
        "count_5smooth": count_5smooth(target),
        "count_7smooth": count_7smooth(target),
        "asymptotic_3smooth": asymptotic_3smooth(target),
        "asymptotic_5smooth": asymptotic_5smooth(target),
        "asymptotic_7smooth": asymptotic_7smooth(target),
        "avg_gap_3smooth": target / max(1, count_3smooth(target)),
        "avg_gap_5smooth": target / max(1, count_5smooth(target)),
        "avg_gap_7smooth": target / max(1, count_7smooth(target)),
    }

# ============================================================
# DEMO / TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SCHUMACHER 2016 SMOOTH NUMBER FFT SIZE SELECTOR")
    print("Based on arXiv:1608.06928 - Convergent formulas for smooth numbers")
    print("=" * 70)
    
    # Verify against paper's tables
    print("\n--- Verification against paper's Table 1 (3-smooth) ---")
    test_points = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
    for x in test_points:
        exact = count_3smooth(x)
        asym = asymptotic_3smooth(x)
        print(f"N_{{2,3}}({x:>10}) = {exact:>6}  (asymptotic: {asym:.3f})")
    
    print("\n--- Verification against paper's Table 3 (5-smooth) ---")
    for x in test_points:
        exact = count_5smooth(x)
        asym = asymptotic_5smooth(x)
        print(f"N_{{2,3,5}}({x:>10}) = {exact:>6}  (asymptotic: {asym:.3f})")
    
    print("\n--- Verification against paper's Table 4 (7-smooth) ---")
    for x in test_points:
        exact = count_7smooth(x)
        asym = asymptotic_7smooth(x)
        print(f"N_{{2,3,5,7}}({x:>10}) = {exact:>6}  (asymptotic: {asym:.3f})")
    
    # Optimal FFT size selection examples
    print("\n--- Base-12 (3-smooth) FFT sizes near 1024 ---")
    results = find_optimal_3smooth_near(1024, 200)
    for size, err in results[:10]:
        print(f"  {size:>6}  (error: {err*100:.2f}%)")
    
    print("\n--- Base-60 (5-smooth) FFT sizes near 1024 ---")
    results = find_optimal_5smooth_near(1024, 200)
    for size, err in results[:10]:
        print(f"  {size:>6}  (error: {err*100:.2f}%)")
    
    print("\n--- Base-60 (5-smooth) FFT sizes near 10000 ---")
    results = find_optimal_5smooth_near(10000, 500)
    for size, err in results[:10]:
        print(f"  {size:>6}  (error: {err*100:.2f}%)")
    
    print("\n--- Density analysis at various scales ---")
    for target in [1000, 10000, 100000, 1000000, 10000000]:
        d = density_analysis(target)
        print(f"\nTarget {target}:")
        print(f"  3-smooth:  count={d['count_3smooth']:>5}, avg gap≈{d['avg_gap_3smooth']:.1f}")
        print(f"  5-smooth:  count={d['count_5smooth']:>5}, avg gap≈{d['avg_gap_5smooth']:.1f}")
        print(f"  7-smooth:  count={d['count_7smooth']:>5}, avg gap≈{d['avg_gap_7smooth']:.1f}")
    
    # Inverse: k-th smooth number
    print("\n--- k-th smooth numbers ---")
    for k in [1, 10, 100, 1000, 10000]:
        kth_3 = find_kth_3smooth(k)
        kth_5 = find_kth_5smooth(k)
        print(f"  k={k:>5}:  3-smooth={kth_3:>8},  5-smooth={kth_5:>8}")
    
    print("\n" + "=" * 70)
    print("APPLICATION TO EXPERIMENT D:")
    print("  - Use find_optimal_3smooth_near() for base-12 FFT sizes")
    print("  - Use find_optimal_5smooth_near() for base-60 FFT sizes")
    print("  - Use density_analysis() to estimate candidate pool size")
    print("  - Asymptotic formulas give quick density estimates")
    print("=" * 70)