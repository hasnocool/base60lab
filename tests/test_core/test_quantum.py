"""Tests for the quantum module."""

import pytest
from fractions import Fraction
import math

from base60lab.core.rational import Rational
from base60lab.quantum import Qudit, QuantumCircuit, mixed_radix_qft, StabilizerCode, _radix_decomposition


class TestQudit:
    """Tests for Qudit class."""

    def test_qudit_creation(self):
        q = Qudit(12)
        assert q.d == 12
        assert q.state is not None

    def test_qudit_state_vector(self):
        q = Qudit(12)
        state = q.state
        assert len(state) == 12
        assert state[0] == Rational(1, 1)
        for i in range(1, 12):
            assert state[i] == Rational(0, 1)

    def test_qudit_base60(self):
        q = Qudit(60)
        assert q.d == 60
        state = q.state
        assert len(state) == 60
        assert state[0] == Rational(1, 1)

    def test_qudit_invalid_dimension(self):
        with pytest.raises(ValueError):
            Qudit(0)
        with pytest.raises(ValueError):
            Qudit(-1)


class TestQuantumCircuit:
    """Tests for QuantumCircuit class."""

    def test_circuit_creation(self):
        q = Qudit(12)
        circuit = QuantumCircuit([q])
        assert len(circuit.qudits) == 1

    def test_hadamard_gate(self):
        q = Qudit(12)
        circuit = QuantumCircuit([q])
        circuit.h(0)
        state = q.state
        for amplitude in state:
            assert amplitude != Rational(0, 1)

    def test_measure(self):
        q = Qudit(12)
        circuit = QuantumCircuit([q])
        result = circuit.measure(0)
        assert 0 <= result < 12


class TestQFT:
    """Tests for Quantum Fourier Transform."""

    def test_qft_12(self):
        q = Qudit(12)
        circuit = QuantumCircuit([q])
        circuit.h(0)
        mixed_radix_qft(circuit, [0], 12)
        state = q.state
        for amp in state:
            mag = abs(amp)
            assert abs(mag - 1/12**0.5) < 0.01

    def test_qft_60(self):
        q = Qudit(60)
        circuit = QuantumCircuit([q])
        circuit.h(0)
        mixed_radix_qft(circuit, [0], 60)
        state = q.state
        assert len(state) == 60

    def test_radix_decomposition(self):
        factors = _radix_decomposition(60)
        assert factors == [4, 3, 5]

    def test_radix_decomposition_12(self):
        factors = _radix_decomposition(12)
        assert factors == [4, 3]


class TestStabilizerCode:
    """Tests for StabilizerCode framework."""

    def test_stabilizer_creation(self):
        code = StabilizerCode(60)
        assert code.d == 60

    def test_syndrome_extraction(self):
        code = StabilizerCode(60)
        q = Qudit(60)
        circuit = QuantumCircuit([q])
        circuit.h(0)
        syndrome = code.extract_syndrome(circuit, 0)
        assert isinstance(syndrome, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])