import pytest

from cv import check_unique, VersionExists


def test_unique():
    assert check_unique('serious', '99.0.0') is None


def test_not_unique():
    with pytest.raises(VersionExists):
        check_unique('serious', '1.0.0.dev10')
