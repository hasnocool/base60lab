"""Tests for fractions domain — delegates all base-specific arithmetic to engines."""

from base60lab.core.rational import Rational
from base60lab.core.types import BaseNumber
from base60lab.core.unknowns import UnknownsRegistry
from base60lab.engines import Base10Engine, Base12Engine, Base60Engine
from base60lab.domains.fractions import FractionsDomain


def test_domain_creation():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)
    assert domain.engines == engines


def test_reciprocal_delegates_to_engine():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)

    # 1/3 in base 12 terminates as "0.4"
    result = domain.reciprocal(3, 12)
    assert isinstance(result, BaseNumber)
    assert result.base == 12
    assert engines[12].to_rational(result) == Rational(1, 3)

    notation = engines[12].to_notation(result)
    assert notation.text == "0.4"
    assert notation.repeating is None


def test_reciprocal_base60_terminating():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)

    # 1/5 in base 60 terminates (place value 12, rendered "0;C")
    result = domain.reciprocal(5, 60)
    assert engines[60].to_rational(result) == Rational(1, 5)

    notation = engines[60].to_notation(result)
    assert notation.repeating is None


def test_reciprocal_base10_repeating():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)

    # 1/7 repeats in base 10
    result = domain.reciprocal(7, 10)
    notation = engines[10].to_notation(result)
    assert notation.repeating is not None


def test_division_delegates_to_engine():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)

    a = engines[10].from_rational(Rational(1))
    b = engines[10].from_rational(Rational(3))
    result = domain.divides(a, b)
    assert engines[10].to_rational(result) == Rational(1, 3)
    assert result.base == 10


def test_is_terminating():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)

    assert domain.is_terminating(2, 10) is True
    assert domain.is_terminating(5, 10) is True
    assert domain.is_terminating(3, 10) is False
    assert domain.is_terminating(3, 12) is True
    assert domain.is_terminating(3, 60) is True
    assert domain.is_terminating(5, 60) is True
    assert domain.is_terminating(7, 60) is False


def test_repeating_period():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)

    assert domain.repeating_period(3, 10) == 1
    assert domain.repeating_period(7, 10) == 6
    assert domain.repeating_period(5, 12) is not None


def test_terminating_count():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)

    result = domain.terminating_count(360)
    assert 10 in result
    assert 12 in result
    assert 60 in result

    # Base 10: denominators with only factors 2 and 5 terminate
    assert 2 in result[10]
    assert 5 in result[10]
    assert 10 in result[10]
    assert 3 not in result[10]
    assert 7 not in result[10]

    # Base 12: denominators with only factors 2 and 3 terminate
    assert 2 in result[12]
    assert 3 in result[12]
    assert 4 in result[12]
    assert 5 not in result[12]

    # Base 60: denominators with only factors 2, 3, 5 terminate
    assert 2 in result[60]
    assert 3 in result[60]
    assert 5 in result[60]
    assert 7 not in result[60]


def test_compare_reciprocal_all_bases():
    engines = {
        10: Base10Engine(),
        12: Base12Engine(),
        60: Base60Engine(),
    }
    domain = FractionsDomain(engines)

    result = domain.compare_reciprocal(3)
    assert 10 in result
    assert 12 in result
    assert 60 in result
    assert result[12] == "0.4"  # 1/3 terminates in base 12


def test_domain_uses_engines_not_reimplemented():
    """Verify domain delegates to engines rather than re-implementing per-base logic."""
    engines = {
        10: Base10Engine(UnknownsRegistry()),
        12: Base12Engine(UnknownsRegistry()),
        60: Base60Engine(UnknownsRegistry()),
    }
    domain = FractionsDomain(engines)

    # Domain should use engine's from_rational/to_rational/to_notation
    result = domain.reciprocal(4, 12)
    assert result.base == 12
    notation = engines[12].to_notation(result)
    assert notation.text == "0.3"  # 1/4 in base 12


