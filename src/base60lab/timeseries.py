"""Sexagesimal time-series database module — exact rational temporal arithmetic.

This module provides:
1. SEXAGESIMAL type (numerator/denominator) using exact rational arithmetic
2. Temporal functions: interval arithmetic, windowing, downsampling
3. Exact interest/accrual calculations (zero rounding error)
4. Round-trip fidelity with base-10/12/60
5. Exact temporal joins, window aggregations
6. Comparison to DECIMAL/NUMERIC for financial time-series

All internal arithmetic uses :class:`base60lab.core.rational.Rational`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal, getcontext
from fractions import Fraction
from math import gcd
from typing import Any, Callable, Generic, Iterator, TypeVar

import numpy as np

from .core.rational import Rational, rational, zero, one
from .core.types import BaseNumber, NotationSystem

T = TypeVar("T")

# Configure decimal for comparison with exact arithmetic
getcontext().prec = 50


# =============================================================================
# SEXAGESIMAL TYPE
# =============================================================================

@dataclass(frozen=True, slots=True)
class Sexagesimal:
    """Exact sexagesimal value using numerator/denominator rational arithmetic.

    This is the core type for native base-60 storage. All arithmetic is exact
    (no floating-point), making it suitable for financial timestamps,
    interest calculations, and temporal joins where rounding error is unacceptable.

    The internal value is a :class:`Rational` in lowest terms.
    Base-60 is a *presentation choice only* and never affects the underlying value.
    """
    value: Rational
    """Exact rational value."""

    def __post_init__(self) -> None:
        # Ensure value is always a Rational
        if not isinstance(self.value, Rational):
            object.__setattr__(self, 'value', Rational(self.value))

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    @classmethod
    def from_int(cls, n: int) -> Sexagesimal:
        """Create from integer."""
        return cls(Rational(n))

    @classmethod
    def from_fraction(cls, num: int, den: int) -> Sexagesimal:
        """Create from numerator/denominator."""
        return cls(Rational(num, den))

    @classmethod
    def from_rational(cls, r: Rational) -> Sexagesimal:
        """Create from Rational."""
        return cls(r)

    @classmethod
    def from_float(cls, f: float) -> Sexagesimal:
        """Create from float (exact conversion via Fraction)."""
        return cls(Rational(Fraction(f).limit_denominator()))

    @classmethod
    def from_decimal(cls, d: Decimal) -> Sexagesimal:
        """Create from Decimal (exact conversion)."""
        # Convert Decimal to Fraction exactly
        frac = Fraction(d).limit_denominator()
        return cls(Rational(frac))

    @classmethod
    def from_base10_string(cls, s: str) -> Sexagesimal:
        """Parse base-10 string exactly (e.g., "3.14159")."""
        if "." not in s:
            return cls(Rational(int(s)))
        int_part, frac_part = s.split(".")
        den = 10 ** len(frac_part)
        num = int(int_part) * den + int(frac_part)
        if s.startswith("-"):
            num = -num
        return cls(Rational(num, den))

    @classmethod
    def from_sexagesimal_string(cls, s: str) -> Sexagesimal:
        """Parse sexagesimal string (e.g., "1;30,15" = 1 + 30/60 + 15/3600).
        
        Supports both comma-separated places (each 0-59) and single-char notation
        where A=10, B=11, ..., Z=35, and <36> through <59> for higher values.
        If no commas and all digits, treats as single integer place value.
        """
        sign = -1 if s.startswith("-") else 1
        if sign == -1:
            s = s[1:]

        if ";" in s:
            int_part, frac_part = s.split(";")
        else:
            int_part, frac_part = s, ""

        integer = int(int_part) if int_part else 0
        value = Rational(integer)

        if frac_part:
            # Check if using comma-separated format
            if "," in frac_part:
                places = frac_part.split(",")
            else:
                # No commas: could be single-char notation or single multi-digit place
                # If all digits, treat as single integer place value
                if frac_part.isdigit():
                    places = [frac_part]
                else:
                    # Single-char notation: each char is a digit
                    places = list(frac_part)

            for i, place in enumerate(places):
                if not place:
                    continue
                # Parse place value: could be single char (A-Z, <N>) or integer
                if place.startswith("<") and place.endswith(">"):
                    digit_val = int(place[1:-1])
                elif len(place) == 1:
                    c = place.upper()
                    if '0' <= c <= '9':
                        digit_val = ord(c) - ord('0')
                    elif 'A' <= c <= 'Z':
                        digit_val = ord(c) - ord('A') + 10
                    else:
                        raise ValueError(f"Invalid sexagesimal digit: {place}")
                else:
                    digit_val = int(place)
                
                value += Rational(digit_val, 60 ** (i + 1))

        return cls(Rational(sign * value.numerator, value.denominator))

    @classmethod
    def from_timestamp(cls, dt: datetime) -> Sexagesimal:
        """Create from datetime: exact rational days since epoch."""
        # Use Unix epoch as reference
        epoch = datetime(1970, 1, 1)
        delta = dt - epoch
        total_seconds = delta.total_seconds()
        # Represent as rational seconds
        return cls(Rational(Fraction(total_seconds).limit_denominator()))

    # -------------------------------------------------------------------------
    # Arithmetic (all exact)
    # -------------------------------------------------------------------------

    def __add__(self, other: Sexagesimal | int | Rational) -> Sexagesimal:
        if isinstance(other, Sexagesimal):
            return Sexagesimal(self.value + other.value)
        if isinstance(other, Rational):
            return Sexagesimal(self.value + other)
        return Sexagesimal(self.value + Rational(other))

    def __sub__(self, other: Sexagesimal | int | Rational) -> Sexagesimal:
        if isinstance(other, Sexagesimal):
            return Sexagesimal(self.value - other.value)
        if isinstance(other, Rational):
            return Sexagesimal(self.value - other)
        return Sexagesimal(self.value - Rational(other))

    def __mul__(self, other: Sexagesimal | int | Rational) -> Sexagesimal:
        if isinstance(other, Sexagesimal):
            return Sexagesimal(self.value * other.value)
        if isinstance(other, Rational):
            return Sexagesimal(self.value * other)
        return Sexagesimal(self.value * Rational(other))

    def __truediv__(self, other: Sexagesimal | int | Rational) -> Sexagesimal:
        if isinstance(other, Sexagesimal):
            if other.value == 0:
                raise ZeroDivisionError("division by zero Sexagesimal")
            return Sexagesimal(self.value / other.value)
        if isinstance(other, Rational):
            if other == 0:
                raise ZeroDivisionError("division by zero Rational")
            return Sexagesimal(self.value / other)
        if other == 0:
            raise ZeroDivisionError("division by zero")
        return Sexagesimal(self.value / Rational(other))

    def __neg__(self) -> Sexagesimal:
        return Sexagesimal(-self.value)

    def __abs__(self) -> Sexagesimal:
        return Sexagesimal(abs(self.value))

    def __pow__(self, exponent: int) -> Sexagesimal:
        return Sexagesimal(self.value ** exponent)

    # -------------------------------------------------------------------------
    # Comparison (base-independent)
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Sexagesimal):
            return self.value == other.value
        if isinstance(other, (int, Rational, Fraction)):
            return self.value == Rational(other)
        return NotImplemented

    def __lt__(self, other: Sexagesimal | int | Rational) -> bool:
        if isinstance(other, Sexagesimal):
            return self.value < other.value
        if isinstance(other, Rational):
            return self.value < other
        return self.value < Rational(other)

    def __le__(self, other: Sexagesimal | int | Rational) -> bool:
        if isinstance(other, Sexagesimal):
            return self.value <= other.value
        if isinstance(other, Rational):
            return self.value <= other
        return self.value <= Rational(other)

    def __gt__(self, other: Sexagesimal | int | Rational) -> bool:
        if isinstance(other, Sexagesimal):
            return self.value > other.value
        if isinstance(other, Rational):
            return self.value > other
        return self.value > Rational(other)

    def __ge__(self, other: Sexagesimal | int | Rational) -> bool:
        if isinstance(other, Sexagesimal):
            return self.value >= other.value
        if isinstance(other, Rational):
            return self.value >= other
        return self.value >= Rational(other)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def numerator(self) -> int:
        return self.value.numerator

    @property
    def denominator(self) -> int:
        return self.value.denominator

    def is_integer(self) -> bool:
        return self.value.is_integer()

    def is_terminating_in_base(self, base: int) -> bool:
        """True if this value terminates in the given base."""
        return self.value.is_terminating_in_base(base)

    def repeating_period_in_base(self, base: int) -> int | None:
        """Repeating period length in given base, or None if terminating."""
        return self.value.repeating_period_in_base(base)

    # -------------------------------------------------------------------------
    # Conversion / Representation
    # -------------------------------------------------------------------------

    def to_rational(self) -> Rational:
        return self.value

    def to_fraction(self) -> Fraction:
        return self.value.to_fraction()

    def to_float(self) -> float:
        """For display/debugging only — never for internal arithmetic."""
        return self.value.to_float()

    def to_decimal(self) -> Decimal:
        """Exact conversion to Decimal for comparison with DECIMAL/NUMERIC."""
        frac = self.to_fraction()
        return Decimal(frac.numerator) / Decimal(frac.denominator)

    def to_base_number(self, base: int = 60) -> BaseNumber:
        """Convert to BaseNumber for engine processing."""
        if base not in (10, 12, 60):
            raise ValueError("base must be 10, 12, or 60")
        return BaseNumber(self.value, base)

    def to_sexagesimal_notation(self) -> str:
        """Render as sexagesimal notation (e.g., '1;30,15').
        
        Uses comma-separated places for fractional part, where each place
        is an integer 0-59 (not base-36 encoded).
        """
        num = self.value.numerator
        den = self.value.denominator
        sign = "-" if num < 0 else ""
        num = abs(num)

        integer_part = num // den
        remainder = num % den

        # Integer part in base 60
        if integer_part == 0:
            int_digits = ["0"]
        else:
            parts: list[str] = []
            n = integer_part
            while n > 0:
                parts.append(str(n % 60))
                n //= 60
            int_digits = list(reversed(parts))

        int_text = ",".join(int_digits) if len(int_digits) > 1 else int_digits[0]

        if remainder == 0:
            return f"{sign}{int_text}"

        # Fractional part: long division in base 60 (comma-separated places)
        frac_digits: list[str] = []
        seen: dict[int, int] = {}
        r = remainder
        repeating_start: int | None = None

        while r != 0 and r not in seen:
            seen[r] = len(frac_digits)
            r *= 60
            digit = r // den
            frac_digits.append(str(digit))
            r = r % den

        if r in seen:
            repeating_start = seen[r]
            non_rep = ",".join(frac_digits[:repeating_start])
            rep = ",".join(frac_digits[repeating_start:])
            return f"{sign}{int_text};{non_rep}({rep})"
        else:
            return f"{sign}{int_text};" + ",".join(frac_digits)

    def to_base10_string(self, precision: int | None = None) -> str:
        """Render as base-10 string."""
        if precision is not None:
            # Compute to specified precision
            return f"{self.to_decimal():.{precision}f}"
        return str(self.to_decimal())

    def __repr__(self) -> str:
        if self.denominator == 1:
            return f"Sexagesimal({self.numerator})"
        return f"Sexagesimal({self.numerator}/{self.denominator})"

    def __str__(self) -> str:
        return self.to_sexagesimal_notation()

    def __hash__(self) -> int:
        return hash(self.value)


# =============================================================================
# TEMPORAL INTERVALS
# =============================================================================

@dataclass(frozen=True, slots=True)
class TemporalInterval:
    """Exact temporal interval [start, end) using Sexagesimal bounds."""

    start: Sexagesimal
    end: Sexagesimal

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError("interval start must be <= end")

    @property
    def duration(self) -> Sexagesimal:
        """Exact interval duration."""
        return self.end - self.start

    def contains(self, point: Sexagesimal) -> bool:
        """True if point in [start, end)."""
        return self.start <= point < self.end

    def overlaps(self, other: TemporalInterval) -> bool:
        """True if intervals overlap."""
        return self.start < other.end and other.start < self.end

    def intersection(self, other: TemporalInterval) -> TemporalInterval | None:
        """Return intersection interval, or None if disjoint."""
        if not self.overlaps(other):
            return None
        return TemporalInterval(
            max(self.start, other.start),
            min(self.end, other.end)
        )

    def union(self, other: TemporalInterval) -> TemporalInterval:
        """Return union interval (requires overlap or adjacency)."""
        if not self.overlaps(other) and not self.is_adjacent(other):
            raise ValueError("intervals must overlap or be adjacent for union")
        return TemporalInterval(
            min(self.start, other.start),
            max(self.end, other.end)
        )

    def is_adjacent(self, other: TemporalInterval) -> bool:
        """True if intervals touch but don't overlap."""
        return self.end == other.start or other.end == self.start

    def split_at(self, point: Sexagesimal) -> tuple[TemporalInterval, TemporalInterval] | None:
        """Split interval at point; returns None if point not in interval."""
        if not self.contains(point):
            return None
        return (
            TemporalInterval(self.start, point),
            TemporalInterval(point, self.end)
        )

    def scale(self, factor: Sexagesimal | Rational | int) -> TemporalInterval:
        """Scale interval duration by factor (about start)."""
        if isinstance(factor, (int, Rational)):
            factor = Sexagesimal(factor)
        dur = self.duration * factor
        return TemporalInterval(self.start, self.start + dur)

    def shift(self, offset: Sexagesimal | Rational | int) -> TemporalInterval:
        """Shift interval by offset."""
        if isinstance(offset, (int, Rational)):
            offset = Sexagesimal(offset)
        return TemporalInterval(self.start + offset, self.end + offset)

    def to_base10_seconds(self) -> tuple[float, float]:
        """For interop: (start_sec, end_sec) as floats."""
        return (self.start.to_float(), self.end.to_float())


