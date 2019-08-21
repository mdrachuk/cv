# cv
[![PyPI](https://img.shields.io/pypi/v/cv)][pypi]
[![Build Status](https://img.shields.io/azure-devops/build/misha-drachuk/cv/9)](https://dev.azure.com/misha-drachuk/cv/_build/latest?definitionId=9&branchName=master)
[![Test Coverage](https://img.shields.io/coveralls/github/mdrachuk/cv/master)](https://coveralls.io/github/mdrachuk/cv)
[![Supported Python](https://img.shields.io/pypi/pyversions/cv)][pypi]

Check version of a Python module.

Queries PyPI and looks for the `<module>.__version__` among all available versions.
Raises an error if the version already exists.

Comes useful during CI PR checks.

## Installation
Available from [PyPI][pypi]:
```shell
pip install cv
```

## Module Example
With a "module" present on PyPI and `module.py` in current directory:
```python
__version__ = '7.7.7'

...
```

Simply run:
```shell
cv module
```

If `7.7.7` version of `module` is on PyPI already you’ll get a `VersionExists` error:
```plain
Traceback (most recent call last):
  File "./cv", line 86, in <module>
    main(sys.argv[1:])
  File "./cv", line 82, in main
    check_unique(name, version)
  File "./cv", line 28, in check_unique
    raise VersionExists(name, version)
__main__.VersionExists: Package "module" with version "7.7.7" already exists on PyPI. Change the "module.__version__" to fix this error.
```

## Package Example
Packages work in the same way as modules except `__version__` is defined in `module/__init__.py`

[pypi]: https://pypi.org/project/cv/