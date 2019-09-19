import json
import threading
from contextlib import contextmanager
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
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


class WarehousePass(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"releases": {}}).encode(encoding='utf8'))

    def log_message(self, format, *args):
        pass


class WarehouseFail(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.NOT_FOUND)
        self.end_headers()

    def log_message(self, format, *args):
        pass


class ServerThread(threading.Thread):
    def __init__(self, server: HTTPServer):
        super().__init__()
        self.server = server

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


@contextmanager
def background_server(port, request_handler):
    test_server = HTTPServer(('localhost', port), request_handler)
    thread = ServerThread(test_server)
    thread.start()
    yield
    thread.stop()


def test_warehouse():
    with background_server(1337, WarehousePass):
        assert check_unique('cv', '1.0.0', 'http://localhost:1337') is None


def test_invalid_warehouse():
    with background_server(1337, WarehouseFail):
        with pytest.raises(PypiError):
            check_unique('cv', '1.0.0', 'http://localhost:1337')