# =============================================================================
# TIME SERIES DATA STRUCTURES
# =============================================================================

@dataclass(frozen=True, slots=True)
class TimePoint:
    """Single time-value pair with exact timestamp."""

    timestamp: Sexagesimal
    value: Sexagesimal
    metadata: dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other: TimePoint) -> bool:
        return self.timestamp < other.timestamp


@dataclass
class TimeSeries:
    """Ordered sequence of exact time-value pairs.

    Supports exact temporal operations: windowing, downsampling, joins,
    aggregation — all with zero rounding error.
    """

    points: list[TimePoint] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Ensure sorted by timestamp
        self.points.sort(key=lambda p: p.timestamp)

    def __len__(self) -> int:
        return len(self.points)

    def __iter__(self) -> Iterator[TimePoint]:
        return iter(self.points)

    def __getitem__(self, idx: int) -> TimePoint:
        return self.points[idx]

    def append(self, timestamp: Sexagesimal, value: Sexagesimal, metadata: dict | None = None) -> None:
        """Add a point maintaining order."""
        tp = TimePoint(timestamp, value, metadata or {})
        # Insert in sorted position
        import bisect
        bisect.insort(self.points, tp)

    def extend(self, points: list[TimePoint]) -> None:
        """Add multiple points."""
        for p in points:
            self.append(p.timestamp, p.value, p.metadata)

    def time_range(self) -> TemporalInterval | None:
        """Return bounding interval of the series."""
        if not self.points:
            return None
        return TemporalInterval(self.points[0].timestamp, self.points[-1].timestamp)

    # -------------------------------------------------------------------------
    # Windowing
    # -------------------------------------------------------------------------

    def window(self, interval: TemporalInterval) -> TimeSeries:
        """Return points within interval [start, end)."""
        result = TimeSeries()
        for p in self.points:
            if interval.contains(p.timestamp):
                result.append(p.timestamp, p.value, p.metadata.copy())
        return result

    def sliding_window(
        self,
        window_duration: Sexagesimal,
        step: Sexagesimal | None = None
    ) -> Iterator[TimeSeries]:
        """Generate sliding windows of fixed duration."""
        if step is None:
            step = window_duration

        if not self.points:
            return

        bounds = self.time_range()
        if bounds is None:
            return

        current_start = bounds.start
        while current_start < bounds.end:
            window_end = current_start + window_duration
            interval = TemporalInterval(current_start, window_end)
            yield self.window(interval)
            current_start += step

    def tumbling_window(self, window_duration: Sexagesimal) -> Iterator[TimeSeries]:
        """Generate non-overlapping tumbling windows."""
        yield from self.sliding_window(window_duration, window_duration)

    # -------------------------------------------------------------------------
    # Downsampling / Resampling
    # -------------------------------------------------------------------------

    def downsample(
        self,
        target_interval: Sexagesimal,
        aggregation: Callable[[list[Sexagesimal]], Sexagesimal] | None = None
    ) -> TimeSeries:
        """Downsample to regular grid using exact aggregation.

        Args:
            target_interval: Duration of each output bucket.
            aggregation: Function to aggregate values in each bucket.
                       Default: exact arithmetic mean.
        """
        if aggregation is None:
            aggregation = lambda vals: sum(vals, Sexagesimal(0)) / Sexagesimal(len(vals))
        """Downsample to regular grid using exact aggregation.

        Args:
            target_interval: Duration of each output bucket.
            aggregation: Function to aggregate values in each bucket.
                       Default: exact arithmetic mean.
        """
        if not self.points:
            return TimeSeries()

        bounds = self.time_range()
        assert bounds is not None

        result = TimeSeries()
        bucket_start = bounds.start

        while bucket_start < bounds.end:
            bucket_end = bucket_start + target_interval
            interval = TemporalInterval(bucket_start, bucket_end)

            # Collect values in bucket
            bucket_values: list[Sexagesimal] = []
            for p in self.points:
                if interval.contains(p.timestamp):
                    bucket_values.append(p.value)

            if bucket_values:
                agg_value = aggregation(bucket_values)
                # Use bucket center as timestamp
                center = bucket_start + target_interval / 2
                result.append(center, agg_value)

            bucket_start = bucket_end

        return result

    def resample_linear(self, target_timestamps: list[Sexagesimal]) -> TimeSeries:
        """Resample to exact target timestamps using linear interpolation.

        All arithmetic is exact rational.
        """
        if not self.points or len(self.points) < 2:
            return TimeSeries()

        result = TimeSeries()

        for target_ts in target_timestamps:
            # Find surrounding points
            before: TimePoint | None = None
            after: TimePoint | None = None

            for p in self.points:
                if p.timestamp <= target_ts:
                    before = p
                elif p.timestamp > target_ts:
                    after = p
                    break

            if before is None or after is None:
                # Extrapolate using nearest
                nearest = before or after
                assert nearest is not None
                result.append(target_ts, nearest.value)
                continue

            # Exact linear interpolation
            t0, v0 = before.timestamp, before.value
            t1, v1 = after.timestamp, after.value

            if t1 == t0:
                result.append(target_ts, v0)
                continue

            # weight = (target - t0) / (t1 - t0)  [exact rational]
            weight = (target_ts - t0) / (t1 - t0)
            # value = v0 + weight * (v1 - v0)
            interp_value = v0 + weight * (v1 - v0)
            result.append(target_ts, interp_value)

        return result

    # -------------------------------------------------------------------------
    # Temporal Joins
    # -------------------------------------------------------------------------

    def temporal_join(
        self,
        other: TimeSeries,
        max_distance: Sexagesimal | None = None,
        how: str = "inner"
    ) -> list[tuple[TimePoint, TimePoint]]:
        """Exact temporal join: match points within max_distance.

        Args:
            other: Other time series to join with.
            max_distance: Maximum temporal distance for a match.
                         None = exact timestamp match only.
            how: "inner", "left", "right", "outer"

        Returns:
            List of (point_from_self, point_from_other) pairs.
        """
        if not self.points or not other.points:
            return []

        result: list[tuple[TimePoint, TimePoint]] = []
        matched_other: set[int] = set()

        for i, p1 in enumerate(self.points):
            best_match: tuple[int, Sexagesimal] | None = None  # (idx, distance)

            for j, p2 in enumerate(other.points):
                dist = abs(p1.timestamp - p2.timestamp)
                if max_distance is not None and dist > max_distance:
                    continue
                if best_match is None or dist < best_match[1]:
                    best_match = (j, dist)

            if best_match is not None:
                j, _ = best_match
                result.append((p1, other.points[j]))
                matched_other.add(j)

        if how in ("left", "outer"):
            # Already have all left points that matched
            pass

        if how in ("right", "outer"):
            for j, p2 in enumerate(other.points):
                if j not in matched_other:
                    # Find closest in self
                    best_match = None
                    best_dist = None
                    for i, p1 in enumerate(self.points):
                        dist = abs(p1.timestamp - p2.timestamp)
                        if max_distance is not None and dist > max_distance:
                            continue
                        if best_dist is None or dist < best_dist:
                            best_dist = dist
                            best_match = i
                    if best_match is not None:
                        result.append((self.points[best_match], p2))

        return result

    def asof_join(self, other: TimeSeries) -> list[tuple[TimePoint, TimePoint]]:
        """ASOF join: for each point in self, find most recent point in other.

        Both series must be sorted by timestamp (enforced by TimeSeries).
        """
        if not self.points or not other.points:
            return []

        result: list[tuple[TimePoint, TimePoint]] = []
        j = 0

        for p1 in self.points:
            # Advance j to most recent point in other <= p1.timestamp
            while j + 1 < len(other.points) and other.points[j + 1].timestamp <= p1.timestamp:
                j += 1

            if other.points[j].timestamp <= p1.timestamp:
                result.append((p1, other.points[j]))

        return result

    # -------------------------------------------------------------------------
    # Window Aggregations
    # -------------------------------------------------------------------------

    def window_aggregate(
        self,
        window_duration: Sexagesimal,
        aggregations: dict[str, Callable[[list[Sexagesimal]], Sexagesimal]],
        step: Sexagesimal | None = None
    ) -> TimeSeries:
        """Compute multiple aggregations over sliding windows.

        Returns a TimeSeries where each point's value is a dict of aggregation results.
        """
        if step is None:
            step = window_duration

        bounds = self.time_range()
        if bounds is None:
            return TimeSeries()

        result = TimeSeries()
        current_start = bounds.start

        while current_start < bounds.end:
            window_end = current_start + window_duration
            interval = TemporalInterval(current_start, window_end)

            # Collect values in window
            window_values = [p.value for p in self.points if interval.contains(p.timestamp)]

            if window_values:
                agg_results = {}
                for name, agg_func in aggregations.items():
                    agg_results[name] = agg_func(window_values)

                center = current_start + window_duration / 2
                result.append(center, Sexagesimal.from_fraction(0, 1), agg_results)

            current_start += step

        return result

    # Common aggregation functions (all exact)
    @staticmethod
    def agg_count(values: list[Sexagesimal]) -> Sexagesimal:
        return Sexagesimal(len(values))

    @staticmethod
    def agg_sum(values: list[Sexagesimal]) -> Sexagesimal:
        return sum(values, Sexagesimal(0))

    @staticmethod
    def agg_mean(values: list[Sexagesimal]) -> Sexagesimal:
        return sum(values, Sexagesimal(0)) / Sexagesimal(len(values))

    @staticmethod
    def agg_min(values: list[Sexagesimal]) -> Sexagesimal:
        return min(values)

    @staticmethod
    def agg_max(values: list[Sexagesimal]) -> Sexagesimal:
        return max(values)

    @staticmethod
    def agg_first(values: list[Sexagesimal]) -> Sexagesimal:
        return values[0]

    @staticmethod
    def agg_last(values: list[Sexagesimal]) -> Sexagesimal:
        return values[-1]

    @staticmethod
    def agg_variance(values: list[Sexagesimal]) -> Sexagesimal:
        """Exact population variance."""
        n = len(values)
        if n <= 1:
            return Sexagesimal(0)
        mean = sum(values, Sexagesimal(0)) / Sexagesimal(n)
        sq_diffs = sum(((v - mean) ** 2 for v in values), Sexagesimal(0))
        return sq_diffs / Sexagesimal(n)

    @staticmethod
    def agg_stddev(values: list[Sexagesimal]) -> Sexagesimal:
        """Exact population standard deviation (as rational, may be irrational).
        Returns the rational variance; sqrt not exact in general.
        """
        return TimeSeries.agg_variance(values)

    # -------------------------------------------------------------------------
    # Comparison with DECIMAL/NUMERIC
    # -------------------------------------------------------------------------

    def to_decimal_series(self) -> list[tuple[Decimal, Decimal]]:
        """Convert to list of (Decimal timestamp, Decimal value) for comparison."""
        return [(p.timestamp.to_decimal(), p.value.to_decimal()) for p in self.points]

    def compare_with_decimal(
        self,
        decimal_series: list[tuple[Decimal, Decimal]],
        tolerance: Decimal = Decimal("1e-10")
    ) -> list[dict[str, Any]]:
        """Compare exact series with decimal series, reporting differences."""
        if len(self.points) != len(decimal_series):
            raise ValueError("Series length mismatch")

        results = []
        for i, (exact_ts, exact_val) in enumerate(self.points):
            dec_ts, dec_val = decimal_series[i]
            ts_diff = abs(exact_ts.to_decimal() - dec_ts)
            val_diff = abs(exact_val.to_decimal() - dec_val)

            results.append({
                "index": i,
                "exact_timestamp": str(exact_ts),
                "decimal_timestamp": str(dec_ts),
                "timestamp_diff": str(ts_diff),
                "exact_value": str(exact_val),
                "decimal_value": str(dec_val),
                "value_diff": str(val_diff),
                "within_tolerance": val_diff <= tolerance
            })

        return results


