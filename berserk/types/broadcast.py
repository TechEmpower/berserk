from __future__ import annotations

from typing import Dict, List

from typing_extensions import NotRequired, TypedDict

from .common import LightUser, Title


class BroadcastPlayer(TypedDict):
    # The name of the player as it appears on the source PGN
    source_name: str
    # The name of the player as it will be displayed on Lichess
    display_name: str
    # Rating, optional
    rating: NotRequired[int]
    # Title, optional
    title: NotRequired[Title]


class BroadcastTourInfo(TypedDict):
    website: NotRequired[str]
    players: NotRequired[str]
    location: NotRequired[str]
    tc: NotRequired[str]
    fideTc: NotRequired[str]
    timeZone: NotRequired[str]
    standings: NotRequired[str]
    format: NotRequired[str]


class BroadcastTour(TypedDict):
    id: str
    name: str
    slug: str
    createdAt: int
    dates: NotRequired[List[int]]
    info: NotRequired[BroadcastTourInfo]
    tier: NotRequired[int]
    image: NotRequired[str]
    description: NotRequired[str]
    leaderboard: NotRequired[bool]
    teamTable: NotRequired[bool]
    url: str
    communityOwner: NotRequired[LightUser]


class BroadcastCustomPointsPerColor(TypedDict):
    win: float
    draw: float


class BroadcastCustomScoring(TypedDict):
    white: BroadcastCustomPointsPerColor
    black: BroadcastCustomPointsPerColor


class BroadcastRoundInfo(TypedDict):
    id: str
    name: str
    slug: str
    createdAt: int
    rated: bool
    ongoing: NotRequired[bool]
    startsAt: NotRequired[int]
    startsAfterPrevious: NotRequired[bool]
    finishedAt: NotRequired[int]
    finished: NotRequired[bool]
    url: NotRequired[str]
    delay: NotRequired[int]
    customScoring: NotRequired[BroadcastCustomScoring]


class BroadcastWithLastRound(TypedDict):
    group: NotRequired[str]
    tour: BroadcastTour
    round: BroadcastRoundInfo
    roundToLink: NotRequired[BroadcastRoundInfo]


class PaginatedBroadcasts(TypedDict):
    currentPage: int
    maxPerPage: int
    currentPageResults: List[BroadcastWithLastRound]
    previousPage: NotRequired[int | None]
    nextPage: NotRequired[int | None]


class BroadcastTop(TypedDict):
    active: List[BroadcastWithLastRound]
    upcoming: List[None]  # deprecated
    past: PaginatedBroadcasts


class BroadcastByUser(TypedDict):
    tour: BroadcastTour


class BroadcastsByUser(TypedDict):
    currentPage: int
    maxPerPage: int
    currentPageResults: List[BroadcastByUser]
    nbResults: int
    previousPage: int | None
    nextPage: int | None
    nbPages: int


class BroadcastTournamentPlayerOpponent(TypedDict):
    name: str
    title: NotRequired[str]
    rating: NotRequired[int]
    fideId: NotRequired[int]
    team: NotRequired[str]
    fed: NotRequired[str]


class BroadcastTournamentPlayerGame(TypedDict):
    round: str
    id: str
    opponent: BroadcastTournamentPlayerOpponent
    color: str
    fideTC: NotRequired[str]
    points: str
    ratingDiff: NotRequired[int]


class BroadcastTournamentPlayerFideRatings(TypedDict):
    standard: NotRequired[int]
    rapid: NotRequired[int]
    blitz: NotRequired[int]


class BroadcastTournamentPlayerFide(TypedDict):
    year: NotRequired[int]
    ratings: NotRequired[BroadcastTournamentPlayerFideRatings]
    follow: NotRequired[bool]


class BroadcastTournamentPlayer(TypedDict):
    """A single player in a broadcast tournament (GET /broadcast/{id}/players/{playerId})."""

    name: str
    title: NotRequired[str]
    rating: NotRequired[int]
    fideId: NotRequired[int]
    team: NotRequired[str]
    fed: NotRequired[str]
    played: NotRequired[int]
    score: NotRequired[float]
    ratingDiff: NotRequired[int]
    ratingsMap: NotRequired[Dict[str, int]]
    ratingDiffs: NotRequired[Dict[str, int]]
    performance: NotRequired[int]
    performances: NotRequired[Dict[str, int]]
    fide: NotRequired[BroadcastTournamentPlayerFide]
    games: NotRequired[List[BroadcastTournamentPlayerGame]]
