"""Tests for the RNS/NTT module."""

import pytest

from base60lab.rns_ntt import (
    RNSModuliSet,
    RNSNTT,
    NTTParameters,
    MixedRadixNTT,
    PQCStandard,
    PQC_STANDARDS,
    find_primitive_root_for_ntt,
    generate_60_smooth_primes,
    generate_rns_moduli_sets,
    garner_reconstruct,
    is_60_smooth,
    is_prime,
    prime_factors,
)


class TestRNSModuliSet:
    """Tests for Residue Number System."""

    def test_moduli_creation(self):
        moduli = [3, 5, 7, 11, 13]
        rns = RNSModuliSet(moduli)
        assert rns.moduli == moduli
        assert rns.M == 3 * 5 * 7 * 11 * 13

    def test_rns_conversion(self):
        moduli = [3, 5, 7, 11, 13]
        rns = RNSModuliSet(moduli)
        
        x = 12345
        residues = rns.to_rns(x)
        assert len(residues) == len(moduli)
        assert all(0 <= r < m for r, m in zip(residues, moduli))
        
        reconstructed = rns.from_rns(residues)
        assert reconstructed == x

    def test_rns_addition(self):
        moduli = [3, 5, 7, 11, 13]
        rns = RNSModuliSet(moduli)
        
        x = 100
        y = 200
        x_rns = rns.to_rns(x)
        y_rns = rns.to_rns(y)
        
        sum_rns = [(a + b) % m for a, b, m in zip(x_rns, y_rns, moduli)]
        reconstructed = rns.from_rns(sum_rns)
        assert reconstructed == (x + y) % rns.M

    def test_rns_multiplication(self):
        moduli = [3, 5, 7, 11, 13]
        rns = RNSModuliSet(moduli)
        
        x = 10
        y = 20
        x_rns = rns.to_rns(x)
        y_rns = rns.to_rns(y)
        
        prod_rns = [(a * b) % m for a, b, m in zip(x_rns, y_rns, moduli)]
        reconstructed = rns.from_rns(prod_rns)
        assert reconstructed == (x * y) % rns.M


class TestRNSNTT:
    """Tests for RNS NTT."""

    def test_ntt_creation(self):
        moduli = [17, 97]  # NTT-friendly primes
        params = NTTParameters(moduli=moduli, log2n=4)
        ntt = RNSNTT(params)
        assert ntt.params.moduli == moduli

    def test_ntt_forward_inverse(self):
        """Test forward and inverse NTT."""
        moduli = [17, 97]
        params = NTTParameters(moduli=moduli, log2n=4)
        ntt = RNSNTT(params)
        
        signal = [1, 2, 3, 4, 5, 6, 7, 8] + [0] * 8
        
        transformed = ntt.forward(signal[:16])
        reconstructed = ntt.inverse(transformed)
        
        # Should match original
        for i in range(16):
            for m_idx, m in enumerate(moduli):
                assert reconstructed[m_idx][i] % m == signal[i] % m

    def test_ntt_convolution(self):
        """Test convolution via NTT."""
        moduli = [17, 97]
        params = NTTParameters(moduli=moduli, log2n=4)
        ntt = RNSNTT(params)
        
        a = [1, 2, 3, 4] + [0] * 12
        b = [4, 3, 2, 1] + [0] * 12
        
        a_ntt = ntt.forward(a)
        b_ntt = ntt.forward(b)
        
        c_ntt = [(x * y) % m for (x, m), (y, _) in zip(zip(a_ntt, moduli), zip(b_ntt, moduli))]
        c = ntt.inverse(c_ntt)
        
        # Verify against direct convolution
        direct = [0] * 16
        for i in range(4):
            for j in range(4):
                direct[i + j] = (direct[i + j] + a[i] * b[j]) % moduli[0]
        
        for i in range(16):
            assert c[0][i] % moduli[0] == direct[i] % moduli[0]


class Test60SmoothModuli:
    """Tests for 60-smooth moduli generation."""

    def test_generate_moduli(self):
        moduli = generate_60_smooth_primes(min_prime=1000, max_prime=10000, count=10)
        
        assert len(moduli) == 10
        for p in moduli:
            assert p >= 1000
            assert p <= 10000
            assert is_prime(p)
            factors = prime_factors(p - 1)
            for f in factors:
                assert f in [2, 3, 5]

    def test_is_60_smooth(self):
        assert is_60_smooth(60)
        assert is_60_smooth(180)
        assert is_60_smooth(2**10 * 3**5 * 5**3)
        assert not is_60_smooth(7)
        assert not is_60_smooth(11)

    def test_generate_rns_moduli_sets(self):
        sets = generate_rns_moduli_sets(min_prime=1000, max_prime=10000, count=5, num_moduli=3)
        assert len(sets) >= 1
        for s in sets:
            assert len(s) == 3
            for p in s:
                assert is_prime(p)
                assert is_60_smooth(p - 1)


class TestCRT:
    """Tests for Chinese Remainder Theorem reconstruction."""

    def test_garner_reconstruct(self):
        residues = [2, 3, 2]
        moduli = [3, 5, 7]
        result = garner_reconstruct(residues, moduli)
        assert result == 23

    def test_garner_reconstruct_large(self):
        residues = [123, 456, 789, 1011]
        moduli = [1009, 1013, 1019, 1021]
        result = garner_reconstruct(residues, moduli)
        for r, m in zip(residues, moduli):
            assert result % m == r


class TestPQCStandards:
    """Tests for PQC standard parameters."""

    def test_pqc_standards_defined(self):
        for std in PQCStandard:
            assert std in PQC_STANDARDS
            params = PQC_STANDARDS[std]
            assert 'n' in params
            assert 'q' in params
            assert 'eta' in params

    def test_analyze_pqc_rns_support(self):
        from base60lab.rns_ntt import analyze_pqc_rns_support
        results = {}
        for std in PQCStandard:
            results[std] = analyze_pqc_rns_support(std)
            assert 'rns_friendly' in results[std]
            assert 'moduli_count' in results[std]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])