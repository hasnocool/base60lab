"""Cyclic/modular arithmetic mod 12 and mod 60 using exact integer/rational arithmetic.

This module provides modular arithmetic operations distinct from base representation.
Modular arithmetic ≠ base notation: in mod 12, 10 means ten; in base-12, "10" means twelve.
"""

from __future__ import annotations

from math import gcd
from typing import List


class ModularError(ValueError):
    """Raised for invalid modular arithmetic operations (e.g., non-invertible elements)."""
    pass


def _validate_modulus(modulus: int) -> None:
    """Validate that modulus is a positive integer."""
    if not isinstance(modulus, int):
        raise ModularError(f"modulus must be an integer, got {type(modulus).__name__}")
    if modulus <= 0:
        raise ModularError(f"modulus must be positive, got {modulus}")


def _normalize(a: int, modulus: int) -> int:
    """Normalize integer to canonical representative in [0, modulus)."""
    return a % modulus


def mod_add(a: int, b: int, modulus: int) -> int:
    """Add a and b modulo modulus."""
    _validate_modulus(modulus)
    return (_normalize(a, modulus) + _normalize(b, modulus)) % modulus


def mod_sub(a: int, b: int, modulus: int) -> int:
    """Subtract b from a modulo modulus."""
    _validate_modulus(modulus)
    return (_normalize(a, modulus) - _normalize(b, modulus)) % modulus


def mod_mul(a: int, b: int, modulus: int) -> int:
    """Multiply a and b modulo modulus."""
    _validate_modulus(modulus)
    return (_normalize(a, modulus) * _normalize(b, modulus)) % modulus


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """Compute base^exponent modulo modulus using fast exponentiation."""
    _validate_modulus(modulus)
    if exponent < 0:
        # Negative exponent: compute modular inverse first
        inv = mod_inv(base, modulus)
        return mod_pow(inv, -exponent, modulus)
    base = _normalize(base, modulus)
    result = 1 % modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result


def _extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm: returns (gcd, x, y) such that a*x + b*y = gcd."""
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = _extended_gcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def mod_inv(a: int, modulus: int) -> int:
    """Compute modular inverse of a modulo modulus.
    
    Raises ModularError if a is not invertible (not a unit).
    """
    _validate_modulus(modulus)
    a = _normalize(a, modulus)
    if a == 0:
        raise ModularError(f"{a} has no modular inverse modulo {modulus}")
    g, x, _ = _extended_gcd(a, modulus)
    if g != 1:
        raise ModularError(f"{a} has no modular inverse modulo {modulus} (gcd = {g})")
    return x % modulus


def mod_div(a: int, b: int, modulus: int) -> int:
    """Divide a by b modulo modulus (a * b^{-1} mod modulus)."""
    _validate_modulus(modulus)
    b_inv = mod_inv(b, modulus)
    return mod_mul(a, b_inv, modulus)


def is_unit(a: int, modulus: int) -> bool:
    """Return True if a is a unit (invertible) modulo modulus."""
    _validate_modulus(modulus)
    a = _normalize(a, modulus)
    if a == 0:
        return False
    return gcd(a, modulus) == 1


def units(modulus: int) -> List[int]:
    """Return all units (invertible elements) modulo modulus in ascending order."""
    _validate_modulus(modulus)
    return [a for a in range(modulus) if is_unit(a, modulus)]


def zero_divisors(modulus: int) -> List[int]:
    """Return all zero divisors modulo modulus in ascending order.
    
    Zero divisors are elements a (including 0) such that there exists
    non-zero b with a * b ≡ 0 (mod modulus).
    """
    _validate_modulus(modulus)
    if modulus == 1:
        return [0]
    result = []
    for a in range(modulus):
        if a == 0:
            result.append(a)
        else:
            # Check if a shares any factor with modulus
            if gcd(a, modulus) > 1:
                result.append(a)
    return result


def multiplication_table(modulus: int) -> List[List[int]]:
    """Generate the full multiplication table modulo modulus."""
    _validate_modulus(modulus)
    table = []
    for i in range(modulus):
        row = []
        for j in range(modulus):
            row.append(mod_mul(i, j, modulus))
        table.append(row)
    return table


__all__ = [
    "ModularError",
    "mod_add",
    "mod_sub",
    "mod_mul",
    "mod_pow",
    "mod_inv",
    "mod_div",
    "is_unit",
    "units",
    "zero_divisors",
    "multiplication_table",
]