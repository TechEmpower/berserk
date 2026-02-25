import pytest
import requests_mock
from typing import List

from berserk import ArenaResult, Client, SwissResult
from berserk.types import ArenaTournamentPlayed
from berserk.types.tournaments import TeamBattleResult
from utils import skip_if_older_3_dot_10, validate


class TestLichessGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_swiss_result(self):
        res = list(Client().tournaments.stream_swiss_results("ADAHHiMX", limit=3))
        validate(List[SwissResult], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_arenas_result(self):
        res = list(Client().tournaments.stream_results("hallow23", limit=3))
        validate(List[ArenaResult], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_arenas_result_with_sheet(self):
        res = list(Client().tournaments.stream_results("hallow23", sheet=True, limit=3))
        validate(List[ArenaResult], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_team_standings(self):
        res = Client().tournaments.get_team_standings("Qv0dRqml")
        validate(TeamBattleResult, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_played(self):
        res = Client().tournaments.get_played("thibault", nb=3)
        validate(List[ArenaTournamentPlayed], res)

    def test_get_played_params(self):
        """Verify that nb and performance query params are passed correctly."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://lichess.org/api/user/foo/tournament/played?nb=5&performance=true",
                content=b"",
            )
            Client().tournaments.get_played("foo", nb=5, performance=True)
