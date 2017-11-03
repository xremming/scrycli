# scrycli
[![PyPI](https://img.shields.io/pypi/l/scrycli.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/PolarPayne/scrycli.svg?branch=master)](https://travis-ci.org/PolarPayne/scrycli)
[![PyPI](https://img.shields.io/pypi/v/scrycli.svg)](https://pypi.python.org/pypi/scrycli)
[![PyPI](https://img.shields.io/pypi/pyversions/scrycli.svg)]()

## What
CLI for [scryfall](https://scryfall.com/).

## Installation
Install through pip with `pip install scrycli`.
Should work with python 3.4 and newer.

I personally recommend to also add `alias scry="scrycli search"` to make
searching extra easy.

### Autocompletion
Autocompletion is currently supported only on bash. Enable it by adding
`eval "$(_SCRYCLI_COMPLETE=source-bash scrycli)"` to your `.bashrc`.

## Todo
* Support for different output formats (start is already in \_\_main\_\_.py)
* better autocomplete
* list sets, list cards in set
