"""Base-60 RNS NTT for Post-Quantum Cryptography.

This module implements:
- RNS class with 60-smooth prime moduli set generation
- NTT class with mixed-radix Cooley-Tukey butterflies (radix-2, 3, 4, 5)
- CRT reconstruction using Garner's algorithm
- Kyber/Dilithium/Falcon parameter integration

Key insight: 60-smooth moduli (p where p-1 factors only into primes ≤ 59)
enable mixed-radix NTT with radices {2,3,4,5}, exploiting base-60's factorization 2²×3×5.
"""

from __future__ import annotations

import heapq
import math
import random
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any

from .modular import mod_add, mod_sub, mod_mul, mod_pow, mod_inv
from .numerals import int_to_base


# ========================================================================
# 60-Smooth Prime Generation
# ========================================================================

_PRIMES_UPTO_60 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 2^64."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int) -> dict[int, int]:
    """Return prime factorization of n as {prime: exponent}."""
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def is_60_smooth(n: int) -> bool:
    """Check if n is 60-smooth (all prime factors ≤ 59)."""
    return all(p <= 59 for p in prime_factors(n))


def generate_60_smooth_primes(
    min_bits: int = 16,
    max_bits: int = 32,
    count: int = 20,
) -> list[dict[str, Any]]:
    """Generate primes p where p-1 is 60-smooth (NTT-friendly moduli).

    These primes enable mixed-radix NTT with radices {2,3,4,5} because
    p-1 has only small prime factors, allowing large power-of-2,3,5 transform lengths.

    Args:
        min_bits: Minimum bit-length of prime
        max_bits: Maximum bit-length of prime
        count: Number of primes to find

    Returns:
        List of dicts with prime info including p-1 factorization
    """
    results = []
    min_val = 1 << min_bits
    max_val = 1 << max_bits

    # Generate 60-smooth numbers using a priority queue (like Hamming numbers)
    # Only need small primes for N: 2, 3, 5, 7, 11, 13
    smooth_primes = [2, 3, 5, 7, 11, 13]
    smooth_numbers = []
    seen = {1}
    max_smooth = 1 << 18  # Limit for N

    heap = [1]
    while heap:
        n = heapq.heappop(heap)
        if n > max_smooth:
            break
        smooth_numbers.append(n)
        for p in smooth_primes:
            next_n = n * p
            if next_n <= max_smooth and next_n not in seen:
                seen.add(next_n)
                heapq.heappush(heap, next_n)

    smooth_numbers = [n for n in smooth_numbers if n > 1]
    smooth_numbers.sort()

    for N in smooth_numbers:
        if len(results) >= count:
            break
        # Search k such that p = k*N + 1 is prime and in bit range
        max_k = max_val // N + 1
        # Limit k search for speed
        for k in range(1, min(max_k, 500)):
            p = k * N + 1
            if p < min_val:
                continue
            if p >= max_val:
                break
            if is_prime(p):
                pf = prime_factors(p - 1)
                max_pf = max(pf.keys()) if pf else 1
                results.append({
                    "prime": p,
                    "prime_base60": int_to_base(p, 60),
                    "prime_base12": int_to_base(p, 12),
                    "prime_bits": p.bit_length(),
                    "N": N,
                    "k": k,
                    "p_minus_1_factors": pf,
                    "max_prime_factor": max_pf,
                    "max_transform_power_2": pf.get(2, 0),
                    "max_transform_power_3": pf.get(3, 0),
                    "max_transform_power_5": pf.get(5, 0),
                    "max_transform_length_2": 1 << pf.get(2, 0),
                    "max_transform_length_3": 3 ** pf.get(3, 0),
                    "max_transform_length_5": 5 ** pf.get(5, 0),
                })

    return sorted(results, key=lambda x: x["prime"])


