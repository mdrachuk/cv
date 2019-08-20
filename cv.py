#!/usr/bin/env python
"""
This module is querying PyPI to check if the current version set to package is already present on PyPI.

Used during PR checks, to ensure that package version is changed.

Finishes with an VersionExists exception and a non-zero exit code if the version exists on PyPI.
"""
from __future__ import annotations

__version__ = '1.0.0.dev2'

from dataclasses import dataclass
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
    package_json = requests.get(f'https://pypi.org/pypi/{name}/json').text
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
                         f'You can change the version in "version.py".')


if __name__ == '__main__':
    # TODO:mdrachuk:2019-08-20: import version from provided module
    # TODO:mdrachuk:2019-08-20: add option to check version format
    # TODO:mdrachuk:2019-08-20: add version manipulation (increment..)
    check_unique('cv', __version__)
