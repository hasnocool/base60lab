"""Tests for FFT benchmarks module.

Tests cover:
- Baseline characterization (ImportError when module doesn't exist)
- Failing-first proof (tests written before implementation)
- Smooth number classification
- Size generation
- Single FFT benchmark
- Full benchmark suite
- Adversarial inputs (zero, negative sizes)
- Deterministic behavior (fixed seed)
- Output data structure validation
"""

from __future__ import annotations

import pytest
import numpy as np

# Test that the module can be imported
try:
    from base60lab.fft_benchmarks import (
        SizeCategory,
        BenchmarkResult,
        BenchmarkSummary,
        is_smooth,
        is_powers_of_2,
        is_5_smooth,
        is_12_smooth,
        is_60_smooth,
        is_poorly_factored,
        generate_sizes,
        benchmark_fft,
        run_benchmarks,
        print_benchmark_results,
    )
    MODULE_EXISTS = True
except ImportError:
    MODULE_EXISTS = False


class TestModuleImport:
    """Baseline characterization: verify module import behavior."""

    def test_module_exists(self):
        """Module should be importable after implementation."""
        # This test will fail before implementation, pass after
        assert MODULE_EXISTS, "fft_benchmarks module should be importable"

    def test_all_exports_present(self):
        """All expected exports should be present."""
        assert MODULE_EXISTS
        from base60lab.fft_benchmarks import __all__

        expected = [
            "SizeCategory",
            "BenchmarkResult",
            "BenchmarkSummary",
            "is_smooth",
            "is_powers_of_2",
            "is_5_smooth",
            "is_12_smooth",
            "is_60_smooth",
            "is_poorly_factored",
            "generate_sizes",
            "benchmark_fft",
            "run_benchmarks",
            "print_benchmark_results",
        ]
        for exp in expected:
            assert exp in __all__, f"Missing export: {exp}"


