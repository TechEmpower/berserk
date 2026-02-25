import requests_mock

import berserk


class TestOAuthRevoke:
    def test_revoke_sends_delete_with_bearer_token(self):
        """Verify the client sends DELETE /api/token with Authorization Bearer."""
        with requests_mock.Mocker() as m:
            m.delete("https://lichess.org/api/token", status_code=204)
            session = berserk.TokenSession("my_access_token")
            client = berserk.Client(session=session)
            client.oauth.revoke()
            assert m.call_count == 1
            req = m.last_request
            assert req.method == "DELETE"
            assert req.headers.get("Authorization") == "Bearer my_access_token"
