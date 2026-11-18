#!/usr/bin/env python3
"""
Verify Ramanujan's partition congruences:
- p(5n + 4) ≡ 0 (mod 5)
- p(7n + 5) ≡ 0 (mod 7)
- p(11n + 6) ≡ 0 (mod 11)

Using the pentagonal number theorem recurrence:
p(n) = sum_{k!=0} (-1)^{k-1} p(n - k(3k-1)/2)
"""

def compute_partitions(max_n: int) -> list[int]:
    """Compute partition numbers p(0) through p(max_n) using pentagonal recurrence."""
    p = [0] * (max_n + 1)
    p[0] = 1  # p(0) = 1 by convention

    for n in range(1, max_n + 1):
        total = 0
        k = 1
        while True:
            # Generalized pentagonal numbers: k(3k-1)/2 for k = 1, -1, 2, -2, 3, -3, ...
            # For positive k: k(3k-1)/2
            # For negative k: (-k)(-3k-1)/2 = k(3k+1)/2
            pent1 = k * (3 * k - 1) // 2
            pent2 = k * (3 * k + 1) // 2

            if pent1 > n and pent2 > n:
                break

            sign = 1 if (k % 2 == 1) else -1  # (-1)^{k-1}

            if pent1 <= n:
                total += sign * p[n - pent1]
            if pent2 <= n:
                total += sign * p[n - pent2]

            k += 1

        p[n] = total

    return p


def verify_congruence(p: list[int], modulus: int, offset: int, step: int, max_n: int) -> tuple[str, list[int]]:
    """
    Verify p(step * n + offset) ≡ 0 (mod modulus) for all valid n.

    Returns (status, failures) where failures is list of indices where congruence fails.
    """
    failures = []
    n = 0
    while True:
        idx = step * n + offset
        if idx > max_n:
            break
        if p[idx] % modulus != 0:
            failures.append(idx)
        n += 1

    if not failures:
        return "CONFIRMED", []
    elif len(failures) < n:  # some passed, some failed
        return "PARTIAL", failures
    else:
        return "REFUTED", failures


def main():
    MAX_N = 500

    print(f"Computing partition numbers p(0) to p({MAX_N})...")
    p = compute_partitions(MAX_N)
    print(f"Done. p({MAX_N}) = {p[MAX_N]}")

    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)

    # Ramanujan's three congruences
    results = []

    # p(5n + 4) ≡ 0 (mod 5)
    status, failures = verify_congruence(p, 5, 4, 5, MAX_N)
    results.append(("p(5n+4) ≡ 0 (mod 5)", status, failures))
    print(f"\np(5n+4) ≡ 0 (mod 5): {status}")
    if failures:
        print(f"  Failures at indices: {failures[:20]}{'...' if len(failures) > 20 else ''} ({len(failures)} total)")
    else:
        print(f"  All {100} values verified (n=0..99)")

    # p(7n + 5) ≡ 0 (mod 7)
    status, failures = verify_congruence(p, 7, 5, 7, MAX_N)
    results.append(("p(7n+5) ≡ 0 (mod 7)", status, failures))
    print(f"\np(7n+5) ≡ 0 (mod 7): {status}")
    if failures:
        print(f"  Failures at indices: {failures[:20]}{'...' if len(failures) > 20 else ''} ({len(failures)} total)")
    else:
        max_n_7 = (MAX_N - 5) // 7
        print(f"  All {max_n_7 + 1} values verified (n=0..{max_n_7})")

    # p(11n + 6) ≡ 0 (mod 11)
    status, failures = verify_congruence(p, 11, 6, 11, MAX_N)
    results.append(("p(11n+6) ≡ 0 (mod 11)", status, failures))
    print(f"\np(11n+6) ≡ 0 (mod 11): {status}")
    if failures:
        print(f"  Failures at indices: {failures[:20]}{'...' if len(failures) > 20 else ''} ({len(failures)} total)")
    else:
        max_n_11 = (MAX_N - 6) // 11
        print(f"  All {max_n_11 + 1} values verified (n=0..{max_n_11})")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_confirmed = True
    for name, status, failures in results:
        print(f"  {name}: {status}")
        if status != "CONFIRMED":
            all_confirmed = False

    print(f"\nBase-60 factor check: 5 | 60 = {60 % 5 == 0} (True)")
    print(f"Overall: {'ALL CONFIRMED' if all_confirmed else 'SOME FAILED'}")

    return all_confirmed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)