class TestSmoothNumberClassification:
    """Test smooth number classification functions."""

    def test_is_powers_of_2(self):
        """Test power of 2 detection."""
        assert is_powers_of_2(1) is True
        assert is_powers_of_2(2) is True
        assert is_powers_of_2(4) is True
        assert is_powers_of_2(8) is True
        assert is_powers_of_2(16) is True
        assert is_powers_of_2(32) is True
        assert is_powers_of_2(64) is True
        assert is_powers_of_2(128) is True
        assert is_powers_of_2(256) is True

        # Not powers of 2
        assert is_powers_of_2(3) is False
        assert is_powers_of_2(6) is False
        assert is_powers_of_2(12) is False
        assert is_powers_of_2(24) is False
        assert is_powers_of_2(0) is False
        assert is_powers_of_2(-1) is False

    def test_is_5_smooth(self):
        """Test 5-smooth (regular numbers) detection."""
        # 5-smooth: only prime factors 2, 3, 5
        assert is_5_smooth(1) is True
        assert is_5_smooth(2) is True
        assert is_5_smooth(3) is True
        assert is_5_smooth(4) is True
        assert is_5_smooth(5) is True
        assert is_5_smooth(6) is True  # 2*3
        assert is_5_smooth(8) is True
        assert is_5_smooth(9) is True  # 3*3
        assert is_5_smooth(10) is True  # 2*5
        assert is_5_smooth(12) is True  # 2*2*3
        assert is_5_smooth(15) is True  # 3*5
        assert is_5_smooth(16) is True
        assert is_5_smooth(18) is True  # 2*3*3
        assert is_5_smooth(20) is True  # 2*2*5
        assert is_5_smooth(24) is True  # 2*2*2*3
        assert is_5_smooth(25) is True  # 5*5
        assert is_5_smooth(27) is True  # 3*3*3
        assert is_5_smooth(30) is True  # 2*3*5
        assert is_5_smooth(36) is True  # 2*2*3*3
        assert is_5_smooth(40) is True  # 2*2*2*5
        assert is_5_smooth(45) is True  # 3*3*5
        assert is_5_smooth(48) is True  # 2*2*2*2*3
        assert is_5_smooth(50) is True  # 2*5*5
        assert is_5_smooth(54) is True  # 2*3*3*3
        assert is_5_smooth(60) is True  # 2*2*3*5
        assert is_5_smooth(64) is True
        assert is_5_smooth(72) is True  # 2*2*2*3*3
        assert is_5_smooth(75) is True  # 3*5*5
        assert is_5_smooth(80) is True
        assert is_5_smooth(81) is True  # 3^4
        assert is_5_smooth(90) is True  # 2*3*3*5
        assert is_5_smooth(96) is True
        assert is_5_smooth(100) is True

        # Not 5-smooth (have prime factor > 5)
        assert is_5_smooth(7) is False
        assert is_5_smooth(11) is False
        assert is_5_smooth(13) is False
        assert is_5_smooth(14) is False  # 2*7
        assert is_5_smooth(21) is False  # 3*7
        assert is_5_smooth(22) is False  # 2*11
        assert is_5_smooth(26) is False  # 2*13
        assert is_5_smooth(28) is False  # 2*2*7
        assert is_5_smooth(35) is False  # 5*7
        assert is_5_smooth(49) is False  # 7*7

    def test_is_12_smooth(self):
        """Test 12-smooth detection (primes <= 11)."""
        # Includes 5-smooth plus factors 7, 11
        assert is_12_smooth(7) is True
        assert is_12_smooth(11) is True
        assert is_12_smooth(14) is True  # 2*7
        assert is_12_smooth(21) is True  # 3*7
        assert is_12_smooth(22) is True  # 2*11
        assert is_12_smooth(33) is True  # 3*11
        assert is_12_smooth(35) is True  # 5*7
        assert is_12_smooth(44) is True  # 2*2*11
        assert is_12_smooth(49) is True  # 7*7
        assert is_12_smooth(55) is True  # 5*11
        assert is_12_smooth(63) is True  # 3*3*7
        assert is_12_smooth(77) is True  # 7*11
        assert is_12_smooth(99) is True  # 3*3*11

        # Not 12-smooth (prime factor > 11)
        assert is_12_smooth(13) is False
        assert is_12_smooth(17) is False
        assert is_12_smooth(26) is False  # 2*13
        assert is_12_smooth(143) is False  # 11*13

    def test_is_60_smooth(self):
        """Test 60-smooth detection (primes <= 59)."""
        # Includes all primes up to 59
        assert is_60_smooth(13) is True
        assert is_60_smooth(17) is True
        assert is_60_smooth(19) is True
        assert is_60_smooth(23) is True
        assert is_60_smooth(29) is True
        assert is_60_smooth(31) is True
        assert is_60_smooth(37) is True
        assert is_60_smooth(41) is True
        assert is_60_smooth(43) is True
        assert is_60_smooth(47) is True
        assert is_60_smooth(53) is True
        assert is_60_smooth(59) is True
        assert is_60_smooth(13 * 17) is True  # 221
        assert is_60_smooth(59 * 59) is True  # 3481

        # Not 60-smooth (prime factor >= 61)
        assert is_60_smooth(61) is False
        assert is_60_smooth(67) is False
        assert is_60_smooth(61 * 2) is False  # 122

    def test_is_poorly_factored(self):
        """Test poorly factored detection (large prime factor)."""
        # By default, min_large_prime_factor=13
        assert is_poorly_factored(13) is True
        assert is_poorly_factored(17) is True
        assert is_poorly_factored(26) is True  # 2*13
        assert is_poorly_factored(143) is True  # 11*13
        assert is_poorly_factored(221) is True  # 13*17

        # Not poorly factored (all prime factors < 13)
        assert is_poorly_factored(12) is False  # 2*2*3
        assert is_poorly_factored(30) is False  # 2*3*5
        assert is_poorly_factored(60) is False  # 2*2*3*5
        assert is_poorly_factored(72) is False  # 2*2*2*3*3
        assert is_poorly_factored(100) is False  # 2*2*5*5

        # Custom threshold
        assert is_poorly_factored(11, min_large_prime_factor=11) is True
        assert is_poorly_factored(11, min_large_prime_factor=13) is False
    def test_is_poorly_factored_edge_cases(self):
        """Test is_poorly_factored edge cases."""
        # 1 is not poorly factored
        assert is_poorly_factored(1) is False
        # Prime numbers >= 13 are poorly factored
        assert is_poorly_factored(13) is True
        assert is_poorly_factored(17) is True
        # Numbers with only small factors are not poorly factored
        assert is_poorly_factored(16) is False  # 2^4
        assert is_poorly_factored(30) is False  # 2*3*5
        assert is_poorly_factored(60) is False  # 2^2*3*5
        # With custom threshold
        assert is_poorly_factored(11, min_large_prime_factor=13) is False
        assert is_poorly_factored(13, min_large_prime_factor=13) is True
        assert is_poorly_factored(11, min_large_prime_factor=7) is True


