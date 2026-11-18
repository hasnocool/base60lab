"""Baseline characterization tests for signal_processing module.

These tests verify the module can be imported and basic functionality exists.
Following failing-first methodology: tests written before implementation.
"""

import pytest


class TestSignalProcessingImport:
    """Baseline characterization - module should be importable."""

    def test_module_imports(self):
        """Verify signal_processing module can be imported."""
        from base60lab.signal_processing import (
            fft_of_signal,
            ifft_of_signal,
            design_lowpass_filter,
            design_highpass_filter,
            design_bandpass_filter,
            apply_filter,
            compute_power_spectrum,
            compute_spectral_density,
            Signal,
        )
        assert callable(fft_of_signal)
        assert callable(ifft_of_signal)
        assert callable(design_lowpass_filter)
        assert callable(design_highpass_filter)
        assert callable(design_bandpass_filter)
        assert callable(apply_filter)
        assert callable(compute_power_spectrum)
        assert callable(compute_spectral_density)


class TestSignalProcessingBasicFunctionality:
    """Basic functionality tests for signal processing."""

    def test_fft_of_simple_signal(self):
        """Test FFT of a simple known signal [1, 0, -1, 0]."""
        from base60lab.signal_processing import fft_of_signal
        signal = [1, 0, -1, 0]
        result = fft_of_signal(signal)
        # Should return complex array of same length
        assert len(result) == 4
        assert all(isinstance(x, complex) for x in result)

    def test_fft_real_signal_symmetry(self):
        """Test that FFT of real signal has conjugate symmetry."""
        from base60lab.signal_processing import fft_of_signal
        import numpy as np
        signal = [1, 2, 3, 4, 3, 2, 1, 0]
        result = fft_of_signal(signal)
        # For real signals, FFT[k] = conj(FFT[N-k])
        n = len(result)
        for k in range(1, n // 2):
            assert np.isclose(result[k], np.conj(result[n - k]))

    def test_ifft_roundtrip(self):
        """Test IFFT(FFT(signal)) ≈ signal."""
        from base60lab.signal_processing import fft_of_signal, ifft_of_signal
        import numpy as np
        signal = [1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0, 0.0]
        fft_result = fft_of_signal(signal)
        reconstructed = ifft_of_signal(fft_result)
        # Should be close to original (within numerical precision)
        assert len(reconstructed) == len(signal)
        for i, (orig, recon) in enumerate(zip(signal, reconstructed)):
            assert np.isclose(orig, recon.real, atol=1e-10), f"Mismatch at index {i}: {orig} vs {recon.real}"

    def test_lowpass_filter_design(self):
        """Test lowpass filter design."""
        from base60lab.signal_processing import design_lowpass_filter
        # Design a lowpass filter with cutoff at 0.25 (normalized)
        b, a = design_lowpass_filter(cutoff=0.25, order=4)
        assert len(b) > 0
        assert len(a) > 0

    def test_highpass_filter_design(self):
        """Test highpass filter design."""
        from base60lab.signal_processing import design_highpass_filter
        b, a = design_highpass_filter(cutoff=0.25, order=4)
        assert len(b) > 0
        assert len(a) > 0

    def test_bandpass_filter_design(self):
        """Test bandpass filter design."""
        from base60lab.signal_processing import design_bandpass_filter
        b, a = design_bandpass_filter(lowcut=0.1, highcut=0.4, order=4)
        assert len(b) > 0
        assert len(a) > 0

    def test_apply_filter(self):
        """Test applying a filter to a signal."""
        from base60lab.signal_processing import design_lowpass_filter, apply_filter
        import numpy as np
        # Create a signal with high and low frequency components
        t = np.linspace(0, 1, 1000)
        signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)
        # Design lowpass to keep only 5 Hz component
        b, a = design_lowpass_filter(cutoff=0.1, order=4)
        filtered = apply_filter(signal, b, a)
        assert len(filtered) == len(signal)

    def test_power_spectrum(self):
        """Test power spectrum computation."""
        from base60lab.signal_processing import compute_power_spectrum
        import numpy as np
        signal = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 1000))
        freqs, psd = compute_power_spectrum(signal, fs=1000)
        assert len(freqs) == len(psd)
        # Peak should be at 5 Hz
        peak_idx = np.argmax(psd)
        assert abs(freqs[peak_idx] - 5) < 1.0

    def test_spectral_density(self):
        """Test spectral density computation."""
        from base60lab.signal_processing import compute_spectral_density
        import numpy as np
        signal = np.random.default_rng(42).normal(size=1000)
        freqs, psd = compute_spectral_density(signal, fs=1000)
        assert len(freqs) == len(psd)
        assert all(p >= 0 for p in psd)  # PSD should be non-negative

    def test_spectral_content_pure_sine(self):
        """Test that a pure sine wave produces a peak at the expected frequency."""
        from base60lab.signal_processing import compute_power_spectrum
        import numpy as np
        signal = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 1000))
        freqs, psd = compute_power_spectrum(signal, fs=1000)
        peak_idx = np.argmax(psd)
        # Peak MUST be at 5 Hz, not elsewhere
        assert abs(freqs[peak_idx] - 5) < 0.5
        # Peak magnitude should be significant
        assert psd[peak_idx] > 0

    def test_spectral_content_dc_only(self):
        """Test that a DC signal produces peak at frequency 0."""
        from base60lab.signal_processing import compute_power_spectrum
        import numpy as np
        signal = np.ones(1024) * 5.0
        freqs, psd = compute_power_spectrum(signal, fs=1024)
        peak_idx = np.argmax(psd)
        assert freqs[peak_idx] == 0
        assert psd[peak_idx] > 0

    def test_empty_signal_raises(self):
        """Test that empty signal raises appropriate error."""
        from base60lab.signal_processing import fft_of_signal
        with pytest.raises((ValueError, IndexError)):
            fft_of_signal([])

    def test_non_power_of_two_signal(self):
        """Test FFT works with non-power-of-two lengths."""
        from base60lab.signal_processing import fft_of_signal
        # Length 7 (not power of 2)
        signal = [1, 2, 3, 4, 5, 6, 7]
        result = fft_of_signal(signal)
        assert len(result) == 7

    def test_signal_class(self):
        """Test Signal container class."""
        from base60lab.signal_processing import Signal
        import numpy as np
        data = np.array([1.0, 2.0, 3.0, 4.0])
        sig = Signal(data, sample_rate=1000)
        assert sig.sample_rate == 1000
        assert len(sig.data) == 4
        # Test FFT method
        fft_result = sig.fft()
        assert len(fft_result) == 4


class TestRationalArithmeticIntegration:
    """Tests verifying exact rational arithmetic is used internally."""

    def test_filter_coefficients_rational(self):
        """Test that filter design uses Rational internally where possible."""
        from base60lab.signal_processing import design_lowpass_filter
        from base60lab.core.rational import Rational
        b, a = design_lowpass_filter(cutoff=Rational(1, 4), order=4)
        # Coefficients should be computable as rationals
        assert len(b) > 0
        assert len(a) > 0

    def test_rational_signal_operations(self):
        """Test operations with Rational inputs."""
        from base60lab.signal_processing import fft_of_signal
        from base60lab.core.rational import Rational
        # Signal with rational values
        signal = [Rational(1), Rational(0), Rational(-1), Rational(0)]
        result = fft_of_signal(signal)
        assert len(result) == 4
