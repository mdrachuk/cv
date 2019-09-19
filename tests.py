from uuid import uuid4

import pytest

from cv import check_unique, VersionExists, main, PypiError, InvalidVersionFormat, check_version_format


def test_non_existing():
    with pytest.raises(PypiError):
        assert check_unique(f'cv-{uuid4()}', '1.0.0') is None


def test_unique():
    assert check_unique('cv', '99.0.0') is None


def test_not_unique():
    with pytest.raises(VersionExists):
        check_unique('cv', '1.0.0.dev8')


def test_invalid_version_format():
    with pytest.raises(InvalidVersionFormat):
        check_version_format('cv', '1.0.0.beta1')


def test_valid_version_format():
    check_version_format('cv', '1.0.0b1')


def test_valid_main():
    assert main(['cv']) is None


def test_invalid_format_main():
    with pytest.raises(InvalidVersionFormat):
        main(['invalid_format'])