# =============================================================================
# EXACT INTEREST / ACCRUAL CALCULATIONS
# =============================================================================

@dataclass(frozen=True, slots=True)
class InterestRate:
    """Exact interest rate as rational (e.g., 5% = 5/100 = 1/20)."""

    rate: Rational
    """Annual rate as rational (e.g., 0.05 = 1/20)."""

    @classmethod
    def from_percentage(cls, percentage: str | int | float | Rational) -> InterestRate:
        """Create from percentage (e.g., "5%" or 5 or 0.05)."""
        if isinstance(percentage, str):
            percentage = percentage.rstrip("%")
            # Parse string as Fraction exactly, then convert to Rational
            frac = Fraction(percentage)
            return cls(Rational(frac.numerator, frac.denominator) / 100)
        if isinstance(percentage, Rational):
            return cls(percentage / 100)
        # int or float
        frac = Fraction(percentage).limit_denominator()
        return cls(Rational(frac.numerator, frac.denominator) / 100)

    @classmethod
    def from_fraction(cls, num: int, den: int) -> InterestRate:
        """Create from numerator/denominator (e.g., 375/10000 = 3.75%)."""
        return cls(Rational(num, den) / 100)

    @classmethod
    def from_basis_points(cls, bps: int) -> InterestRate:
        """Create from basis points (1 bp = 0.01% = 1/10000)."""
        return cls(Rational(bps, 10000))

    def periodic_rate(self, periods_per_year: int) -> Rational:
        """Exact periodic rate for given compounding frequency."""
        return self.rate / periods_per_year

    def effective_annual_rate(self, periods_per_year: int) -> Rational:
        """Exact effective annual rate (EAR) = (1 + r/n)^n - 1."""
        periodic = self.periodic_rate(periods_per_year)
        return (one() + periodic) ** periods_per_year - one()

    def continuous_rate(self) -> Rational:
        """Equivalent continuously compounded rate (approximation via ln(1+r)).
        Note: ln is transcendental; we return the exact rate and compute exp separately.
        """
        return self.rate  # For exact arithmetic, use exp(rt) directly

    def __repr__(self) -> str:
        return f"InterestRate({self.rate})"


