#!/usr/bin/env python
"""
This module is querying PyPI to check if the current version set to package is already present on PyPI.

Used during PR checks, to ensure that package version is changed.

Finishes with an VersionExists exception and a non-zero exit code if the version exists on PyPI.
"""
from __future__ import annotations

__version__ = '1.0.0.dev6'

import os
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from importlib import invalidate_caches, import_module
from typing import Dict, Set, List

import requests
from pkg_resources import safe_version
from serious import JsonModel


def check_unique(name: str, version: str):
    pypi_pkg = fetch(name)
    if pypi_pkg.contains_version(version):
        raise VersionExists(name, version)
    print(f'OK: {name} {version} is not present on PyPI.')


def fetch(name: str) -> PypiPackage:
    model = JsonModel(PypiPackage, allow_unexpected=True, allow_any=True)
    response = requests.get(f'https://pypi.org/pypi/{name}/json')
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise PypiError(name) from e
    package_json = response.text
    return model.load(package_json)


@dataclass
class PypiPackage:
    releases: Dict[str, List]

    @property
    def versions(self) -> Set[str]:
        return set(self.releases.keys())

    def contains_version(self, target: str) -> bool:
        target = safe_version(target)
        existing = {safe_version(version) for version in self.versions}
        return target in existing


class VersionExists(Exception):
    def __init__(self, name: str, version: str):
        super().__init__(f'Package "{name}" with version "{version}" already exists on PyPI. '
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
