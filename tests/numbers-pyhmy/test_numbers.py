from decimal import Decimal

import pytest

from pyhmy import (
    numbers
)


@pytest.mark.run(order=1)
def test_convert_atto_to_one():
    a = numbers.convert_atto_to_one(1e18)
    assert Decimal(1) == a

    b = numbers.convert_atto_to_one(1e18 + 0.6)
    assert Decimal(1) == b

    c = numbers.convert_atto_to_one('1' + ('0' * 18))
    assert Decimal(1) == c

    d = numbers.convert_atto_to_one(Decimal(1e18))
    assert Decimal(1) == d

@pytest.mark.run(order=2)
def test_convert_one_to_atto():
    a = numbers.convert_one_to_atto(1e-18)
    assert Decimal(1) == a

    b = numbers.convert_one_to_atto(1.5)
    assert Decimal(1.5e18) == b

    c = numbers.convert_one_to_atto('1')
    assert Decimal(1e18) == c

    d = numbers.convert_one_to_atto(Decimal(1))
    assert Decimal(1e18) == d
