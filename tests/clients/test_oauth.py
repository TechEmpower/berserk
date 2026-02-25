from urllib.parse import parse_qs, urlparse

import pytest

from berserk import Client


class TestOAuthAuthorizationUrl:
    def test_authorization_url_contains_required_params(self):
        """Required query params are present in the built URL."""
        url = Client().oauth.authorization_url(
            client_id="my-app",
            redirect_uri="https://example.com/callback",
            code_challenge="challenge123",
        )
        parsed = urlparse(url)
        assert parsed.path.rstrip("/").endswith("/oauth")
        qs = parse_qs(parsed.query)
        assert qs["response_type"] == ["code"]
        assert qs["client_id"] == ["my-app"]
        assert qs["redirect_uri"] == ["https://example.com/callback"]
        assert qs["code_challenge_method"] == ["S256"]
        assert qs["code_challenge"] == ["challenge123"]

    def test_authorization_url_optional_params(self):
        """Optional state, scope, and username appear when provided."""
        url = Client().oauth.authorization_url(
            client_id="my-app",
            redirect_uri="https://example.com/cb",
            code_challenge="c",
            state="xyz",
            scope="email:read preference:read",
            username="myuser",
        )
        qs = parse_qs(urlparse(url).query)
        assert qs["state"] == ["xyz"]
        assert qs["scope"] == ["email:read preference:read"]
        assert qs["username"] == ["myuser"]

    def test_authorization_url_omits_optional_params_when_none(self):
        """Optional params are omitted when not passed."""
        url = Client().oauth.authorization_url(
            client_id="a",
            redirect_uri="https://e.com/cb",
            code_challenge="x",
        )
        qs = parse_qs(urlparse(url).query)
        assert "state" not in qs
        assert "scope" not in qs
        assert "username" not in qs
