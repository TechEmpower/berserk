from __future__ import annotations

from urllib.parse import urljoin

from typing import Any, Dict

from .. import exceptions, models
from .base import BaseClient


class OAuth(BaseClient):
    def revoke(self) -> None:
        """Revoke the access token sent as Bearer (DELETE /api/token).

        The session must be authenticated with the token to revoke (e.g.
        ``TokenSession(access_token)``). After a successful call, the token
        is invalid and must not be used for further requests.

        :return: None. Raises if the request fails.
        """
        path = "/api/token"
        url = urljoin(self._r.base_url, path)
        response = self._r.session.request("DELETE", url)
        if not response.ok:
            raise exceptions.ResponseError(response)

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
