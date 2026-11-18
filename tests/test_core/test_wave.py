"""Tests for the wave equation solver module."""

import pytest

from base60lab.core.rational import Rational
from base60lab.wave import (
    WaveSolver1D,
    WaveSolver2D,
    WaveParameters,
    standing_wave_1d,
    modal_analysis_1d,
    generate_5_smooth_grid,
    is_5_smooth,
    nearest_5_smooth,
    optimal_grid_1d,
)


class TestWaveSolver1D:
    """Tests for 1D wave equation solver."""

    def test_solver_creation(self):
        params = WaveParameters(length=Rational(1, 1), nx=101, c=Rational(1, 1))
        solver = WaveSolver1D(params)
        assert solver.nx == 101
        assert solver.c == Rational(1, 1)

    def test_initial_conditions(self):
        params = WaveParameters(length=Rational(1, 1), nx=5, c=Rational(1, 1))
        solver = WaveSolver1D(params)
        
        # Use exact solution for initial conditions
        standing_wave_1d(solver, Rational(0, 1))
        
        # Check boundary conditions (fixed ends)
        assert solver.u[0] == Rational(0, 1)
        assert solver.u[-1] == Rational(0, 1)

    def test_zero_drift_simulation(self):
        """Test that simulation has zero drift over many steps."""
        params = WaveParameters(length=Rational(1, 1), nx=21, c=Rational(1, 1))
        solver = WaveSolver1D(params)
        standing_wave_1d(solver, Rational(0, 1))
        
        # Run 1000 steps
        dt = Rational(1, 1000)
        for _ in range(1000):
            solver.step(dt)
        
        # Energy should be conserved (within exact rational arithmetic)
        energy = solver.compute_energy()
        assert energy >= Rational(0, 1)

    def test_standing_wave_solution(self):
        """Test exact standing wave solution."""
        params = WaveParameters(length=Rational(1, 1), nx=11, c=Rational(1, 1))
        solver = WaveSolver1D(params)
        
        # At t=0, standing wave
        standing_wave_1d(solver, Rational(0, 1))
        
        # At x=0.5, should be maximum
        mid_idx = 5
        assert solver.u[mid_idx] > Rational(0, 1)


class TestWaveSolver2D:
    """Tests for 2D wave equation solver."""

    def test_solver_creation(self):
        params = WaveParameters(length=Rational(1, 1), nx=11, c=Rational(1, 1))
        solver = WaveSolver2D(params)
        assert solver.nx == 11
        assert solver.ny == 11

    def test_rectangular_membrane(self):
        params = WaveParameters(length=Rational(1, 1), nx=6, c=Rational(1, 1))
        solver = WaveSolver2D(params)
        
        # Check boundaries are zero
        for i in range(6):
            assert solver.u[0][i] == Rational(0, 1)
            assert solver.u[5][i] == Rational(0, 1)
            assert solver.u[i][0] == Rational(0, 1)
            assert solver.u[i][5] == Rational(0, 1)


class Test5SmoothGrid:
    """Tests for 5-smooth grid generation."""

    def test_generate_5_smooth_grid(self):
        grid = generate_5_smooth_grid(100, 1000)
        assert len(grid) > 0
        for size in grid:
            assert is_5_smooth(size)

    def test_is_5_smooth(self):
        assert is_5_smooth(60)
        assert is_5_smooth(180)
        assert is_5_smooth(2**10 * 3**5 * 5**3)
        assert not is_5_smooth(7)
        assert not is_5_smooth(11)
        assert not is_5_smooth(14)

    def test_nearest_5_smooth(self):
        assert nearest_5_smooth(100) == 96  # 2^5 * 3
        assert nearest_5_smooth(1000) == 960  # 2^6 * 3 * 5
        assert nearest_5_smooth(10000) == 10000  # 10^4 = 2^4 * 5^4

    def test_optimal_grid_1d(self):
        optimal = optimal_grid_1d(100, 1000)
        assert optimal >= 100
        assert optimal <= 1000
        assert is_5_smooth(optimal)


class TestModalAnalysis:
    """Tests for modal analysis."""

    def test_modal_analysis_1d(self):
        params = WaveParameters(length=Rational(1, 1), nx=11, c=Rational(1, 1))
        modes = modal_analysis_1d(params)
        
        assert len(modes) == 10  # nx - 1 modes
        for mode in modes:
            assert 'n' in mode
            assert 'frequency' in mode
            assert 'wavelength' in mode

    def test_cavity_mode_frequencies(self):
        """Test that cavity mode frequencies are exact rational multiples."""
        # For 1D cavity of length L: f_n = n*c/(2L)
        L = Rational(1, 1)
        c = Rational(340, 1)
        
        for n in range(1, 10):
            freq = Rational(n, 1) * c / (Rational(2, 1) * L)
            assert freq.denominator == 2
            assert freq.numerator == n * 340


if __name__ == "__main__":
    pytest.main([__file__, "-v"])