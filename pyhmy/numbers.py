"""
Handles conversion of ONE to ATTO and vice versa
For more granular conversions, see Web3.toWei
"""

from decimal import Decimal

_conversion_unit = Decimal( 1e18 )


def convert_atto_to_one( atto ) -> Decimal:
    """Convert ATTO to ONE.

    Parameters
    ----------
    atto: str, int, float, decimal
        Value in ATTO to convert to ONE
        Float input will be truncated, since ATTO is the lowest possible denomination of ONE

    Returns
    -------
    decimal
        Converted value in ONE
    """
    if isinstance( atto, float ):
        atto = int( atto )
    return Decimal( atto ) / _conversion_unit


def convert_one_to_atto( one ) -> Decimal:
    """Convert ONE to ATTO.

    Parameters
    ----------
    one: str, int, float, decimal
        Value in ONE to convert to ATTO

    Returns
    -------
    decimal
        Converted value in ATTO
    """
    if isinstance( one, float ):
        one = str( one )
    return Decimal( one ) * _conversion_unit
