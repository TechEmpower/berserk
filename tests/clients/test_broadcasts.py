import pytest

from berserk import Client
from berserk.types import (
    BroadcastTop,
    BroadcastTournamentPlayer,
    PaginatedBroadcasts,
    BroadcastsByUser,
)
from utils import skip_if_older_3_dot_10, validate


class TestBroadcasts:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_top(self):
        res = Client().broadcasts.get_top(page=1, html=False)
        validate(BroadcastTop, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_search(self):
        res = Client().broadcasts.search(query="chess", page=1)
        validate(PaginatedBroadcasts, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_by_user(self):
        res = Client().broadcasts.get_by_user(username="lichess", page=1)
        validate(BroadcastsByUser, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_player(self):
        res = Client().broadcasts.get_player(
            broadcast_tournament_id="8jXzp45R", player_id="13401319"
        )
        validate(BroadcastTournamentPlayer, res)
