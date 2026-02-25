from __future__ import annotations

from typing_extensions import TypedDict


class OAuthTokenResponse(TypedDict):
    """Response from POST /api/token (OAuth2 token exchange)."""

    token_type: str
    access_token: str
    expires_in: int