class TestComputePrecisionBits:
    """Test _compute_precision_bits function."""

    def test_compute_precision_bits_zero_signal(self):
        """Test _compute_precision_bits when signal_norm is 0 (line 227)."""
        from base60lab.fft_benchmarks import _compute_precision_bits
        # Zero signal should return infinity
        original = np.zeros(10, dtype=np.complex128)
        reconstructed = np.zeros(10, dtype=np.complex128)
        result = _compute_precision_bits(original, reconstructed)
        assert result == float("inf")

    def test_compute_precision_bits_perfect_reconstruction(self):
        """Test _compute_precision_bits with perfect reconstruction."""
        from base60lab.fft_benchmarks import _compute_precision_bits
        original = np.array([1.0, 2.0, 3.0], dtype=np.complex128)
        reconstructed = np.array([1.0, 2.0, 3.0], dtype=np.complex128)
        result = _compute_precision_bits(original, reconstructed)
        assert result == float("inf")

    def test_compute_precision_bits_normal(self):
        """Test _compute_precision_bits with normal inputs."""
        from base60lab.fft_benchmarks import _compute_precision_bits
        original = np.array([1.0, 2.0, 3.0], dtype=np.complex128)
        reconstructed = np.array([1.1, 2.1, 3.1], dtype=np.complex128)
        result = _compute_precision_bits(original, reconstructed)
        assert isinstance(result, float)
        assert result > 0
        assert result != float("inf")


