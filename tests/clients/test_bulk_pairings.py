import requests_mock

from berserk import Client


def test_export_games_hits_correct_path_and_params():
    """Verify export_games requests GET /api/bulk-pairing/{id}/games with params."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://lichess.org/api/bulk-pairing/5IrD6Gzz/games?moves=True&pgnInJson=False&tags=True&clocks=True&evals=False&accuracy=False&opening=True&division=False&literate=False",
            text='[Event "?"]\n\n1. e4 e5 1-0\n\n',
        )
        client = Client()
        list(
            client.bulk_pairings.export_games(
                "5IrD6Gzz",
                as_pgn=True,
                moves=True,
                pgn_in_json=False,
                tags=True,
                clocks=True,
                evals=False,
                accuracy=False,
                opening=True,
                division=False,
                literate=False,
            )
        )


def test_export_games_as_ndjson_returns_dicts():
    """Verify export_games with as_pgn=False requests NDJSON and yields game dicts."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://lichess.org/api/bulk-pairing/5IrD6Gzz/games?moves=False&pgnInJson=False&tags=False&clocks=False&evals=False&accuracy=False&opening=False&division=False&literate=False",
            text='{"id":"abc123","rated":false}\n',
        )
        client = Client()
        result = list(
            client.bulk_pairings.export_games(
                "5IrD6Gzz",
                as_pgn=False,
                moves=False,
                pgn_in_json=False,
                tags=False,
                clocks=False,
                evals=False,
                accuracy=False,
                opening=False,
                division=False,
                literate=False,
            )
        )
        assert len(result) == 1
        assert result[0]["id"] == "abc123"
        assert result[0]["rated"] is False
