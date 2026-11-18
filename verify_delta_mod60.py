#!/usr/bin/env python3
"""
Verify claim: Ramanujan Delta function Fourier coefficients τ(n) mod 60 follow a 60-cycle.
Source: Caldin 2026 (E8 Zenodo), lead L-10.
"""

def compute_sigma_1(limit):
    """Compute σ_1(k) = sum of divisors of k for k=1..limit"""
    sigma = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for multiple in range(d, limit + 1, d):
            sigma[multiple] += d
    return sigma

def compute_tau(limit):
    """
    Compute Ramanujan tau function τ(n) for n=1..limit using the recurrence:
    Δ(q) = q ∏_{n≥1} (1 - q^n)^24 = Σ_{n≥1} τ(n) q^n
    a_n = -24/n * Σ_{k=0}^{n-1} a_k σ_1(n-k),  a_0 = 1
    τ(n) = a_{n-1}
    """
    sigma = compute_sigma_1(limit)
    a = [0] * (limit + 1)
    a[0] = 1
    for n in range(1, limit + 1):
        s = 0
        for k in range(0, n):
            s += a[k] * sigma[n - k]
        a[n] = (-24 * s) // n
    tau = [0] * (limit + 1)
    for n in range(1, limit + 1):
        tau[n] = a[n - 1]
    return tau

def main():
    LIMIT = 1000
    tau = compute_tau(LIMIT)
    tau_mod60 = [tau[n] % 60 for n in range(1, LIMIT + 1)]

    # Known values for verification
    known = {
        1: 1, 2: -24, 3: 252, 4: -1472, 5: 4830,
        6: -6048, 7: -16744, 8: 84480, 9: -113643, 10: -115920
    }
    print("Verification against known τ(n) values:")
    for n, v in known.items():
        status = "✓" if tau[n] == v else "✗"
        print(f"  τ({n}) = {tau[n]} (expected {v}) {status}")
    print()

    # Check 60-cycle: τ(n+60) ≡ τ(n) mod 60 for n=1..940
    mismatches = []
    for n in range(1, LIMIT - 60 + 1):
        if tau_mod60[n + 60 - 1] != tau_mod60[n - 1]:
            mismatches.append((n, tau_mod60[n - 1], tau_mod60[n + 60 - 1]))

    print("=" * 60)
    print("CLAIM: τ(n) mod 60 follows a 60-cycle")
    print("=" * 60)
    if mismatches:
        print(f"VERDICT: REFUTED")
        print(f"Found {len(mismatches)} mismatches out of {LIMIT - 60} checks (n=1..{LIMIT-60})")
        print("\nFirst 20 mismatches:")
        for n, v1, v2 in mismatches[:20]:
            print(f"  n={n:4d}: τ({n})%60 = {v1:2d}, τ({n+60})%60 = {v2:2d}")
        if len(mismatches) > 20:
            print(f"  ... and {len(mismatches) - 20} more")
    else:
        print(f"VERDICT: CONFIRMED")
        print(f"60-cycle holds for all n=1..{LIMIT-60}")

    # Check for any cycle dividing 60
    print("\n--- Cycle search (divisors of 60) ---")
    for cycle in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]:
        ok = True
        for n in range(1, LIMIT - cycle + 1):
            if tau_mod60[n + cycle - 1] != tau_mod60[n - 1]:
                ok = False
                break
        status = "HOLDS" if ok else "FAILS"
        print(f"  Cycle {cycle:2d}: {status}")

    # Print first 120 values for reference
    print("\nFirst 120 values of τ(n) mod 60:")
    for i in range(0, 120, 60):
        row = tau_mod60[i:i+60]
        print(f"  n={i+1:3d}-{i+60:3d}: {row}")

if __name__ == "__main__":
    main()