class TestSizeGeneration:
    """Test size generation for each category."""

    def test_generate_powers_of_2(self):
        """Test powers of 2 generation."""
        sizes = generate_sizes("powers_of_2", 8, 16, 4096)
        expected = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
        assert sizes == expected[:8]

    def test_generate_powers_of_2_limited_count(self):
        """Test powers of 2 with limited count."""
        sizes = generate_sizes("powers_of_2", 3, 16, 4096)
        assert sizes == [16, 32, 64]

    def test_generate_5_smooth(self):
        """Test 5-smooth generation (excludes powers of 2)."""
        sizes = generate_sizes("5_smooth", 10, 16, 200)
        # Should not include powers of 2
        for s in sizes:
            assert not is_powers_of_2(s), f"{s} is a power of 2"
            assert is_5_smooth(s), f"{s} is not 5-smooth"
        assert len(sizes) == 10

    def test_generate_12_smooth(self):
        """Test 12-smooth generation (excludes 5-smooth)."""
        sizes = generate_sizes("12_smooth", 10, 16, 200)
        for s in sizes:
            assert is_12_smooth(s), f"{s} is not 12-smooth"
            assert not is_5_smooth(s), f"{s} is 5-smooth (should be excluded)"
        assert len(sizes) == 10

    def test_generate_60_smooth(self):
        """Test 60-smooth generation (excludes 12-smooth)."""
        sizes = generate_sizes("60_smooth", 10, 16, 300)
        for s in sizes:
            assert is_60_smooth(s), f"{s} is not 60-smooth"
            assert not is_12_smooth(s), f"{s} is 12-smooth (should be excluded)"
        assert len(sizes) == 10

    def test_generate_poorly_factored(self):
        """Test poorly factored generation."""
        sizes = generate_sizes("poorly_factored", 10, 16, 300)
        for s in sizes:
            assert is_poorly_factored(s), f"{s} is not poorly factored"
        assert len(sizes) == 10

    def test_generate_deterministic(self):
        """Test that generation is deterministic with same seed."""
        sizes1 = generate_sizes("5_smooth", 10, 16, 200, seed=42)
        sizes2 = generate_sizes("5_smooth", 10, 16, 200, seed=42)
        assert sizes1 == sizes2

        sizes3 = generate_sizes("5_smooth", 10, 16, 200, seed=123)
        assert sizes1 != sizes3  # Different seed should give different results (usually)

    def test_generate_unknown_category(self):
        """Test that unknown category raises ValueError."""
        with pytest.raises(ValueError, match="Unknown category"):
            generate_sizes("unknown_category", 5)
    def test_generate_sizes_filtered_smaller_than_count(self):
        """Test generate_sizes when filtered list is smaller than requested count (line 200)."""
        # For "5_smooth" in narrow range 16-20: 5-smooth numbers are 16, 18, 20
        # But 16 is power of 2, so filtered = [18, 20]
        sizes = generate_sizes("5_smooth", 10, 16, 20, seed=42)
        assert sizes == [18, 20]  # Should return all available, sorted
        assert len(sizes) == 2  # Less than requested count of 10

    def test_generate_sizes_12_smooth_category(self):
        """Test generate_sizes for 12_smooth category."""
        sizes = generate_sizes("12_smooth", 5, 16, 256, seed=42)
        assert len(sizes) > 0
        for s in sizes:
            assert is_12_smooth(s)
            assert not is_5_smooth(s)  # Should exclude 5-smooth

    def test_generate_sizes_60_smooth_category(self):
        """Test generate_sizes for 60_smooth category."""
        sizes = generate_sizes("60_smooth", 5, 16, 256, seed=42)
        assert len(sizes) > 0
        for s in sizes:
            assert is_60_smooth(s)
            assert not is_12_smooth(s)  # Should exclude 12-smooth

    def test_generate_sizes_poorly_factored_category(self):
        """Test generate_sizes for poorly_factored category."""
        sizes = generate_sizes("poorly_factored", 5, 16, 256, seed=42)
        assert len(sizes) > 0
        for s in sizes:
            assert is_poorly_factored(s)


class TestBenchmarkFFT:
    """Test single FFT benchmark function."""

    def test_benchmark_fft_basic(self):
        """Test basic FFT benchmark."""
        result = benchmark_fft(64, iterations=3, warmup=1, seed=42)

        assert isinstance(result, BenchmarkResult)
        assert result.size == 64
        assert result.category == "powers_of_2"
        assert result.execution_time_ns > 0
        assert result.peak_memory_bytes > 0
        assert result.precision_bits > 0
        assert result.accuracy_ulps >= 0
        assert result.forward_time_ns > 0
        assert result.inverse_time_ns > 0
    def test_benchmark_fft_deterministic(self):
        """Test that benchmark is deterministic with same seed."""
        r1 = benchmark_fft(128, iterations=5, warmup=2, seed=42)
        r2 = benchmark_fft(128, iterations=5, warmup=2, seed=42)

        # Should have identical structure and precision/accuracy (deterministic computation)
        # Timing may vary slightly due to system noise, so allow small tolerance
        assert r1.size == r2.size
        assert r1.category == r2.category
        assert r1.peak_memory_bytes == r2.peak_memory_bytes
        assert r1.precision_bits == r2.precision_bits
        assert r1.accuracy_ulps == r2.accuracy_ulps
        # Timing within 10% tolerance
        assert abs(r1.execution_time_ns - r2.execution_time_ns) / r1.execution_time_ns < 0.1
        assert abs(r1.forward_time_ns - r2.forward_time_ns) / r1.forward_time_ns < 0.1
        assert abs(r1.inverse_time_ns - r2.inverse_time_ns) / r1.inverse_time_ns < 0.1
        # poorly_factored
        r4 = benchmark_fft(13, iterations=3, warmup=1, seed=42)
        assert r4.category == "poorly_factored"

    def test_benchmark_fft_zero_size(self):
        """Test that zero size raises ValueError."""
        with pytest.raises(ValueError, match="FFT size must be positive"):
            benchmark_fft(0)

    def test_benchmark_fft_negative_size(self):
        """Test that negative size raises ValueError."""
        with pytest.raises(ValueError, match="FFT size must be positive"):
            benchmark_fft(-16)

    def test_benchmark_fft_precision_reasonable(self):
        """Test that precision is reasonable (not infinite, not too low)."""
        result = benchmark_fft(256, iterations=5, warmup=2, seed=42)
        # Double precision should give ~50 bits precision for clean signals
        assert result.precision_bits > 40
        assert result.precision_bits < 100

    def test_benchmark_fft_accuracy_reasonable(self):
        """Test that accuracy in ULPs is reasonable."""
        result = benchmark_fft(256, iterations=5, warmup=2, seed=42)
        # Should be small number of ULPs on average
        assert result.accuracy_ulps < 1000