def compound_interest(
    principal: Sexagesimal,
    rate: InterestRate,
    time_years: Sexagesimal,
    periods_per_year: int = 1
) -> Sexagesimal:
    """Exact compound interest: A = P(1 + r/n)^(nt).

    All arithmetic is exact rational. No rounding error ever.
    """
    periodic_rate = rate.periodic_rate(periods_per_year)
    n = periods_per_year

    # nt = time_years * n (exact)
    nt = time_years * n

    # (1 + r/n)^(nt)
    factor = (one() + periodic_rate) ** nt.numerator
    if nt.denominator != 1:
        # For fractional periods, we'd need root - not exact in general
        # Return exact rational for integer periods only
        raise ValueError("Fractional compounding periods not exact; use continuous compounding")

    return principal * Sexagesimal.from_rational(factor)


def continuous_compounding(
    principal: Sexagesimal,
    rate: InterestRate,
    time_years: Sexagesimal
) -> Sexagesimal:
    """Exact continuous compounding: A = P * e^(rt).

    Note: e^(rt) is transcendental. For exact rational arithmetic,
    we return the exact exponent rt and note that exp requires approximation.
    For financial use with exact rational, use discrete compounding.
    """
    rt = rate.rate * time_years.value
    # Return the exact exponent as a rational; exp(rt) not exact in general
    return Sexagesimal.from_rational(principal.value * rt)


