import pytest

from typing import List

from berserk import Client
from berserk.types import (
    BroadcastTeamStandingsItem,
    BroadcastTop,
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
    def test_get_team_standings(self):
        """Get team leaderboard for a broadcast.

        A broadcast is a Lichess relay of an external chess event (OTB/online);
        it has a tour (tournament) and rounds with games. Standings exist when
        the tour is a team event (tour.teamTable is true) and teams are assigned
        (e.g. via WhiteTeam/BlackTeam in PGN or manual assignment). To find
        broadcasts with non-empty standings: get_top() or search(), filter for
        tour.teamTable, then call get_team_standings(tour.id) until len > 0.
        This test uses a broadcast that has team standings (e.g. German
        Bundesliga). Re-record if it later returns [] (delete cassette, make
        test_record, or pick another tour.id from get_top with teamTable).
        """
        res = Client().broadcasts.get_team_standings("Y9YjcDKG")
        validate(List[BroadcastTeamStandingsItem], res)
