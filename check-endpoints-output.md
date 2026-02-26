# Old output:

Missing endpoints:

/api/board/game/{gameId}/claim-draw
/api/bot/game/{gameId}/claim-draw
/api/bot/game/{gameId}/claim-victory
/api/broadcast/round/{broadcastRoundId}/reset
/api/bulk-pairing/{id}/games
/api/challenge/{challengeId}/show
/api/fide/player/{playerId}/ratings
/api/games/export/bookmarks
/api/puzzle/batch/{angle}
/api/puzzle/replay/{days}/{theme}
/api/racer/{id}
/api/study/by/{username}/export.pgn
/api/study/{studyId}/{chapterId}/tags
/api/user/{username}/note
/api/user/{username}/tournament/played
/broadcast/{broadcastTournamentId}/players
/broadcast/{broadcastTournamentId}/players/{playerId}
/broadcast/{broadcastTournamentId}/teams/standings
/oauth
https://tablebase.lichess.ovh/antichess
https://tablebase.lichess.ovh/atomic
https://tablebase.lichess.ovh/standard

(those tablebase endpoints are false positives, but the script isn't correctly filtering them out)

# New output:

Exit codes: 0 = no missing; 1 = has missing endpoints or params; 2 = error (e.g. spec file not found).

Missing (path, operation):

  /api/board/game/{gameId}/claim-draw  POST
  /api/bot/game/{gameId}/chat  GET
  /api/bot/game/{gameId}/claim-draw  POST
  /api/bot/game/{gameId}/claim-victory  POST
  /api/broadcast/round/{broadcastRoundId}/reset  POST
  /api/broadcast/{broadcastTournamentSlug}/{broadcastRoundSlug}/{broadcastRoundId}  GET
  /api/bulk-pairing/{id}  GET
  /api/bulk-pairing/{id}/games  GET
  /api/challenge/{challengeId}/show  GET
  /api/fide/player/{playerId}/ratings  GET
  /api/games/export/bookmarks  GET
  /api/puzzle/batch/{angle}  GET
  /api/puzzle/batch/{angle}  POST
  /api/puzzle/replay/{days}/{theme}  GET
  /api/racer/{id}  GET
  /api/study/by/{username}/export.pgn  GET
  /api/study/{studyId}/{chapterId}  DELETE
  /api/study/{studyId}/{chapterId}/tags  POST
  /api/token  DELETE
  /api/token  POST
  /api/tournament/{id}  POST
  /api/user/{username}/note  GET
  /api/user/{username}/note  POST
  /api/user/{username}/tournament/played  GET
  /broadcast/{broadcastTournamentId}/players  GET
  /broadcast/{broadcastTournamentId}/players/{playerId}  GET
  /broadcast/{broadcastTournamentId}/teams/standings  GET

Missing query params (implemented endpoints):

  /api/broadcast  GET  missing params: ['html']  (berserk/clients/broadcasts.py: Broadcasts.get_official)
  /api/games/export/_ids  POST  missing params: ['accuracy', 'division', 'literate', 'pgnInJson']  (berserk/clients/games.py: Games.export_multi)
  /api/games/user/{username}  GET  missing params: ['accuracy', 'division', 'lastFen', 'withBookmarked']  (berserk/clients/games.py: Games.export_by_player)
  /api/puzzle/activity  GET  missing params: ['since']  (berserk/clients/puzzles.py: Puzzles.get_puzzle_activity)
  /api/puzzle/next  GET  missing params: ['color']  (berserk/clients/puzzles.py: Puzzles.get_next)
  /api/swiss/{id}/games  GET  missing params: ['accuracy', 'division', 'moves', 'player']  (berserk/clients/tournaments.py: Tournaments.export_swiss_games)
  /api/team/{teamId}/arena  GET  missing params: ['createdBy', 'name', 'status']  (berserk/clients/tournaments.py: Tournaments.arenas_by_team)
  /api/team/{teamId}/swiss  GET  missing params: ['createdBy', 'name', 'status']  (berserk/clients/tournaments.py: Tournaments.swiss_by_team)
  /api/tournament/{id}/games  GET  missing params: ['accuracy', 'division', 'pgnInJson', 'player']  (berserk/clients/tournaments.py: Tournaments.export_arena_games)
  /api/user/{username}/current-game  GET  missing params: ['accuracy', 'division']  (berserk/clients/games.py: Games.export_ongoing_by_player)
  /api/user/{username}/tournament/created  GET  missing params: ['status']  (berserk/clients/tournaments.py: Tournaments.tournaments_by_user)
  /game/export/{gameId}  GET  missing params: ['accuracy', 'division', 'withBookmarked']  (berserk/clients/games.py: Games.export)
  https://explorer.lichess.ovh/player  GET  missing params: ['modes']  (berserk/clients/opening_explorer.py: OpeningExplorer.stream_player_games)

  JSON output (with `--json`; see exit codes above):

  {
  "missing_endpoints": [
    {
      "path": "/api/board/game/{gameId}/claim-draw",
      "operation": "POST"
    },
    ...
  ],
  "missing_params": [
    {
      "path": "/api/broadcast",
      "operation": "GET",
      "params": [
        "html"
      ],
      "method": "berserk/clients/broadcasts.py: Broadcasts.get_official"
    },
    ...
  ]
}