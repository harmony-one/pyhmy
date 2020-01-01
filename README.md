# Pyhmy - Harmony's python utilities

**This library is for python 3 only.** 

[Full documentation is located on Harmony's GitBook](https://harmony.one/) (in progress).

A Python library for interacting and working the [Harmony blockchain](https://harmony.one/) 
and [related codebases](https://github.com/harmony-one).

## Installation
```bash
pip install pyhmy
```

## Development
Clone the repository and then run the following:
```bash
make install
```
(Optional) Copy over the CLI binary into `<pyhmy_repo_directory>/bin/`. Reference 
[here](https://app.gitbook.com/@harmony-one/s/home/command-line-interface/using-the-harmony-cli-tool) 
for more details on the Harmony CLI. *Note that this library comes with a function (under the `pyhmy.utils`) 
to download the statically linked CLI for Linux and MacOS*.

## Running tests

You can run all of the tests with the following:

```bash
make test
```

## Releasing

You can release this library with the following command (assuming you have credentials to upload):

```bash
make release
```