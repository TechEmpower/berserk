import requests_mock

from berserk import Client


class TestGamesExportBookmarks:
    """Test client-side behavior for export_bookmarks (auth required)."""

    def test_export_bookmarks_path_and_params(self):
        """Request hits correct path and query params are passed."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://lichess.org/api/games/export/bookmarks?max=10&since=1609459200000&sort=dateDesc&until=1640995200000",
                content=b'{"id":"abc123"}\n',
            )
            list(
                Client().games.export_bookmarks(
                    since=1609459200000,
                    until=1640995200000,
                    max=10,
                    sort="dateDesc",
                )
            )
