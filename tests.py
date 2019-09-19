from uuid import uuid4

import pytest

from cv import check_unique, VersionExists, main, PypiError, InvalidVersionFormat, check_version_format, \
    InvalidRequirements, VersionTypeMismatch


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
        main(['test_modules.invalid_format'])


def test_valid_alpha_main():
    assert main(['test_modules.valid_alpha', '--alpha', '--dry']) is None


def test_valid_beta_main():
    assert main(['test_modules.valid_beta', '--beta', '--dry']) is None


def test_valid_rc_main():
    assert main(['test_modules.valid_rc', '--rc', '--dry']) is None


def test_valid_dev_main():
    assert main(['test_modules.valid_dev', '--dev', '--dry']) is None


def test_valid_release_main():
    assert main(['test_modules.valid_release', '--release', '--dry']) is None


def test_restrict_invalid_combinations():
    with pytest.raises(InvalidRequirements):
        main(['test_modules.valid_release', '--release', '--dev'])
    with pytest.raises(InvalidRequirements):
        main(['test_modules.valid_release', '--release', '--alpha'])
    with pytest.raises(InvalidRequirements):
        main(['test_modules.valid_release', '--release', '--beta'])
    with pytest.raises(InvalidRequirements):
        main(['test_modules.valid_release', '--alpha', '--beta'])
    with pytest.raises(InvalidRequirements):
        main(['test_modules.valid_release', '--beta', '--rc'])
    with pytest.raises(InvalidRequirements):
        main(['test_modules.valid_release', '--rc', '--alpha'])


def test_invalid_version_type():
    with pytest.raises(VersionTypeMismatch):
        main(['test_modules.valid_dev', '--release', '--dry'])
    with pytest.raises(VersionTypeMismatch):
        main(['test_modules.valid_beta', '--alpha', '--dry'])
    with pytest.raises(VersionTypeMismatch):
        main(['test_modules.valid_release', '--dev', '--dry'])