@dataclass(frozen=True)
class RNSModuliSet:
    """RNS moduli set with pairwise co-prime moduli.

    For NTT, we need moduli that are primes where p-1 is 60-smooth,
    enabling large mixed-radix transforms.
    """
    moduli: tuple[int, ...]
    dynamic_range: int = field(init=False)
    total_bits: int = field(init=False)
    max_transform_len: int = field(init=False)

    def __post_init__(self) -> None:
        # Verify pairwise co-prime
        for i, m1 in enumerate(self.moduli):
            for m2 in self.moduli[i + 1:]:
                if math.gcd(m1, m2) != 1:
                    raise ValueError(f"Moduli {m1} and {m2} are not co-prime")
        if not all(is_prime(m) for m in self.moduli):
            raise ValueError("All moduli must be prime")
        if not all(is_60_smooth(m - 1) for m in self.moduli):
            raise ValueError("All moduli must have 60-smooth p-1")

        object.__setattr__(self, "dynamic_range", math.prod(self.moduli))
        object.__setattr__(self, "total_bits", sum(m.bit_length() for m in self.moduli))
        # Max transform length is limited by min(p-1) across moduli
        max_len = min(m - 1 for m in self.moduli)
        object.__setattr__(self, "max_transform_len", max_len)

    def to_dict(self) -> dict[str, Any]:
        return {
            "moduli": list(self.moduli),
            "moduli_base60": [int_to_base(m, 60) for m in self.moduli],
            "moduli_base12": [int_to_base(m, 12) for m in self.moduli],
            "dynamic_range": self.dynamic_range,
            "total_bits": self.total_bits,
            "num_moduli": len(self.moduli),
            "max_transform_len": self.max_transform_len,
        }


