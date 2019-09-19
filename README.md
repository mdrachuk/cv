# cv
[![PyPI](https://img.shields.io/pypi/v/cv)][pypi]
[![Downloads](https://img.shields.io/pypi/dm/cv)][pypi]
[![Build Status](https://img.shields.io/azure-devops/build/misha-drachuk/cv/9)](https://dev.azure.com/misha-drachuk/cv/_build/latest?definitionId=9&branchName=master)
[![Test Coverage](https://img.shields.io/coveralls/github/mdrachuk/cv/master)](https://coveralls.io/github/mdrachuk/cv)
[![Supported Python](https://img.shields.io/pypi/pyversions/cv)][pypi]

Check version of a Python module.

Raises an error if the `<module>.__version__`:
- already present on PyPI; 
- does not match [PEP 440](https://www.python.org/dev/peps/pep-0440);
- or does not match specified type: alpha/beta/rc/dev/release.

All of this comes in handy during CI. 

Also: No runtime dependencies!

## Installation
Available from [PyPI][pypi]:
```shell
pip install cv
```

## Module Example
With a \<module\> present on PyPI and `<module>.py` in current directory:
```python
__version__ = '7.7.7'

...
```

Simply run:
```shell
cv <module>
```

If `7.7.7` version of \<module\> is on PyPI already you’ll get a `VersionExists` error:
```plain
Traceback (most recent call last):
  File "./cv", line 86, in <module>
    main(sys.argv[1:])
  File "./cv", line 82, in main
    check_unique(name, version)
  File "./cv", line 28, in check_unique
    raise VersionExists(name, version)
__main__.VersionExists: Package "<module>" with version "7.7.7" already exists on PyPI.
Change the "<module>.__version__" to fix this error.
```

## Package Example
Packages work in the same way as modules except `__version__` is defined in `<module>/__init__.py`


## Help
```shell
$ cv --help
usage: cv [-h] [-w WAREHOUSE] [--alpha] [--beta] [--rc] [--dev] [--release]
          [--dry]
          module

Check version of a Python package or module.

positional arguments:
  module                the package/module with "__version__" defined

optional arguments:
  -h, --help            show this help message and exit
  -w WAREHOUSE, --warehouse WAREHOUSE
                        package index to use, default is
                        "https://pypi.org/pypi"
  --alpha               check that version is an alpha, e.g. 1.0.0a1
  --beta                check that version is a beta, e.g. 1.0.0b2
  --rc                  check that version is a release candidate, e.g.
                        1.0.0rc
  --dev                 check that version is in development, e.g. 1.0.0.dev3
  --release             check that version is a release without modifiers,
                        e.g. 1.0.0
  --dry                 make no request to PyPI
```

[pypi]: https://pypi.org/project/cv/