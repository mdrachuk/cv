#!/usr/bin/env python
"""
This module is querying PyPI to check if the current version set to package is already present on PyPI.

Used during PR checks, to ensure that package version is changed.

Finishes with an VersionExists exception and a non-zero exit code if the version exists on PyPI.
"""
from __future__ import annotations

import json
from urllib.error import HTTPError
from urllib.request import urlopen

__version__ = '1.0.0.dev9'

import os
import sys
from argparse import ArgumentParser
from importlib import invalidate_caches, import_module
from typing import List

from pkg_resources import safe_version


def check_unique(name: str, version: str):
    try:
        response = urlopen(f'https://pypi.org/pypi/{name}/json')
    except HTTPError as e:
        raise PypiError(name) from e
    data = json.loads(response.read())
    versions = set(data['releases'].keys())
    if safe_version(version) in versions:
        raise VersionExists(name, version)
    print(f'OK: {name} {version} is not present on PyPI.')


class VersionExists(Exception):
    def __init__(self, name: str, version: str):
        super().__init__(f'Package "{name}" with version "{version}" already exists on PyPI.{os.linesep}'
                         f'Change the "{name}.__version__" or "{name}.__init__.__version__" to fix this error.')


class PypiError(Exception):
    def __init__(self, name: str):
        super().__init__(f'Package "{name}" could not be fetched from PyPI. ')


parser = ArgumentParser(description='Check version of a Python package or module.')
parser.add_argument('module', type=str, help='the package/module to check')


def _parse_args(args: List[str]):
    parameters = parser.parse_args(args)
    module_name = parameters.module
    module = _resolve_module(module_name)
    return module_name, module.__version__


def _resolve_module(module_name: str):
    """Black magic. Prevents loading a package from cv dependencies."""
    invalidate_caches()
    old_module = sys.modules.pop(module_name, None)
    module = import_module(module_name)
    if old_module:
        sys.modules[module_name] = old_module
    return module


def main(args):
    name, version = _parse_args(args)
    check_unique(name, version)


if __name__ == '__main__':
    sys.path.insert(0, os.getcwd())
    main(sys.argv[1:])
