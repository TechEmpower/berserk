from __future__ import annotations

from typing import Any, Dict, Iterator, List, cast

from ..formats import NDJSON, PGN
from ..types.common import Color, VariantKey
from ..types import ChapterIdName
from .base import BaseClient


class Studies(BaseClient):
    """Study chess the Lichess way."""

    def export_chapter(
        self,
        study_id: str,
        chapter_id: str,
        clocks: bool = True,
        comments: bool = True,
        variations: bool = True,
        source: bool = False,
        orientation: bool = False,
    ) -> str:
        """Export one chapter of a study.

        :param study_id: study id
        :param chapter_id: chapter id
        :param clocks: include any clock comments in the PGN moves
        :param comments: include any analysis and annotator comments in the PGN moves
        :param variations: include any variations in the PGN moves
        :param source: include a `Source` PGN tag containing the chapter URL
        :param orientation: include an `Orientation` PGN tag containing the chapter's board orientation
        :return: chapter PGN
        """
        path = f"/api/study/{study_id}/{chapter_id}.pgn"
        params = {
            "clocks": clocks,
            "comments": comments,
            "variations": variations,
            "source": source,
            "orientation": orientation,
        }
        return self._r.get(path, fmt=PGN, params=params)

    def export(
        self,
        study_id: str,
        clocks: bool = True,
        comments: bool = True,
        variations: bool = True,
        source: bool = False,
        orientation: bool = False,
    ) -> Iterator[str]:
        """Export all chapters of a study.

        :param study_id: study id
        :param clocks: include any clock comments in the PGN moves
        :param comments: include any analysis and annotator comments in the PGN moves
        :param variations: include any variations in the PGN moves
        :param source: for each chapter, include a `Source` PGN tag containing the chapter URL
        :param orientation: for each chapter, include an `Orientation` PGN tag containing the chapter's board orientation
        :return: iterator over all chapters as PGNs
        """
        path = f"/api/study/{study_id}.pgn"
        params = {
            "clocks": clocks,
            "comments": comments,
            "variations": variations,
            "source": source,
            "orientation": orientation,
        }
        yield from self._r.get(path, fmt=PGN, stream=True, params=params)

    def export_by_username(
        self,
        username: str,
        clocks: bool = True,
        comments: bool = True,
        variations: bool = True,
        source: bool = False,
        orientation: bool = False,
    ) -> Iterator[str]:
        """Export all chapters of all studies of a user in PGN format.

        If authenticated, then all public, unlisted, and private studies are included.

        If not, only public (non-unlisted) studies are included.

        :param username: the user whose studies will be exported
        :param clocks: include any clock comments in the PGN moves
        :param comments: include any analysis and annotator comments in the PGN moves
        :param variations: include any variations in the PGN moves
        :param source: for each chapter, include a `Source` PGN tag containing the chapter URL
        :param orientation: for each chapter, include an `Orientation` PGN tag containing the chapter's board orientation
        :return: iterator over all chapters as PGNs
        """
        path = f"/study/by/{username}/export.pgn"
        params = {
            "clocks": clocks,
            "comments": comments,
            "variations": variations,
            "source": source,
            "orientation": orientation,
        }
        yield from self._r.get(path, fmt=PGN, stream=True, params=params)

    def import_pgn(
        self,
        study_id: str,
        chapter_name: str,
        pgn: str,
        orientation: Color = "white",
        variant: VariantKey = "standard",
    ) -> List[ChapterIdName]:
        """Imports an arbitrary PGN into an existing study.
        Creates a new chapter in the study.

        If the PGN contains multiple games (separated by 2 or more newlines) then multiple chapters will be created within the study.

        Note that a study can contain at most 64 chapters.

        return: List of the chapters {id, name}"""
        # https://lichess.org/api/study/{studyId}/import-pgn
        path = f"/api/study/{study_id}/import-pgn"
        payload = {
            "name": chapter_name,
            "pgn": pgn,
            "orientation": orientation,
            "variant": variant,
        }
        # The return is of the form:
        return cast(
            List[ChapterIdName], self._r.post(path, data=payload).get("chapters", [])
        )

    def update_chapter_tags(self, study_id: str, chapter_id: str, pgn: str) -> None:
        """Update PGN tags of a study chapter.

        Add, update, or delete PGN tags by providing PGN text (only the tag
        lines are used; moves are ignored). Omitted tags are left unchanged.

        :param study_id: study id (8 characters)
        :param chapter_id: chapter id (8 characters)
        :param pgn: PGN text containing the tags to set
        :return: None (API returns 204 No Content on success)
        """
        path = f"/api/study/{study_id}/{chapter_id}/tags"
        self._r.post(path, data={"pgn": pgn})

    def get_by_user(self, username: str) -> Iterator[Dict[str, Any]]:
        """
        Get metadata (name and dates) of all studies of a user.

        If authenticated, then all public, unlisted, and private studies are
        included. If not, only public (non-unlisted) studies are included.
        Studies are streamed as ndjson.

        return:iterator over all studies as ndjson
        """

        path = f"/api/study/by/{username}"
        yield from self._r.get(path, fmt=NDJSON, stream=True)
