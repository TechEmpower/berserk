from __future__ import annotations

from typing import Any, Dict, cast

from .. import models
from ..types import OAuthTokenResponse
from .base import BaseClient


class OAuth(BaseClient):
    def exchange_code(
        self,
        code: str,
        code_verifier: str,
        client_id: str,
        redirect_uri: str,
    ) -> OAuthTokenResponse:
        """Exchange an authorization code for an access token (POST /api/token).

        Call this after the user returns from the authorization URL with a ``code``
        in the redirect query string. Use the same ``code_verifier`` that was used
        to generate the ``code_challenge`` when building the authorization URL.

        :param code: The authorization code from the redirect_uri query string.
        :param code_verifier: The secret used to derive the code_challenge.
        :param client_id: Must match the client_id used to request the code.
        :param redirect_uri: Must match the redirect_uri used to request the code.
        :return: Token response with access_token, token_type, and expires_in.
        """
        path = "/api/token"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": code_verifier,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
        }
        return cast(
            OAuthTokenResponse,
            self._r.post(path, data=payload),
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
