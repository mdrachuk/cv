import pytest

from cv import check_unique, VersionExists, main, PypiError


def test_non_existing():
    with pytest.raises(PypiError):
        assert check_unique('cv-cv-cv-cv-cv-cv-cv', '1.0.0') is None


def test_unique():
    assert check_unique('serious', '99.0.0') is None


def test_not_unique():
    with pytest.raises(VersionExists):
        check_unique('serious', '1.0.0.dev10')


def test_main():
    assert main(['cv']) is None
