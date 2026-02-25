import requests_mock

from berserk import Client


class TestUpdateChapterTags:
    def test_request_path_and_form_body(self):
        """Request hits correct path and sends form-encoded pgn body (204)."""
        pgn = '[Event "Test"]\n[Site "Lichess"]'
        with requests_mock.Mocker() as m:
            m.post(
                "https://lichess.org/api/study/abc123/chapter456/tags",
                status_code=204,
            )
            res = Client().studies.update_chapter_tags("abc123", "chapter456", pgn=pgn)
            assert res is None
            assert m.called
            assert m.call_count == 1
            assert m.last_request.method == "POST"
            assert (
                m.last_request.headers["Content-Type"]
                == "application/x-www-form-urlencoded"
            )
            assert (
                m.last_request.body
                == "pgn=%5BEvent+%22Test%22%5D%0A%5BSite+%22Lichess%22%5D"
            )
