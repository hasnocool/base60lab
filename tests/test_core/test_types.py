"""Tests for core types (BaseNumber, Expression, Notation, Function)."""

from base60lab.core.rational import Rational
from base60lab.core.types import BaseNumber, Expression, Notation, Function, NotationSystem


def test_base_number_equality_base_independent():
    assert BaseNumber(Rational(1, 2), 10) == BaseNumber(Rational(1, 2), 12)
    assert BaseNumber(Rational(1, 2), 10) != BaseNumber(Rational(1, 3), 10)


def test_base_number_invalid_base():
    try:
        BaseNumber(Rational(1), 7)
        assert False, "should have raised ValueError"
    except ValueError:
        pass


def test_base_number_is_terminating():
    assert BaseNumber(Rational(1, 2), 10).is_terminating() is True
    assert BaseNumber(Rational(1, 3), 10).is_terminating() is False
    assert BaseNumber(Rational(1, 3), 12).is_terminating() is True
    assert BaseNumber(Rational(1, 3), 60).is_terminating() is True


def test_base_number_with_base():
    bn = BaseNumber(Rational(1, 2), 10)
    bn12 = bn.with_base(12)
    assert bn12.base == 12
    assert bn12 == bn  # same value, different base -> equal


def test_expression_not_evaluated():
    expr = Expression("add", (1, 2))
    assert expr.evaluated() is False


def test_expression_evaluated():
    expr = Expression("add", (1, 2), value=Rational(3))
    assert expr.evaluated() is True


def test_notation_terminating():
    n = Notation(base=10, digits=("0","1"), fractional_point=".", text="0.5", repeating=None)
    assert n.is_terminating() is True

    n2 = Notation(base=10, digits=("0","1"), fractional_point=".", text="0.(3)", repeating=2)
    assert n2.is_terminating() is False


def test_function_call():
    f = Function("add", 2, evaluate=lambda x, y: x + y)
    assert f.call(Rational(1), Rational(2)) == Rational(3)


def test_function_no_evaluator():
    f = Function("unknown", 1)
    try:
        f.call(Rational(1))
        assert False, "should have raised NotImplementedError"
    except NotImplementedError:
        pass


def test_notation_system_enum():
    assert NotationSystem.DECIMAL.value == 10
    assert NotationSystem.DUODECIMAL.value == 12
    assert NotationSystem.SEXAGESIMAL.value == 60