class TestRunBenchmarks:
    """Test full benchmark suite."""

    def test_run_benchmarks_basic(self):
        """Test running benchmarks across all categories."""
        results = run_benchmarks(
            sizes_per_category=3,
            min_size=16,
            max_size=256,
            iterations=3,
            warmup=1,
            seed=42,
        )

        assert isinstance(results, dict)
        expected_categories = [
            "powers_of_2",
            "5_smooth",
            "12_smooth",
            "60_smooth",
            "poorly_factored",
        ]
        for cat in expected_categories:
            assert cat in results
            assert isinstance(results[cat], BenchmarkSummary)
            assert results[cat].category == cat

    def test_run_benchmarks_results_structure(self):
        """Test that benchmark results have correct structure."""
        results = run_benchmarks(
            sizes_per_category=2,
            min_size=16,
            max_size=128,
            iterations=2,
            warmup=1,
            seed=42,
        )

        for cat, summary in results.items():
            assert isinstance(summary.sizes_tested, list)
            assert isinstance(summary.results, list)
            assert len(summary.sizes_tested) == len(summary.results)

            if summary.results:
                assert summary.mean_execution_time_ns > 0
                assert summary.median_execution_time_ns > 0
                assert summary.mean_memory_bytes > 0
                assert summary.mean_precision_bits > 0
                assert summary.mean_accuracy_ulps >= 0

    def test_run_benchmarks_deterministic(self):
        """Test that full benchmark run produces deterministic results for precision, accuracy, and sizes."""
        # Note: execution timing is inherently non-deterministic on modern systems
        # We test only the deterministic properties: sizes, precision, accuracy, memory
        r1 = run_benchmarks(sizes_per_category=3, min_size=16, max_size=256, seed=42, iterations=10, warmup=3)
        r2 = run_benchmarks(sizes_per_category=3, min_size=16, max_size=256, seed=42, iterations=10, warmup=3)

        for cat in r1:
            s1 = r1[cat]
            s2 = r2[cat]
            assert s1.sizes_tested == s2.sizes_tested
            if s1.results:
                for res1, res2 in zip(s1.results, s2.results):
                    # These are deterministic based on the seed
                    assert res1.peak_memory_bytes == res2.peak_memory_bytes
                    assert res1.precision_bits == res2.precision_bits
                    assert res1.accuracy_ulps == res2.accuracy_ulps
                    # Timing is non-deterministic - skip assertion
                    # assert abs(res1.execution_time_ns - res2.execution_time_ns) / res1.execution_time_ns < 0.10

    def test_run_benchmarks_to_dict(self):
        """Test that results can be converted to dict."""
        results = run_benchmarks(
            sizes_per_category=2,
            min_size=16,
            max_size=64,
            iterations=2,
            warmup=1,
            seed=42,
        )

        for summary in results.values():
            d = summary.to_dict()
            assert "category" in d
            assert "sizes_tested" in d
            assert "results" in d
            assert "mean_execution_time_ns" in d
            assert "median_execution_time_ns" in d
            assert "mean_memory_bytes" in d
            assert "mean_precision_bits" in d
            assert "mean_accuracy_ulps" in d

            for r in d["results"]:
                assert "size" in r
                assert "category" in r
                assert "execution_time_ns" in r
                assert "peak_memory_bytes" in r
                assert "precision_bits" in r
                assert "accuracy_ulps" in r
                assert "forward_time_ns" in r
                assert "inverse_time_ns" in r
    def test_run_benchmarks_empty_category(self):
        """Test run_benchmarks with a category that has no sizes in range (lines 361-366)."""
        # Use a very narrow range where poorly_factored might have no sizes
        # For example, min_size=16, max_size=16: only size 16 (power of 2)
        results = run_benchmarks(
            sizes_per_category=5,
            min_size=16,
            max_size=16,
            iterations=2,
            warmup=1,
            seed=42,
        )
        # All categories should be present
        for cat in ["powers_of_2", "5_smooth", "12_smooth", "60_smooth", "poorly_factored"]:
            assert cat in results
            assert results[cat].category == cat
        # powers_of_2 should have size 16
        assert results["powers_of_2"].sizes_tested == [16]
        # Other categories should have empty sizes_tested
        for cat in ["5_smooth", "12_smooth", "60_smooth", "poorly_factored"]:
            assert results[cat].sizes_tested == []
            assert results[cat].results == []
            # These should have default/empty summary values
            assert results[cat].mean_execution_time_ns == 0.0
            assert results[cat].median_execution_time_ns == 0.0
            assert results[cat].mean_memory_bytes == 0.0
            assert results[cat].mean_precision_bits == 0.0
            assert results[cat].mean_accuracy_ulps == 0.0

    def test_run_benchmarks_exception_handling(self, monkeypatch):
        """Test run_benchmarks handles exceptions in benchmark_fft (lines 373-376)."""
        from base60lab.fft_benchmarks import benchmark_fft
        
        # Mock benchmark_fft to raise an exception for specific sizes
        original_benchmark = benchmark_fft
        
        def mock_benchmark(size, iterations=10, warmup=3, seed=42):
            if size == 32:
                raise RuntimeError("Simulated benchmark failure")
            return original_benchmark(size, iterations, warmup, seed)
        
        monkeypatch.setattr("base60lab.fft_benchmarks.benchmark_fft", mock_benchmark)
        
        # Run with a range that includes 32
        results = run_benchmarks(
            sizes_per_category=5,
            min_size=16,
            max_size=64,
            iterations=2,
            warmup=1,
            seed=42,
        )
        
        # Should complete without crashing
        assert "powers_of_2" in results
        # The 32 size should be skipped due to exception
        powers_of_2_sizes = results["powers_of_2"].sizes_tested
        assert 16 in powers_of_2_sizes
        # 32 might be in sizes_tested but not in results (since it failed)
        # or it might not be in sizes_tested at all depending on implementation
        # The key thing is no crash occurred

    def test_run_benchmarks_all_fail_in_category(self, monkeypatch):
        """Test run_benchmarks when all benchmarks in a category fail (line 395)."""
        from base60lab.fft_benchmarks import benchmark_fft
        
        # Mock benchmark_fft to always raise an exception
        def mock_benchmark(size, iterations=10, warmup=3, seed=42):
            raise RuntimeError("All benchmarks fail")
        
        monkeypatch.setattr("base60lab.fft_benchmarks.benchmark_fft", mock_benchmark)
        
        results = run_benchmarks(
            sizes_per_category=3,
            min_size=16,
            max_size=128,
            iterations=2,
            warmup=1,
            seed=42,
        )
        
        # Should complete without crashing
        for cat in results:
            assert cat in results
            assert results[cat].category == cat
            # All results should be empty since all benchmarks failed
            assert results[cat].results == []
            # Summary values should be defaults (0.0)
            assert results[cat].mean_execution_time_ns == 0.0
            assert results[cat].median_execution_time_ns == 0.0
            assert results[cat].mean_memory_bytes == 0.0
            assert results[cat].mean_precision_bits == 0.0
            assert results[cat].mean_accuracy_ulps == 0.0


