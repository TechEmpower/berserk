import requests_mock

from berserk import Client


def test_export_games_hits_correct_path_and_params():
    """Verify export_games requests GET /api/bulk-pairing/{id}/games with params."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://lichess.org/api/bulk-pairing/5IrD6Gzz/games",
            text='[Event "?"]\n\n1. e4 e5 1-0\n\n',
        )
        client = Client()
        result = list(
            client.bulk_pairings.export_games(
                "5IrD6Gzz",
                as_pgn=True,
                moves=False,
                tags=False,
            )
        )
        assert len(result) >= 1
        request = m.request_history[0]
        assert request.path_url.startswith("/api/bulk-pairing/5IrD6Gzz/games")
        assert request.qs["moves"] == ["false"]
        assert request.qs["tags"] == ["false"]
