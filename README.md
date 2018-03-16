# scrycli
[![PyPI](https://img.shields.io/pypi/l/scrycli.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/PolarPayne/scrycli.svg?branch=master)](https://travis-ci.org/PolarPayne/scrycli)
[![PyPI](https://img.shields.io/pypi/v/scrycli.svg)](https://pypi.python.org/pypi/scrycli)
[![PyPI](https://img.shields.io/pypi/pyversions/scrycli.svg)][![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPolarPayne%2Fscrycli.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FPolarPayne%2Fscrycli?ref=badge_shield)
()

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
  * for search
  * for set command


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FPolarPayne%2Fscrycli.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FPolarPayne%2Fscrycli?ref=badge_large)