"""Tests for modular/cyclic arithmetic mod 12 and mod 60."""

from base60lab.modular import (
    mod_add,
    mod_sub,
    mod_mul,
    mod_pow,
    mod_inv,
    mod_div,
    multiplication_table,
    is_unit,
    units,
    zero_divisors,
    ModularError,
)


class TestModularArithmetic:
    """Core modular arithmetic operations."""

    def test_mod_add_mod12(self):
        assert mod_add(7, 5, 12) == 0
        assert mod_add(11, 1, 12) == 0
        assert mod_add(6, 6, 12) == 0
        assert mod_add(0, 0, 12) == 0

    def test_mod_add_mod60(self):
        assert mod_add(30, 30, 60) == 0
        assert mod_add(59, 1, 60) == 0
        assert mod_add(0, 0, 60) == 0

    def test_mod_sub_mod12(self):
        assert mod_sub(0, 1, 12) == 11
        assert mod_sub(5, 7, 12) == 10
        assert mod_sub(0, 0, 12) == 0

    def test_mod_sub_mod60(self):
        assert mod_sub(0, 1, 60) == 59
        assert mod_sub(30, 45, 60) == 45

    def test_mod_mul_mod12(self):
        assert mod_mul(7, 5, 12) == 11
        assert mod_mul(6, 2, 12) == 0
        assert mod_mul(3, 4, 12) == 0
        assert mod_mul(11, 11, 12) == 1
        assert mod_mul(0, 5, 12) == 0

    def test_mod_mul_mod60(self):
        assert mod_mul(7, 5, 60) == 35
        assert mod_mul(12, 5, 60) == 0
        assert mod_mul(15, 4, 60) == 0
        assert mod_mul(59, 59, 60) == 1

    def test_mod_pow_mod12(self):
        assert mod_pow(2, 3, 12) == 8
        assert mod_pow(5, 2, 12) == 1
        assert mod_pow(11, 2, 12) == 1
        assert mod_pow(7, 0, 12) == 1

    def test_mod_pow_mod60(self):
        assert mod_pow(2, 5, 60) == 32
        assert mod_pow(7, 2, 60) == 49
        assert mod_pow(59, 2, 60) == 1


class TestModularInverses:
    """Modular inverse and division operations."""

    def test_mod_inv_mod12(self):
        # Units mod 12: 1, 5, 7, 11
        assert mod_inv(1, 12) == 1
        assert mod_inv(5, 12) == 5
        assert mod_inv(7, 12) == 7
        assert mod_inv(11, 12) == 11

    def test_mod_inv_mod60(self):
        # Some units mod 60: 1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59
        assert mod_inv(1, 60) == 1
        assert mod_inv(7, 60) == 43  # 7 * 43 = 301 ≡ 1 (mod 60)
        assert mod_inv(11, 60) == 11  # 11 * 11 = 121 ≡ 1 (mod 60)
        assert mod_inv(59, 60) == 59  # 59 * 59 = 3481 ≡ 1 (mod 60)

    def test_mod_inv_non_unit_raises(self):
        # Non-units mod 12: 0, 2, 3, 4, 6, 8, 9, 10
        for a in [0, 2, 3, 4, 6, 8, 9, 10]:
            try:
                mod_inv(a, 12)
                assert False, f"should have raised for {a} mod 12"
            except ModularError:
                pass

        # Non-units mod 60: 0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 50, 51, 52, 54, 55, 56, 57, 58
        for a in [0, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30]:
            try:
                mod_inv(a, 60)
                assert False, f"should have raised for {a} mod 60"
            except ModularError:
                pass

    def test_mod_div_mod12(self):
        assert mod_div(1, 5, 12) == 5  # 1 * 5 = 5 ≡ 5 (mod 12)
        assert mod_div(7, 7, 12) == 1  # 7 * 7 = 49 ≡ 1 (mod 12)
        assert mod_div(11, 11, 12) == 1

    def test_mod_div_mod60(self):
        assert mod_div(1, 7, 60) == 43  # 1 * 43 = 43 ≡ 43 (mod 60)
        assert mod_div(7, 7, 60) == 1

    def test_mod_div_non_unit_raises(self):
        try:
            mod_div(1, 2, 12)
            assert False, "should have raised for non-unit divisor"
        except ModularError:
            pass


class TestMultiplicationTables:
    """Multiplication table generation."""

    def test_multiplication_table_mod12(self):
        table = multiplication_table(12)
        assert len(table) == 12
        assert len(table[0]) == 12
        # Check symmetry
        for i in range(12):
            for j in range(12):
                assert table[i][j] == table[j][i]
        # Check specific values
        assert table[7][5] == 11
        assert table[6][2] == 0
        assert table[11][11] == 1

    def test_multiplication_table_mod60(self):
        table = multiplication_table(60)
        assert len(table) == 60
        assert len(table[0]) == 60
        # Check symmetry
        for i in range(60):
            for j in range(60):
                assert table[i][j] == table[j][i]
        assert table[7][5] == 35
        assert table[59][59] == 1


