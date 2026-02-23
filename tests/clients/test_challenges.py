import requests_mock

from berserk import Client
from berserk.types import ChallengeJson

from utils import validate


def test_show_calls_correct_path_and_returns_challenge():
    """Show sends GET to /api/challenge/{id}/show and returns typed challenge."""
    challenge_id = "abc123"
    url = f"https://lichess.org/api/challenge/{challenge_id}/show"
    mock_challenge: ChallengeJson = {
        "id": challenge_id,
        "url": "https://lichess.org/abc",
        "status": "created",
        "challenger": {"id": "u1", "name": "Alice"},
        "destUser": {"id": "u2", "name": "Bob"},
        "variant": {"key": "standard", "name": "Standard", "short": "std"},
        "rated": False,
        "speed": "rapid",
        "timeControl": {"limit": 600, "increment": 0},
        "color": "random",
        "finalColor": "white",
        "perf": {"icon": "r", "name": "Rapid"},
        "declineReason": "",
        "declineReasonKey": "",
    }
    with requests_mock.Mocker() as m:
        m.get(url, json=mock_challenge)
        res = Client().challenges.show(challenge_id)
    assert res["id"] == challenge_id
    assert res["status"] == "created"
    validate(ChallengeJson, res)
