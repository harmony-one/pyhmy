from pyhmy.bech32 import bech32


def test_encode():
    bech32.encode( "one", 5, [ 121, 161 ] )


def test_decode():
    bech32.decode( "one", "one1a0x3d6xpmr6f8wsyaxd9v36pytvp48zckswvv9" )