def generate_rns_moduli_sets(
    target_bits: int,
    num_moduli: int = 4,
    max_candidates: int = 10,
) -> list[RNSModuliSet]:
    """Generate RNS moduli sets for a target bit-width.

    Args:
        target_bits: Target total bit-width (e.g., 32, 64, 128)
        num_moduli: Number of moduli in the set
        max_candidates: Maximum number of sets to return

    Returns:
        List of RNSModuliSet sorted by closeness to target_bits
    """
    # Generate candidate primes - limit count for speed
    primes_data = generate_60_smooth_primes(
        min_bits=max(8, target_bits // num_moduli - 4),
        max_bits=target_bits // num_moduli + 6,
        count=30,
    )
    primes = [p["prime"] for p in primes_data]

    # Find combinations of num_moduli primes - limit combinations for speed
    candidates = []
    combo_count = 0
    max_combos = 5000
    for combo in combinations(primes, num_moduli):
        combo_count += 1
        if combo_count > max_combos:
            break
        try:
            rns = RNSModuliSet(moduli=combo)
            candidates.append(rns)
        except ValueError:
            continue

    # Sort by closeness to target_bits
    candidates.sort(key=lambda r: abs(r.total_bits - target_bits))
    return candidates[:max_candidates]


# ========================================================================
# CRT Reconstruction (Garner's Algorithm)
# ========================================================================

def garner_reconstruct(
    residues: list[int],
    moduli: list[int],
    precomputed: dict[str, Any] | None = None,
) -> int:
    """Chinese Remainder Theorem reconstruction using Garner's algorithm.

    Garner's algorithm is more efficient than standard CRT for RNS
    as it avoids large intermediate products.

    Args:
        residues: Residues [x mod m_i]
        moduli: Co-prime moduli [m_i]
        precomputed: Optional precomputed constants for repeated use

    Returns:
        Reconstructed integer x in [0, prod(moduli))
    """
    n = len(moduli)
    if len(residues) != n:
        raise ValueError("Residues and moduli length mismatch")

    if precomputed is None:
        # Compute Garner constants: c[i][j] = m_i^{-1} mod m_j for i < j
        c: list[list[int]] = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                c[i][j] = mod_inv(moduli[i], moduli[j])
        precomputed = {"c": c}

    c = precomputed["c"]
    u = residues.copy()

    # Garner's algorithm
    for i in range(1, n):
        for j in range(i):
            u[i] = mod_mul(mod_sub(u[i], u[j], moduli[i]), c[j][i], moduli[i])

    # Reconstruct: x = u[0] + u[1]*m[0] + u[2]*m[0]*m[1] + ...
    x = u[0]
    mult = 1
    for i in range(1, n):
        mult *= moduli[i - 1]
        x += u[i] * mult

    return x


def garner_precompute(moduli: list[int]) -> dict[str, Any]:
    """Precompute Garner constants for a moduli set."""
    n = len(moduli)
    c: list[list[int]] = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            c[i][j] = mod_inv(moduli[i], moduli[j])
    return {"c": c, "moduli": moduli}


# ========================================================================
# Mixed-Radix NTT Implementation
# ========================================================================

@dataclass(frozen=True)
class NTTParameters:
    """NTT parameters for a specific prime modulus."""
    prime: int
    primitive_root: int
    max_power_of_2: int
    max_power_of_3: int
    max_power_of_5: int
    supported_radices: tuple[int, ...] = (2, 3, 4, 5)

    def max_transform_length(self) -> int:
        return min(self.prime - 1, (1 << self.max_power_of_2) * (3 ** self.max_power_of_3) * (5 ** self.max_power_of_5))

    def to_dict(self) -> dict[str, Any]:
        return {
            "prime": self.prime,
            "prime_base60": int_to_base(self.prime, 60),
            "prime_base12": int_to_base(self.prime, 12),
            "primitive_root": self.primitive_root,
            "primitive_root_base60": int_to_base(self.primitive_root, 60),
            "max_power_of_2": self.max_power_of_2,
            "max_power_of_3": self.max_power_of_3,
            "max_power_of_5": self.max_power_of_5,
            "max_transform_length": self.max_transform_length(),
            "supported_radices": list(self.supported_radices),
        }


def find_primitive_root_for_ntt(p: int, N: int) -> int | None:
    """Find primitive N-th root of unity modulo prime p.

    We need g such that g^N ≡ 1 (mod p) and g^(N/r) ≢ 1 for all prime factors r of N.
    """
    if not is_prime(p):
        return None
    if (p - 1) % N != 0:
        return None

    phi = p - 1
    factors = prime_factors(phi)
    # We want order N, so test candidates
    for g in range(2, p):
        if pow(g, phi, p) != 1:
            continue
        ok = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                ok = False
                break
        if ok:
            # g is primitive root of p, now compute N-th root
            return pow(g, phi // N, p)
    return None


def compute_ntt_parameters(prime: int) -> NTTParameters | None:
    """Compute NTT parameters for a prime with 60-smooth p-1."""
    if not is_prime(prime):
        return None
    if not is_60_smooth(prime - 1):
        return None

    pf = prime_factors(prime - 1)
    max_pow_2 = pf.get(2, 0)
    max_pow_3 = pf.get(3, 0)
    max_pow_5 = pf.get(5, 0)

    # Find primitive root of the field
    primitive_root = find_primitive_root_for_ntt(prime, prime - 1)
    if primitive_root is None:
        return None

    return NTTParameters(
        prime=prime,
        primitive_root=primitive_root,
        max_power_of_2=max_pow_2,
        max_power_of_3=max_pow_3,
        max_power_of_5=max_pow_5,
    )


def radix_decomposition(N: int, supported_radices: tuple[int, ...] = (2, 3, 4, 5)) -> list[dict[str, Any]]:
    """Decompose transform length N into mixed-radix stages for Cooley-Tukey.

    Returns list of stages with radix and size info.
    """
    if N <= 1:
        return []

    stages = []
    remaining = N
    radices = sorted(supported_radices, reverse=True)

    while remaining > 1:
        for r in radices:
            if remaining % r == 0:
                stages.append({"radix": r, "size": remaining, "sub_size": remaining // r})
                remaining //= r
                break
        else:
            # No supported radix divides remaining
            raise ValueError(f"Cannot decompose {remaining} with radices {supported_radices}")

    return stages


@dataclass
class MixedRadixNTT:
    """Mixed-Radix NTT implementation with Cooley-Tukey butterflies.

    Supports radices 2, 3, 4, 5 for 60-smooth transform lengths.
    Uses Gentleman-Sande (decimation-in-frequency) for in-place computation.
    """
    params: NTTParameters
    _twiddles: dict[int, list[int]] = field(default_factory=dict, init=False, repr=False)
    _radix_stages: list[dict[str, Any]] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        # Precompute twiddle factors for all needed lengths
        self._precompute_twiddles()

    def _precompute_twiddles(self) -> None:
        """Precompute twiddle factors for all power-of-radix lengths."""
        max_len = self.params.max_transform_length()
        # For each radix, precompute twiddles
        for r in self.params.supported_radices:
            length = r
            while length <= max_len:
                if length not in self._twiddles:
                    self._twiddles[length] = self._compute_twiddles_for_length(length)
                length *= r

    def _compute_twiddles_for_length(self, N: int) -> list[int]:
        """Compute twiddle factors for N-point transform."""
        # w = primitive_root^((p-1)/N) is primitive N-th root of unity
        w = pow(self.params.primitive_root, (self.params.prime - 1) // N, self.params.prime)
        twiddles = [1]
        for k in range(1, N):
            twiddles.append(mod_mul(twiddles[-1], w, self.params.prime))
        return twiddles
    def forward(self, data: list[int]) -> list[int]:
        """Forward NTT (polynomial -> NTT domain) using Cooley-Tukey decimation-in-time.

        Args:
            data: Input coefficients (length must be power of supported radices)

        Returns:
            NTT-transformed coefficients
        """
        N = len(data)
        if N == 0:
            return []
        if N == 1:
            return [data[0] % self.params.prime]

        # Validate length
        stages = radix_decomposition(N, self.params.supported_radices)
        self._radix_stages = stages

        # Copy data to working array
        a = [x % self.params.prime for x in data]

        # Cooley-Tukey decimation-in-time (DIT)
        for stage in stages:
            r = stage["radix"]
            size = stage["size"]
            sub_size = stage["sub_size"]

            # Get twiddle factors for this stage
            twiddles = self._twiddles[r]

            # Butterfly operations - DIT
            for i in range(0, N, size):
                for j in range(sub_size):
                    # Load r elements
                    idx = [i + j + k * sub_size for k in range(r)]
                    vals = [a[idx[k]] for k in range(r)]

                    # Apply radix-r butterfly (DIT)
                    if r == 2:
                        # Radix-2 DIT: (a, b) -> (a + b*w, a - b*w)
                        # where w = twiddle factor
                        u = vals[0]
                        v = mod_mul(vals[1], twiddles[1], self.params.prime)
                        a[idx[0]] = mod_add(u, v, self.params.prime)
                        a[idx[1]] = mod_sub(u, v, self.params.prime)
                    elif r == 3:
                        # Radix-3 DIT butterfly
                        w1 = twiddles[1]
                        w2 = twiddles[2]
                        u0 = mod_add(vals[0], mod_add(mod_mul(vals[1], w1, self.params.prime), mod_mul(vals[2], w2, self.params.prime), self.params.prime), self.params.prime)
                        u1 = mod_add(vals[0], mod_add(mod_mul(vals[1], w2, self.params.prime), mod_mul(vals[2], w1, self.params.prime), self.params.prime), self.params.prime)
                        u2 = mod_add(vals[0], mod_add(mod_mul(vals[1], w1*w1 % self.params.prime, self.params.prime), mod_mul(vals[2], w2*w2 % self.params.prime, self.params.prime), self.params.prime), self.params.prime)
                        # Simplified radix-3 DIT using DFT-3 matrix
                        # X[0] = x[0] + x[1] + x[2]
                        # X[1] = x[0] + x[1]*w + x[2]*w^2
                        # X[2] = x[0] + x[1]*w^2 + x[2]*w
                        w1_sq = mod_mul(w1, w1, self.params.prime)
                        w2_sq = mod_mul(w2, w2, self.params.prime)
                        u0 = mod_add(vals[0], mod_add(vals[1], vals[2], self.params.prime), self.params.prime)
                        u1 = mod_add(vals[0], mod_add(mod_mul(vals[1], w1, self.params.prime), mod_mul(vals[2], w2, self.params.prime), self.params.prime), self.params.prime)
                        u2 = mod_add(vals[0], mod_add(mod_mul(vals[1], w2, self.params.prime), mod_mul(vals[2], w1, self.params.prime), self.params.prime), self.params.prime)
                        a[idx[0]] = u0
                        a[idx[1]] = u1
                        a[idx[2]] = u2
                    elif r == 4:
                        # Radix-4 DIT butterfly (using 2x2 structure)
                        # Standard DIT radix-4: first compute 2x2 DFTs, then apply twiddles
                        w1 = twiddles[1]
                        w2 = twiddles[2]
                        w3 = twiddles[3]
                        # First 2x2 DFTs on (0,2) and (1,3)
                        t0 = mod_add(vals[0], vals[2], self.params.prime)
                        t1 = mod_sub(vals[0], vals[2], self.params.prime)
                        t2 = mod_add(vals[1], vals[3], self.params.prime)
                        t3 = mod_sub(vals[1], vals[3], self.params.prime)
                        # Apply twiddles and combine
                        a[idx[0]] = mod_add(t0, t2, self.params.prime)
                        a[idx[2]] = mod_sub(t0, t2, self.params.prime)
                        a[idx[1]] = mod_add(mod_mul(t1, w1, self.params.prime), mod_mul(t3, w3, self.params.prime), self.params.prime)
                        a[idx[3]] = mod_sub(mod_mul(t1, w1, self.params.prime), mod_mul(t3, w3, self.params.prime), self.params.prime)
                    elif r == 5:
                        # Radix-5 DIT butterfly (full DFT-5)
                        w = [twiddles[k] for k in range(5)]
                        out = [0] * 5
                        for k in range(5):
                            acc = 0
                            for j in range(5):
                                exp = (j * k) % 5
                                acc = mod_add(acc, mod_mul(vals[j], w[exp], self.params.prime), self.params.prime)
                            out[k] = acc
                        for k in range(5):
                            a[idx[k]] = out[k]

        return a
    def forward(self, data: list[int]) -> list[int]:
        """Forward NTT (polynomial -> NTT domain).

        Args:
            data: Input coefficients (length must be power of supported radices)

        Returns:
            NTT-transformed coefficients
        """
        N = len(data)
        if N == 0:
            return []
        if N == 1:
            return [data[0] % self.params.prime]

        # Validate length
        stages = radix_decomposition(N, self.params.supported_radices)
        self._radix_stages = stages

        # Copy data to working array
        a = [x % self.params.prime for x in data]

        # Cooley-Tukey decimation-in-time (Gentleman-Sande)
        for stage in stages:
            r = stage["radix"]
            size = stage["size"]
            sub_size = stage["sub_size"]

            # Get twiddle factors for this stage
            twiddles = self._twiddles[r]

            # Butterfly operations
            for i in range(0, N, size):
                for j in range(sub_size):
                    # Load r elements
                    idx = [i + j + k * sub_size for k in range(r)]
                    vals = [a[idx[k]] for k in range(r)]

                    # Apply radix-r butterfly
                    if r == 2:
                        # Radix-2: (a, b) -> (a+b, (a-b)*w)
                        u = mod_add(vals[0], vals[1], self.params.prime)
                        v = mod_mul(mod_sub(vals[0], vals[1], self.params.prime), twiddles[1], self.params.prime)
                        a[idx[0]] = u
                        a[idx[1]] = v
                    elif r == 3:
                        # Radix-3 butterfly
                        w1 = twiddles[1]
                        w2 = twiddles[2]
                        u0 = mod_add(vals[0], mod_add(vals[1], vals[2], self.params.prime), self.params.prime)
                        u1 = mod_add(vals[0], mod_add(mod_mul(vals[1], w1, self.params.prime), mod_mul(vals[2], w2, self.params.prime), self.params.prime), self.params.prime)
                        u2 = mod_add(vals[0], mod_add(mod_mul(vals[1], w2, self.params.prime), mod_mul(vals[2], w1, self.params.prime), self.params.prime), self.params.prime)
                        a[idx[0]] = u0
                        a[idx[1]] = u1
                        a[idx[2]] = u2
                    elif r == 4:
                        # Radix-4 butterfly (using 2x2 structure)
                        w1 = twiddles[1]
                        w2 = twiddles[2]
                        w3 = twiddles[3]
                        # First 2x2
                        t0 = mod_add(vals[0], vals[2], self.params.prime)
                        t1 = mod_sub(vals[0], vals[2], self.params.prime)
                        t2 = mod_add(vals[1], vals[3], self.params.prime)
                        t3 = mod_mul(mod_sub(vals[1], vals[3], self.params.prime), w2, self.params.prime)
                        # Second 2x2 with twiddles
                        a[idx[0]] = mod_add(t0, t2, self.params.prime)
                        a[idx[2]] = mod_sub(t0, t2, self.params.prime)
                        a[idx[1]] = mod_add(t1, t3, self.params.prime)
                        a[idx[3]] = mod_sub(t1, t3, self.params.prime)
                    elif r == 5:
                        # Radix-5 butterfly
                        w = [twiddles[k] for k in range(5)]
                        # DFT-5 matrix multiplication (optimized)
                        out = [0] * 5
                        for k in range(5):
                            acc = 0
                            for j in range(5):
                                exp = (j * k) % 5
                                acc = mod_add(acc, mod_mul(vals[j], w[exp], self.params.prime), self.params.prime)
                            out[k] = acc
                        for k in range(5):
                            a[idx[k]] = out[k]

        return a

    def inverse(self, data: list[int]) -> list[int]:
        """Inverse NTT (NTT domain -> polynomial).

        Args:
            data: NTT-domain coefficients

        Returns:
            Reconstructed polynomial coefficients
        """
        N = len(data)
        if N == 0:
            return []
        if N == 1:
            return [data[0] % self.params.prime]

        stages = radix_decomposition(N, self.params.supported_radices)
        # Reverse stages for inverse
        stages_rev = list(reversed(stages))

        a = [x % self.params.prime for x in data]

        # Cooley-Tukey decimation-in-frequency for inverse
        for stage in stages_rev:
            r = stage["radix"]
            size = stage["size"]
            sub_size = stage["sub_size"]

            # For inverse, use conjugated twiddle factors (w^{-1})
            twiddles = self._twiddles[r]
            # Inverse twiddles: w^{-k} = w^{N-k}
            inv_twiddles = [twiddles[0]] + [twiddles[r - k] for k in range(1, r)]

            for i in range(0, N, size):
                for j in range(sub_size):
                    idx = [i + j + k * sub_size for k in range(r)]
                    vals = [a[idx[k]] for k in range(r)]

                    if r == 2:
                        u = mod_add(vals[0], vals[1], self.params.prime)
                        v = mod_mul(mod_sub(vals[0], vals[1], self.params.prime), inv_twiddles[1], self.params.prime)
                        a[idx[0]] = u
                        a[idx[1]] = v
                    elif r == 3:
                        w1 = inv_twiddles[1]
                        w2 = inv_twiddles[2]
                        u0 = mod_add(vals[0], mod_add(vals[1], vals[2], self.params.prime), self.params.prime)
                        u1 = mod_add(vals[0], mod_add(mod_mul(vals[1], w1, self.params.prime), mod_mul(vals[2], w2, self.params.prime), self.params.prime), self.params.prime)
                        u2 = mod_add(vals[0], mod_add(mod_mul(vals[1], w2, self.params.prime), mod_mul(vals[2], w1, self.params.prime), self.params.prime), self.params.prime)
                        a[idx[0]] = u0
                        a[idx[1]] = u1
                        a[idx[2]] = u2
                    elif r == 4:
                        w1 = inv_twiddles[1]
                        w2 = inv_twiddles[2]
                        w3 = inv_twiddles[3]
                        t0 = mod_add(vals[0], vals[2], self.params.prime)
                        t1 = mod_sub(vals[0], vals[2], self.params.prime)
                        t2 = mod_add(vals[1], vals[3], self.params.prime)
                        t3 = mod_mul(mod_sub(vals[1], vals[3], self.params.prime), w2, self.params.prime)
                        a[idx[0]] = mod_add(t0, t2, self.params.prime)
                        a[idx[2]] = mod_sub(t0, t2, self.params.prime)
                        a[idx[1]] = mod_add(t1, t3, self.params.prime)
                        a[idx[3]] = mod_sub(t1, t3, self.params.prime)
                    elif r == 5:
                        w = [inv_twiddles[k] for k in range(5)]
                        out = [0] * 5
                        for k in range(5):
                            acc = 0
                            for j in range(5):
                                exp = (j * k) % 5
                                acc = mod_add(acc, mod_mul(vals[j], w[exp], self.params.prime), self.params.prime)
                            out[k] = acc
                        for k in range(5):
                            a[idx[k]] = out[k]

        # Scale by N^{-1}
        n_inv = mod_inv(N, self.params.prime)
        return [mod_mul(x, n_inv, self.params.prime) for x in a]

    def verify(self, test_data: list[int] | None = None) -> dict[str, Any]:
        """Verify NTT correctness with round-trip test."""
        if test_data is None:
            # Generate random test data
            N = self.params.max_transform_length()
            # Use a power of 2 for simplicity
            N = 1 << min(self.params.max_power_of_2, 8)
            test_data = [random.randint(0, self.params.prime - 1) for _ in range(N)]

        forward_result = self.forward(test_data)
        inverse_result = self.inverse(forward_result)

        # Check round-trip
        success = all(
            (inverse_result[i] - test_data[i]) % self.params.prime == 0
            for i in range(len(test_data))
        )

        return {
            "prime": self.params.prime,
            "transform_length": len(test_data),
            "round_trip_success": success,
            "max_error": max(
                (inverse_result[i] - test_data[i]) % self.params.prime
                for i in range(len(test_data))
            ) if not success else 0,
        }


# ========================================================================
# RNS-NTT Combination for Large Moduli
# ========================================================================

@dataclass
class RNSNTT:
    """RNS-based NTT for large dynamic ranges.

    Combines multiple NTT channels (each modulo a 60-smooth prime)
    using CRT for reconstruction. Enables carry-free arithmetic
    for PQC parameter sizes (Kyber-768: 12*256 coefficients mod 3329).
    """
    moduli_set: RNSModuliSet
    _ntts: list[MixedRadixNTT] = field(default_factory=list, init=False, repr=False)
    _garner_precomp: dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        self._ntts = []
        for p in self.moduli_set.moduli:
            params = compute_ntt_parameters(p)
            if params is None:
                raise ValueError(f"Prime {p} not suitable for NTT")
            self._ntts.append(MixedRadixNTT(params))
        self._garner_precomp = garner_precompute(list(self.moduli_set.moduli))

    def max_transform_length(self) -> int:
        return self.moduli_set.max_transform_len

    def forward_rns(self, data: list[int]) -> list[list[int]]:
        """Forward NTT on all RNS channels.

        Args:
            data: Input polynomial coefficients (length = transform length)

        Returns:
            List of NTT results per modulus
        """
        results = []
        for ntt in self._ntts:
            results.append(ntt.forward(data))
        return results

    def inverse_rns(self, rns_data: list[list[int]]) -> list[int]:
        """Inverse NTT on all RNS channels with CRT reconstruction.

        Args:
            rns_data: NTT results per modulus [channel][coefficient]

        Returns:
            Reconstructed polynomial coefficients
        """
        if len(rns_data) != len(self._ntts):
            raise ValueError("RNS data channel count mismatch")

        # Inverse NTT per channel
        inv_results = []
        for i, ntt in enumerate(self._ntts):
            inv_results.append(ntt.inverse(rns_data[i]))

        # CRT reconstruction coefficient-wise
        N = len(inv_results[0])
        reconstructed = []
        for j in range(N):
            residues = [inv_results[i][j] for i in range(len(self._ntts))]
            reconstructed.append(garner_reconstruct(residues, list(self.moduli_set.moduli), self._garner_precomp))

        return reconstructed

    def multiply_polynomials(self, a: list[int], b: list[int]) -> list[int]:
        """Multiply two polynomials using RNS-NTT.

        This is the core operation for PQC (Kyber, Dilithium, Falcon).
        """
        N = len(a)
        if len(b) != N:
            raise ValueError("Polynomials must have same length")

        # Forward NTT on both
        a_ntt = self.forward_rns(a)
        b_ntt = self.forward_rns(b)

        # Pointwise multiplication in NTT domain per channel
        c_ntt = []
        for i in range(len(self._ntts)):
            p = self.moduli_set.moduli[i]
            c_channel = [mod_mul(a_ntt[i][j], b_ntt[i][j], p) for j in range(N)]
            c_ntt.append(c_channel)

        # Inverse NTT with CRT
        return self.inverse_rns(c_ntt)


# ========================================================================
# PQC Standard Parameters
# ========================================================================

@dataclass(frozen=True)
class PQCStandard:
    """PQC standard parameters requiring NTT."""
    name: str
    n: int  # Polynomial degree (usually 256)
    q: int  # Modulus
    k: int  # Module rank (for ML-KEM/ML-DSA)
    l: int  # For Dilithium
    eta: int  # Noise parameter
    algorithm: str  # "Kyber", "Dilithium", "Falcon"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "n": self.n,
            "q": self.q,
            "k": self.k,
            "l": self.l,
            "eta": self.eta,
            "algorithm": self.algorithm,
        }


# PQC Standards from FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (FN-DSA)
PQC_STANDARDS: dict[str, PQCStandard] = {
    "Kyber-512": PQCStandard("Kyber-512", 256, 3329, 2, 0, 3, "Kyber"),
    "Kyber-768": PQCStandard("Kyber-768", 256, 3329, 3, 0, 2, "Kyber"),
    "Kyber-1024": PQCStandard("Kyber-1024", 256, 3329, 4, 0, 2, "Kyber"),
    "Dilithium-2": PQCStandard("Dilithium-2", 256, 8380417, 4, 4, 2, "Dilithium"),
    "Dilithium-3": PQCStandard("Dilithium-3", 256, 8380417, 6, 5, 4, "Dilithium"),
    "Dilithium-5": PQCStandard("Dilithium-5", 256, 8380417, 8, 7, 2, "Dilithium"),
    "Falcon-512": PQCStandard("Falcon-512", 512, 12289, 0, 0, 0, "Falcon"),
    "Falcon-1024": PQCStandard("Falcon-1024", 1024, 12289, 0, 0, 0, "Falcon"),
}


def find_rns_moduli_for_pqc(standard: PQCStandard, num_moduli: int = 4) -> list[RNSModuliSet]:
    """Find RNS moduli sets suitable for a PQC standard.

    The moduli must:
    1. Be pairwise co-prime
    2. Have product > q (the PQC modulus)
    3. Each have p-1 60-smooth for NTT
    4. Support transform length >= n
    """
    # For NTT, we need primes where p-1 has enough factors of 2, 3, 5 to support the transform length
    # Search for primes with sufficient transform capacity
    min_prime_bits = max(16, (standard.n.bit_length() + 2))  # Need enough bits for transform length
    max_prime_bits = min_prime_bits + 8

    # Generate candidate primes with good transform support
    primes_data = generate_60_smooth_primes(
        min_bits=min_prime_bits,
        max_bits=max_prime_bits,
        count=40,
    )

    # Filter primes that support the required transform length
    suitable_primes = []
    for p_data in primes_data:
        p = p_data["prime"]
        params = compute_ntt_parameters(p)
        if params and params.max_transform_length() >= standard.n:
            suitable_primes.append(p)

    if len(suitable_primes) < num_moduli:
        # Try with wider search
        primes_data = generate_60_smooth_primes(
            min_bits=min_prime_bits,
            max_bits=max_prime_bits + 4,
            count=60,
        )
        for p_data in primes_data:
            p = p_data["prime"]
            params = compute_ntt_parameters(p)
            if params and params.max_transform_length() >= standard.n:
                if p not in suitable_primes:
                    suitable_primes.append(p)

    # Find combinations
    valid = []
    combo_count = 0
    max_combos = 2000
    for combo in combinations(suitable_primes, num_moduli):
        combo_count += 1
        if combo_count > max_combos:
            break
        try:
            rns = RNSModuliSet(moduli=combo)
            if rns.dynamic_range > standard.q:
                valid.append(rns)
        except ValueError:
            continue

    # Sort by dynamic range (prefer smaller range that's sufficient)
    valid.sort(key=lambda r: r.dynamic_range)
    return valid[:10]


def analyze_pqc_rns_support() -> dict[str, Any]:
    """Analyze RNS-NTT support for all PQC standards."""
    results = {}
    for name, std in PQC_STANDARDS.items():
        rns_sets = find_rns_moduli_for_pqc(std)
        results[name] = {
            "standard": std.to_dict(),
            "rns_candidates": [r.to_dict() for r in rns_sets[:3]],
            "best_candidate": rns_sets[0].to_dict() if rns_sets else None,
        }
    return results


# ========================================================================
# Benchmarking Utilities
# ========================================================================

def benchmark_ntt_rns(
    rns_ntt: RNSNTT,
    sizes: list[int],
    iterations: int = 10,
    warmup: int = 3,
) -> dict[str, Any]:
    """Benchmark RNS-NTT performance."""
    import time

    results = {}
    for N in sizes:
        if N > rns_ntt.max_transform_length():
            continue

        # Generate test data
        test_data = [random.randint(0, rns_ntt.moduli_set.moduli[0] - 1) for _ in range(N)]

        # Warmup
        for _ in range(warmup):
            rns_ntt.forward_rns(test_data)

        # Benchmark forward
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            rns_ntt.forward_rns(test_data)
            times.append(time.perf_counter() - start)

        # Benchmark inverse (using forward result)
        fwd_result = rns_ntt.forward_rns(test_data)
        inv_times = []
        for _ in range(iterations):
            start = time.perf_counter()
            rns_ntt.inverse_rns(fwd_result)
            inv_times.append(time.perf_counter() - start)

        results[N] = {
            "forward_mean_ms": sum(times) / len(times) * 1000,
            "forward_min_ms": min(times) * 1000,
            "inverse_mean_ms": sum(inv_times) / len(inv_times) * 1000,
            "inverse_min_ms": min(inv_times) * 1000,
            "num_moduli": len(rns_ntt.moduli_set.moduli),
            "total_bits": rns_ntt.moduli_set.total_bits,
        }

    return results


def benchmark_polynomial_multiplication(
    rns_ntt: RNSNTT,
    sizes: list[int],
    iterations: int = 10,
) -> dict[str, Any]:
    """Benchmark polynomial multiplication using RNS-NTT."""
    import time

    results = {}
    for N in sizes:
        if N > rns_ntt.max_transform_length():
            continue

        a = [random.randint(0, rns_ntt.moduli_set.moduli[0] - 1) for _ in range(N)]
        b = [random.randint(0, rns_ntt.moduli_set.moduli[0] - 1) for _ in range(N)]

        # Warmup
        for _ in range(3):
            rns_ntt.multiply_polynomials(a, b)

        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            rns_ntt.multiply_polynomials(a, b)
            times.append(time.perf_counter() - start)

        results[N] = {
            "mean_ms": sum(times) / len(times) * 1000,
            "min_ms": min(times) * 1000,
            "max_ms": max(times) * 1000,
            "ops_per_sec": N / (sum(times) / len(times)) if times else 0,
        }

    return results


# ========================================================================
# Exports
# ========================================================================

__all__ = [
    # Prime generation
    "is_prime",
    "prime_factors",
    "is_60_smooth",
    "generate_60_smooth_primes",
    # RNS
    "RNSModuliSet",
    "generate_rns_moduli_sets",
    "garner_reconstruct",
    "garner_precompute",
    # NTT
    "NTTParameters",
    "find_primitive_root_for_ntt",
    "compute_ntt_parameters",
    "radix_decomposition",
    "MixedRadixNTT",
    # RNS-NTT
    "RNSNTT",
    # PQC
    "PQCStandard",
    "PQC_STANDARDS",
    "find_rns_moduli_for_pqc",
    "analyze_pqc_rns_support",
    # Benchmarks
    "benchmark_ntt_rns",
    "benchmark_polynomial_multiplication",
]