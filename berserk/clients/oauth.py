from __future__ import annotations

from urllib.parse import urlencode, urljoin

from typing import Any, Dict

from .. import models
from .base import BaseClient


class OAuth(BaseClient):
    def authorization_url(
        self,
        client_id: str,
        redirect_uri: str,
        code_challenge: str,
        *,
        state: str | None = None,
        scope: str | None = None,
        username: str | None = None,
    ) -> str:
        """Build the OAuth2 authorization URL (GET /oauth) for the Authorization Code flow with PKCE.

        Redirect the user to the returned URL to start the flow. After they authorize,
        Lichess redirects to ``redirect_uri`` with a ``code`` and ``state`` in the query string.
        Exchange the code for an access token via the token endpoint.

        :param client_id: Arbitrary identifier that uniquely identifies your application.
        :param redirect_uri: Absolute URL Lichess will redirect to with the authorization result.
        :param code_challenge: BASE64URL(SHA256(code_verifier)). Keep code_verifier secret until token exchange.
        :param state: Optional state echoed back on redirect; use for CSRF protection.
        :param scope: Optional space-separated list of requested OAuth scopes.
        :param username: Optional hint for the user to log in with a specific Lichess username.
        :return: Full URL to send the user to for authorization.
        """
        params: Dict[str, str] = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
        }
        if state is not None:
            params["state"] = state
        if scope is not None:
            params["scope"] = scope
        if username is not None:
            params["username"] = username
        path = "/oauth"
        return urljoin(
            self._r.base_url.rstrip("/") + "/", path + "?" + urlencode(params)
        )

    def test_tokens(self, *tokens: str) -> Dict[str, Any]:
        """Test the validity of up to 1000 OAuth tokens.

        Valid OAuth tokens will be returned with their associated user ID and scopes.
        Invalid tokens will be returned as null.

        :param tokens: one or more OAuth tokens
        :return: info about the tokens
        """
        path = "/api/token/test"
        payload = ",".join(tokens)
        return self._r.post(path, data=payload, converter=models.OAuth.convert)
