# Pyhmy - Harmony's python utilities

**This library only supports Python 3.6+**

A Python library for interacting and working the [Harmony blockchain](https://harmony.one/)
and [related codebases](https://github.com/harmony-one).

[Full documentation is located on Harmony's GitBook](https://docs.harmony.one/) (in progress).

## Installation

```
pip install pyhmy

On MacOS:

Make sure you have Python3 installed, and use python3 to install pyhmy

sudo pip3 install pathlib
sudo pip3 install pyhmy
```

## Development

Clone the repository and then run the following:
```
make install
```

## Running tests

You need to run a local Harmony blockchain (instructions [here](https://github.com/harmony-one/harmony/blob/main/README.md)) that has staking enabled.
You can run all of the tests with the following:

```
make test
```

Or directly with `pytest` (reference [here](https://docs.pytest.org/en/latest/index.html) for more info):

```
py.test tests
```

## Releasing

You can release this library with the following command (assuming you have the credentials to upload):

```
make release
```

TODO: sample of how to use the library, reference Tezos.
TODO: start (and finish) some of the documentation.
TODO: add more blockchain rpcs
TODO: check None return types for rpcs
TODO: more detailed tests for rpcs