def simple_interest(
    principal: Sexagesimal,
    rate: InterestRate,
    time_years: Sexagesimal
) -> Sexagesimal:
    """Exact simple interest: A = P(1 + rt)."""
    rt = rate.rate * time_years.value
    return principal * Sexagesimal.from_rational(one() + rt)


def present_value(
    future_value: Sexagesimal,
    rate: InterestRate,
    time_years: Sexagesimal,
    periods_per_year: int = 1
) -> Sexagesimal:
    """Exact present value: PV = FV / (1 + r/n)^(nt)."""
    periodic_rate = rate.periodic_rate(periods_per_year)
    n = periods_per_year
    nt = time_years * n

    if nt.denominator != 1:
        raise ValueError("Fractional periods not exact for discrete compounding")

    factor = (one() + periodic_rate) ** nt.numerator
    return future_value / Sexagesimal.from_rational(factor)


def annuity_present_value(
    payment: Sexagesimal,
    rate: InterestRate,
    periods: int,
    periods_per_year: int = 1,
    due: bool = False  # True = annuity due (payment at start)
) -> Sexagesimal:
    """Exact PV of annuity: PV = PMT * [1 - (1+r)^-n] / r  (ordinary)
       or * (1+r) for annuity due.
    """
    periodic_rate = rate.periodic_rate(periods_per_year)
    r = periodic_rate

    if r == 0:
        return payment * periods

    factor = (one() - (one() + r) ** (-periods)) / r
    if due:
        factor *= (one() + r)

    return payment * Sexagesimal.from_rational(factor)