class TestAdversarialInputs:
    """Test adversarial/malformed inputs."""

    def test_zero_size_raises(self):
        """Zero FFT size should raise ValueError."""
        with pytest.raises(ValueError):
            benchmark_fft(0)

    def test_negative_size_raises(self):
        """Negative FFT size should raise ValueError."""
        with pytest.raises(ValueError):
            benchmark_fft(-64)

    def test_very_small_size(self):
        """Test minimum valid size."""
        result = benchmark_fft(1, iterations=2, warmup=1, seed=42)
        assert result.size == 1
        assert result.execution_time_ns > 0

    def test_very_large_size(self):
        """Test larger FFT size."""
        result = benchmark_fft(8192, iterations=2, warmup=1, seed=42)
        assert result.size == 8192
        assert result.execution_time_ns > 0


class TestOutputDataStructure:
    """Test that output data structures are valid and not misleading."""

    def test_benchmark_result_to_dict(self):
        """Test BenchmarkResult.to_dict() produces valid dict."""
        result = benchmark_fft(64, iterations=3, warmup=1, seed=42)
        d = result.to_dict()

        required_keys = [
            "size",
            "category",
            "execution_time_ns",
            "peak_memory_bytes",
            "precision_bits",
            "accuracy_ulps",
            "forward_time_ns",
            "inverse_time_ns",
        ]
        for key in required_keys:
            assert key in d, f"Missing key: {key}"

        # Values should be correct types
        assert isinstance(d["size"], int)
        assert isinstance(d["category"], str)
        assert isinstance(d["execution_time_ns"], int)
        assert isinstance(d["peak_memory_bytes"], int)
        assert isinstance(d["precision_bits"], float)
        assert isinstance(d["accuracy_ulps"], float)
        assert isinstance(d["forward_time_ns"], int)
        assert isinstance(d["inverse_time_ns"], int)

    def test_benchmark_summary_to_dict(self):
        """Test BenchmarkSummary.to_dict() produces valid dict."""
        results = run_benchmarks(sizes_per_category=2, min_size=16, max_size=64, seed=42)
        summary = results["powers_of_2"]
        d = summary.to_dict()

        required_keys = [
            "category",
            "sizes_tested",
            "results",
            "mean_execution_time_ns",
            "median_execution_time_ns",
            "mean_memory_bytes",
            "mean_precision_bits",
            "mean_accuracy_ulps",
        ]
        for key in required_keys:
            assert key in d, f"Missing key: {key}"

    def test_no_mock_or_fake_data(self):
        """Verify that benchmarks produce real measurements, not fake data."""
        result = benchmark_fft(128, iterations=5, warmup=2, seed=42)

        # Execution time should be realistic (not zero, not suspiciously round)
        assert result.execution_time_ns > 1000  # At least microseconds
        assert result.execution_time_ns < 1_000_000_000  # Less than a second

        # Memory should be realistic
        assert result.peak_memory_bytes > 1000  # At least KB
        assert result.peak_memory_bytes < 100_000_000  # Less than 100MB

        # Precision should be realistic for double precision
        assert 40 < result.precision_bits < 60

        # Accuracy should be realistic
        assert 0 <= result.accuracy_ulps < 100


