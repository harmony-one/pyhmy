"""Mock-based unit tests for numbers module."""
from decimal import Decimal

from pyhmy import numbers


def test_convert_one_to_atto():
    result = numbers.convert_one_to_atto(1)
    assert result == Decimal("1000000000000000000")


def test_convert_one_to_atto_decimal():
    result = numbers.convert_one_to_atto(Decimal("0.5"))
    assert result == Decimal("500000000000000000")


def test_convert_one_to_atto_string():
    result = numbers.convert_one_to_atto("2.5")
    assert result == Decimal("2500000000000000000")


def test_convert_atto_to_one():
    result = numbers.convert_atto_to_one(10**18)
    assert result == Decimal("1")


def test_convert_atto_to_one_large():
    result = numbers.convert_atto_to_one(10**20)
    assert result == Decimal("100")


def test_convert_atto_to_one_zero():
    result = numbers.convert_atto_to_one(0)
    assert result == Decimal("0")


def test_convert_atto_to_one_small():
    result = numbers.convert_atto_to_one(1)
    assert result == Decimal("0.000000000000000001")


def test_roundtrip():
    original = Decimal("42.5")
    atto = numbers.convert_one_to_atto(original)
    back = numbers.convert_atto_to_one(atto)
    assert back == original
