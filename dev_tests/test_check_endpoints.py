"""Unit tests for check-endpoints.py (dev tool). Not run by make test.

Run manually: uv run pytest dev_tests/test_check_endpoints.py -v
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

# Load check-endpoints.py (hyphen in name) as a module
_ROOT = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "check_endpoints", _ROOT / "check-endpoints.py"
)
assert _SPEC is not None and _SPEC.loader is not None
check_endpoints = importlib.util.module_from_spec(_SPEC)
sys.modules["check_endpoints"] = check_endpoints
_SPEC.loader.exec_module(check_endpoints)


class TestNormalizePathTemplate:
    def test_leading_slash_added(self):
        assert check_endpoints.normalize_path_template("api/games") == "/api/games"

    def test_trailing_slash_removed(self):
        assert check_endpoints.normalize_path_template("/api/games/") == "/api/games"

    def test_placeholder_collapsed(self):
        assert check_endpoints.normalize_path_template("/api/game/{id}") == "/api/game/{}"
        assert check_endpoints.normalize_path_template("/api/{gameId}/claim") == "/api/{}/claim"

    def test_query_stripped(self):
        assert check_endpoints.normalize_path_template("/api?page=1") == "/api"
        assert check_endpoints.normalize_path_template("/api?page=1&foo=bar") == "/api"

    def test_unchanged_when_already_normalized(self):
        assert check_endpoints.normalize_path_template("/api/games") == "/api/games"


class TestQueryParamKeysFromPath:
    def test_no_query_returns_empty(self):
        assert check_endpoints.query_param_keys_from_path("/api") == set()
        assert check_endpoints.query_param_keys_from_path(None) == set()
        assert check_endpoints.query_param_keys_from_path("") == set()

    def test_single_param(self):
        assert check_endpoints.query_param_keys_from_path("/api?page=1") == {"page"}

    def test_multiple_params(self):
        assert check_endpoints.query_param_keys_from_path("/api?a=1&b=2") == {"a", "b"}


class TestSpecQueryParams:
    def test_empty_path_item(self):
        assert check_endpoints.spec_query_params({}, "get") == set()

    def test_operation_level_query_params(self):
        path_item = {
            "get": {
                "parameters": [
                    {"name": "page", "in": "query"},
                    {"name": "Accept", "in": "header"},
                ]
            }
        }
        assert check_endpoints.spec_query_params(path_item, "get") == {"page"}

    def test_path_level_and_operation_merged(self):
        path_item = {
            "parameters": [{"name": "common", "in": "query"}],
            "get": {"parameters": [{"name": "page", "in": "query"}]},
        }
        assert check_endpoints.spec_query_params(path_item, "get") == {"common", "page"}


class TestSpecPathOperations:
    def test_yields_path_and_operation(self):
        spec = {
            "paths": {
                "/api/games": {"get": {}},
                "/api/user": {"get": {}, "post": {}},
            }
        }
        out = list(check_endpoints.spec_path_operations(spec))
        assert ("/api/games", spec["paths"]["/api/games"], "get") in out
        assert ("/api/user", spec["paths"]["/api/user"], "get") in out
        assert ("/api/user", spec["paths"]["/api/user"], "post") in out
        assert len(out) == 3


class TestFalsePositives:
    def test_expected_paths_excluded(self):
        assert "/oauth" in check_endpoints.FALSE_POSITIVES
        assert "/standard" in check_endpoints.FALSE_POSITIVES
        assert "/atomic" in check_endpoints.FALSE_POSITIVES
        assert "/antichess" in check_endpoints.FALSE_POSITIVES