class TestPrintFunction:
    """Test print_benchmark_results function."""

    def test_print_benchmark_results_runs(self, capsys):
        """Test that print function runs without error."""
        results = run_benchmarks(
            sizes_per_category=2,
            min_size=16,
            max_size=64,
            iterations=2,
            warmup=1,
            seed=42,
        )
        print_benchmark_results(results)
        captured = capsys.readouterr()
        assert "FFT Benchmark Results" in captured.out
        assert "POWERS_OF_2" in captured.out
    def test_print_benchmark_results_no_data(self, capsys):
        """Test print_benchmark_results with empty category results (lines 415-416)."""
        from base60lab.fft_benchmarks import BenchmarkSummary
        
        # Create results with one category having no data
        results = {
            "powers_of_2": BenchmarkSummary(
                category="powers_of_2",
                sizes_tested=[16, 32],
                results=[],
                mean_execution_time_ns=0.0,
                median_execution_time_ns=0.0,
                mean_memory_bytes=0.0,
                mean_precision_bits=0.0,
                mean_accuracy_ulps=0.0,
            ),
            "5_smooth": BenchmarkSummary(
                category="5_smooth",
                sizes_tested=[],
                results=[],
            ),
        }
        print_benchmark_results(results)
        captured = capsys.readouterr()
        assert "5_smooth: No data" in captured.out


# Run a quick manual verification when executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])