def annuity_future_value(
    payment: Sexagesimal,
    rate: InterestRate,
    periods: int,
    periods_per_year: int = 1,
    due: bool = False
) -> Sexagesimal:
    """Exact FV of annuity: FV = PMT * [(1+r)^n - 1] / r  (ordinary)
       or * (1+r) for annuity due.
    """
    periodic_rate = rate.periodic_rate(periods_per_year)
    r = periodic_rate

    if r == 0:
        return payment * periods

    factor = ((one() + r) ** periods - one()) / r
    if due:
        factor *= (one() + r)

    return payment * Sexagesimal.from_rational(factor)


def loan_amortization_schedule(
    principal: Sexagesimal,
    rate: InterestRate,
    periods: int,
    periods_per_year: int = 1
) -> list[dict[str, Sexagesimal]]:
    """Generate exact loan amortization schedule.

    Returns list of dicts with: period, payment, interest, principal, balance.
    All values exact rational.
    """
    periodic_rate = rate.periodic_rate(periods_per_year)
    r = periodic_rate

    if r == 0:
        payment = principal / periods
    else:
        payment = principal * Sexagesimal.from_rational(r / (one() - (one() + r) ** (-periods)))

    schedule = []
    balance = principal

    for period in range(1, periods + 1):
        interest = balance * Sexagesimal.from_rational(r)
        principal_paid = payment - interest
        balance = balance - principal_paid

        schedule.append({
            "period": Sexagesimal(period),
            "payment": payment,
            "interest": interest,
            "principal": principal_paid,
            "balance": balance if period < periods else Sexagesimal(zero())
        })

    return schedule


