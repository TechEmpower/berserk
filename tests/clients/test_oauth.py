from urllib.parse import parse_qs

import pytest
import requests_mock

from berserk import Client
from berserk.types import OAuthTokenResponse

from utils import validate, skip_if_older_3_dot_10


class TestOAuthExchangeCode:
    @skip_if_older_3_dot_10
    def test_exchange_code_response(self):
        """Verify that the response matches OAuthTokenResponse."""
        token_response = {
            "token_type": "Bearer",
            "access_token": "lio_abc123",
            "expires_in": 31536000,
        }
        with requests_mock.Mocker() as m:
            m.post(
                "https://lichess.org/api/token",
                json=token_response,
            )
            res = Client().oauth.exchange_code(
                code="auth_code_xyz",
                code_verifier="verifier_secret",
                client_id="my-app",
                redirect_uri="https://example.com/callback",
            )
        validate(OAuthTokenResponse, res)
        assert res["access_token"] == "lio_abc123"
        assert res["token_type"] == "Bearer"
        assert res["expires_in"] == 31536000

    def test_exchange_code_sends_form_data(self):
        """Verify the client sends grant_type, code, code_verifier, client_id, redirect_uri."""
        with requests_mock.Mocker() as m:
            m.post(
                "https://lichess.org/api/token",
                json={"token_type": "Bearer", "access_token": "x", "expires_in": 0},
            )
            Client().oauth.exchange_code(
                code="c",
                code_verifier="v",
                client_id="client",
                redirect_uri="https://e.com/cb",
            )
            assert m.call_count == 1
            req = m.last_request
            assert req.method == "POST"
            form = parse_qs(req.body)
            assert form["grant_type"] == ["authorization_code"]
            assert form["code"] == ["c"]
            assert form["code_verifier"] == ["v"]
            assert form["client_id"] == ["client"]
            assert form["redirect_uri"] == ["https://e.com/cb"]
