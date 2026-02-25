import pytest
import requests_mock

from berserk import Client, PuzzleBatchResponse, PuzzleData
from utils import validate, skip_if_older_3_dot_10


class TestPuzzles:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_next(self):
        """Validate that the response matches the typed-dict"""
        res = Client().puzzles.get_next(angle="anastasiaMate", difficulty="hardest")
        validate(PuzzleData, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_batch(self):
        """Validate that the batch response matches the typed-dict"""
        res = Client().puzzles.get_batch("opening", nb=1)
        validate(PuzzleBatchResponse, res)

    def test_get_batch_params(self):
        """Verify that difficulty, nb, and color are passed correctly in query params."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://lichess.org/api/puzzle/batch/mix?difficulty=hardest&nb=2&color=white",
                json={"puzzles": []},
            )
            Client().puzzles.get_batch("mix", difficulty="hardest", nb=2, color="white")