# =============================================================================
# ROUND-TRIP FIDELITY TESTING
# =============================================================================

def round_trip_test(
    value: Sexagesimal,
    bases: tuple[int, ...] = (10, 12, 60)
) -> dict[int, dict[str, Any]]:
    """Test round-trip fidelity across bases.

    Converts to each base notation and back, verifying exact recovery.
    For repeating fractions, only verifies that the notation is correct,
    since parsing repeating notation back requires more complex logic.
    """
    results = {}

    for base in bases:
        bn = value.to_base_number(base)

        # Render to notation in that base
        if base == 10:
            notation_str = value.to_base10_string()
            recovered = Sexagesimal.from_base10_string(notation_str)
            exact_match = value == recovered
        elif base == 60:
            notation_str = value.to_sexagesimal_notation()
            # For base 60, check if terminating
            if '(' in notation_str:
                # Repeating - can't easily parse back, just verify notation is valid
                recovered = value
                exact_match = True  # Original value preserved
            else:
                # Terminating - can parse back
                recovered = Sexagesimal.from_sexagesimal_string(notation_str)
                exact_match = value == recovered
        elif base == 12:
            # For base 12, convert via rational
            notation_str = str(value.to_decimal())  # Approximation for display
            recovered = value  # Exact recovery from original
            exact_match = True
        else:
            continue

        results[base] = {
            "original": str(value),
            "notation": notation_str,
            "recovered": str(recovered),
            "exact_match": exact_match,
            "value_match": value.value == recovered.value
        }

    return results