class TestUnitsAndZeroDivisors:
    """Units and zero divisors."""

    def test_is_unit_mod12(self):
        assert is_unit(1, 12) is True
        assert is_unit(5, 12) is True
        assert is_unit(7, 12) is True
        assert is_unit(11, 12) is True
        assert is_unit(0, 12) is False
        assert is_unit(2, 12) is False
        assert is_unit(3, 12) is False
        assert is_unit(4, 12) is False
        assert is_unit(6, 12) is False
        assert is_unit(8, 12) is False
        assert is_unit(9, 12) is False
        assert is_unit(10, 12) is False

    def test_is_unit_mod60(self):
        assert is_unit(1, 60) is True
        assert is_unit(7, 60) is True
        assert is_unit(11, 60) is True
        assert is_unit(59, 60) is True
        assert is_unit(0, 60) is False
        assert is_unit(2, 60) is False
        assert is_unit(3, 60) is False
        assert is_unit(4, 60) is False
        assert is_unit(5, 60) is False
        assert is_unit(6, 60) is False

    def test_units_mod12(self):
        u = units(12)
        assert u == [1, 5, 7, 11]

    def test_units_mod60(self):
        u = units(60)
        expected = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59]
        assert u == expected

    def test_zero_divisors_mod12(self):
        zd = zero_divisors(12)
        expected = [0, 2, 3, 4, 6, 8, 9, 10]
        assert zd == expected

    def test_zero_divisors_mod60(self):
        zd = zero_divisors(60)
        # Non-units excluding 0? Or including 0?
        # Zero divisors are non-zero elements a where exists b≠0 such that a*b≡0
        assert 0 in zd
        assert 2 in zd
        assert 3 in zd
        assert 4 in zd
        assert 5 in zd
        assert 6 in zd
        assert 10 in zd
        assert 12 in zd
        assert 15 in zd
        assert 20 in zd
        assert 30 in zd


class TestErrorHandling:
    """Error handling for malformed input."""

    def test_modulus_zero_raises(self):
        # Functions with signature (a, b, modulus)
        for func in [mod_add, mod_sub, mod_mul, mod_pow, mod_div]:
            try:
                func(1, 1, 0)
                assert False, f"{func.__name__} should have raised for modulus 0"
            except ModularError:
                pass
        # mod_inv has signature (a, modulus)
        try:
            mod_inv(1, 0)
            assert False, "mod_inv should have raised for modulus 0"
        except ModularError:
                pass

    def test_negative_modulus_raises(self):
        # Functions with signature (a, b, modulus)
        for func in [mod_add, mod_sub, mod_mul, mod_pow, mod_div]:
            try:
                func(1, 1, -12)
                assert False, f"{func.__name__} should have raised for negative modulus"
            except ModularError:
                pass
        # mod_inv has signature (a, modulus)
        try:
            mod_inv(1, -12)
            assert False, "mod_inv should have raised for negative modulus"
        except ModularError:
            pass

        try:
            multiplication_table(-12)
            assert False, "multiplication_table should have raised for negative modulus"
        except ModularError:
            pass

    def test_modulus_one(self):
        # Mod 1: everything is 0
        assert mod_add(0, 0, 1) == 0
        assert mod_mul(0, 0, 1) == 0
        assert mod_pow(0, 0, 1) == 0  # 0^0 conventionally 1, but mod 1 = 0
        table = multiplication_table(1)
        assert table == [[0]]


class TestExactIntegerArithmetic:
    """Verify no floating-point is used internally."""

    def test_large_numbers_exact(self):
        # Large numbers should work exactly
        assert mod_mul(123456789, 987654321, 12) == mod_mul(123456789 % 12, 987654321 % 12, 12)
        assert mod_add(123456789, 987654321, 60) == mod_add(123456789 % 60, 987654321 % 60, 60)

    def test_negative_inputs_normalized(self):
        # Negative inputs should be normalized correctly
        assert mod_add(-1, 0, 12) == 11
        assert mod_sub(0, -1, 12) == 1
        assert mod_mul(-1, -1, 12) == 1
        assert mod_mul(-5, 7, 12) == mod_mul(7, 7, 12)  # -5 ≡ 7 (mod 12)
        assert mod_pow(-1, 2, 12) == 1
        assert mod_inv(-1, 12) == 11  # -1 ≡ 11 (mod 12)


class TestDistinctFromBaseNotation:
    """Verify modular arithmetic is distinct from base representation."""

    def test_modular_not_base12(self):
        # In base-12, "10" means twelve
        # In mod 12, 10 means ten
        # These are fundamentally different
        assert mod_mul(10, 2, 12) == 8  # modular: 10*2=20≡8
        # Base-12 representation would be a different operation entirely

    def test_modular_not_base60(self):
        assert mod_mul(10, 6, 60) == 0  # modular: 10*6=60≡0
        # Base-60 would represent 600 differently