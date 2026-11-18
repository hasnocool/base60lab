"""Tests for the timeseries module."""

import pytest

from base60lab.core.rational import Rational
from base60lab.timeseries import (
    TimeSeries,
    TimePoint,
    TemporalInterval,
    compound_interest,
    simple_interest,
    present_value,
    annuity_future_value,
    annuity_present_value,
    continuous_compounding,
    loan_amortization_schedule,
    terminating_denominators,
)


class TestTimeSeries:
    """Tests for time series."""

    def test_creation(self):
        ts = TimeSeries()
        assert ts is not None

    def test_add_data_point(self):
        ts = TimeSeries()
        timestamp = TimePoint(Rational(1, 1))
        value = Rational(100, 1)
        ts.add(timestamp, value)
        assert len(ts.points) == 1

    def test_exact_arithmetic(self):
        ts = TimeSeries()
        ts.add(TimePoint(Rational(1, 1)), Rational(1, 3))
        ts.add(TimePoint(Rational(2, 1)), Rational(1, 6))
        # Sum should be exactly 1/2
        total = sum(v for _, v in ts.points)
        assert total == Rational(1, 2)

    def test_window_aggregation(self):
        ts = TimeSeries()
        for i in range(10):
            ts.add(TimePoint(Rational(i, 1)), Rational(i, 1))
        
        # Sum over window [2, 5]
        interval = TemporalInterval(TimePoint(Rational(2, 1)), TimePoint(Rational(5, 1)))
        window_sum = ts.window_sum(interval)
        expected = sum(Rational(i, 1) for i in range(2, 6))
        assert window_sum == expected


class TestExactInterestCalculation:
    """Tests for exact interest calculations."""

    def test_simple_interest(self):
        principal = Rational(1000, 1)
        rate = Rational(5, 100)  # 5%
        time = Rational(1, 1)  # 1 year
        
        interest = simple_interest(principal, rate, time)
        expected = Rational(50, 1)
        assert interest == expected

    def test_compound_interest(self):
        principal = Rational(1000, 1)
        rate = Rational(5, 100)
        periods = 4  # quarterly
        
        # A = P(1 + r/n)^(nt)
        result = compound_interest(principal, rate, Rational(1, 1), compounding=periods)
        expected = principal * (Rational(1, 1) + rate / Rational(periods, 1)) ** periods
        assert result == expected

    def test_no_rounding_error(self):
        """Test that compound interest has no floating-point rounding error."""
        principal = Rational(1, 1)
        rate = Rational(1, 3)  # 33.33...%
        periods = 12
        
        result = compound_interest(principal, rate, Rational(1, 1), compounding=periods)
        # Result should be exact rational
        assert isinstance(result, Rational)
        # No floating-point involved


class TestFinancialFunctions:
    """Tests for financial functions."""

    def test_present_value(self):
        future = Rational(1000, 1)
        rate = Rational(5, 100)
        periods = 10
        
        pv = present_value(future, rate, periods)
        expected = future / (Rational(1, 1) + rate) ** periods
        assert pv == expected

    def test_annuity_future_value(self):
        payment = Rational(100, 1)
        rate = Rational(5, 100)
        periods = 10
        
        fv = annuity_future_value(payment, rate, periods)
        expected = payment * ((Rational(1, 1) + rate) ** periods - Rational(1, 1)) / rate
        assert fv == expected

    def test_annuity_present_value(self):
        payment = Rational(100, 1)
        rate = Rational(5, 100)
        periods = 10
        
        pv = annuity_present_value(payment, rate, periods)
        expected = payment * (Rational(1, 1) - (Rational(1, 1) + rate) ** (-periods)) / rate
        assert pv == expected

    def test_continuous_compounding(self):
        principal = Rational(1000, 1)
        rate = Rational(5, 100)
        time = Rational(1, 1)
        
        result = continuous_compounding(principal, rate, Rational(1, 1))
        # e^(rt) approximation using series
        assert isinstance(result, Rational)

    def test_loan_amortization_schedule(self):
        principal = Rational(100000, 1)
        rate = Rational(5, 100)
        periods = 360  # 30 years monthly
        
        schedule = loan_amortization_schedule(Rational(100000, 1), Rational(5, 100), 360, Rational(1, 12))
        assert len(schedule) == 360
        for payment in schedule:
            assert 'principal' in payment
            assert 'interest' in payment
            assert 'balance' in payment


class TestTerminatingDenominators:
    """Tests for terminating denominator analysis."""

    def test_terminating_denominators(self):
        denoms = terminating_denominators(max_denom=100, base=60)
        # Should include all numbers whose prime factors are subset of {2,3,5}
        assert 1 in denoms
        assert 2 in denoms
        assert 3 in denoms
        assert 4 in denoms
        assert 5 in denoms
        assert 6 in denoms
        assert 7 not in denoms
        assert 11 not in denoms

    def test_base60_vs_base10(self):
        base60_denoms = terminating_denominators(max_denom=100, base=60)
        base10_denoms = terminating_denominators(max_denom=100, base=10)
        base12_denoms = terminating_denominators(max_denom=100, base=12)
        
        assert len(base60_denoms) > len(base12_denoms)
        assert len(base12_denoms) > len(base10_denoms)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])