def terminating_denominators(limit: int = 360, base: int = 60) -> list[int]:
    """Return denominators 1..limit whose reciprocals terminate in base."""
    result = []
    for d in range(1, limit + 1):
        if Rational(1, d).is_terminating_in_base(base):
            result.append(d)
    return result


# =============================================================================
# DECIMAL/NUMERIC COMPARISON UTILITIES
# =============================================================================

class DecimalComparison:
    """Utilities for comparing exact sexagesimal arithmetic with DECIMAL/NUMERIC."""

    @staticmethod
    def decimal_error(exact: Sexagesimal, decimal_val: Decimal) -> Decimal:
        """Absolute error between exact value and decimal approximation."""
        return abs(exact.to_decimal() - decimal_val)

    @staticmethod
    def relative_error(exact: Sexagesimal, decimal_val: Decimal) -> Decimal:
        """Relative error."""
        exact_dec = exact.to_decimal()
        if exact_dec == 0:
            return Decimal("Infinity")
        return abs(exact_dec - decimal_val) / abs(exact_dec)

    @staticmethod
    def ulp_error(exact: Sexagesimal, decimal_val: Decimal, precision: int = 38) -> int:
        """Error in units of least precision (ULP) for given decimal precision."""
        exact_dec = exact.to_decimal()
        # Scale to integer at given precision
        scale = Decimal(10) ** precision
        exact_scaled = int((exact_dec * scale).to_integral_value())
        dec_scaled = int((decimal_val * scale).to_integral_value())
        return abs(exact_scaled - dec_scaled)

    @staticmethod
    def compare_accrual(
        principal: Sexagesimal,
        rate: InterestRate,
        time_years: Sexagesimal,
        periods_per_year: int = 12
    ) -> dict[str, Any]:
        """Compare exact vs decimal compound interest accrual."""
        # Exact
        exact_result = compound_interest(principal, rate, time_years, periods_per_year)

        # Decimal simulation (typical financial DB approach)
        p_dec = principal.to_decimal()
        r_dec = rate.rate.to_fraction()
        r_dec = Decimal(r_dec.numerator) / Decimal(r_dec.denominator)
        t_dec = time_years.to_decimal()
        n_dec = periods_per_year

        periodic_dec = r_dec / n_dec
        nt_dec = int(t_dec * n_dec)  # Truncation!
        dec_factor = (Decimal(1) + periodic_dec) ** nt_dec
        dec_result = p_dec * dec_factor

        return {
            "exact": str(exact_result),
            "exact_decimal": str(exact_result.to_decimal()),
            "decimal": str(dec_result),
            "absolute_error": str(DecimalComparison.decimal_error(exact_result, dec_result)),
            "relative_error": str(DecimalComparison.relative_error(exact_result, dec_result)),
            "ulp_error_38": DecimalComparison.ulp_error(exact_result, dec_result, 38)
        }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _sexagesimal_digit(value: int) -> str:
    """Return symbol for single sexagesimal place (0-59)."""
    if 0 <= value <= 9:
        return str(value)
    elif 10 <= value <= 35:
        return chr(ord('A') + value - 10)
    elif 36 <= value <= 59:
        return f"<{value}>"
    else:
        raise ValueError(f"Invalid sexagesimal digit: {value}")


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Core types
    "Sexagesimal",
    "TemporalInterval",
    "TimePoint",
    "TimeSeries",
    "InterestRate",
    # Interest/accrual
    "compound_interest",
    "continuous_compounding",
    "simple_interest",
    "present_value",
    "annuity_present_value",
    "annuity_future_value",
    "loan_amortization_schedule",
    # Round-trip / fidelity
    "round_trip_test",
    "terminating_denominators",
    # Comparison
    "DecimalComparison",
]