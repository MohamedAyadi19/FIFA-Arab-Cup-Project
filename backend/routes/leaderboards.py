from flask import Blueprint, jsonify, request
from services.db_data_service import get_leaderboard, get_all_teams

leaderboards_bp = Blueprint("leaderboards", __name__, url_prefix="/api/leaderboards")


@leaderboards_bp.route("/top-scorers", methods=["GET"])
def get_top_scorers():
    """
    Get Top Scorers Leaderboard from Database
    
    Loads top scorers from the relational database, sorted by goals_overall.
    ---
    tags:
      - Leaderboards
    parameters:
      - name: limit
        in: query
        type: integer
        default: 10
        example: 10
    responses:
      200:
        description: Top scorers leaderboard from CSV
        schema:
          type: object
          properties:
            leaderboard:
              type: array
              items:
                type: object
                properties:
                  rank:
                    type: integer
                  full_name:
                    type: string
                  goals_overall:
                    type: number
                  assists_overall:
                    type: number
                  Current Club:
                    type: string
    """
    limit = request.args.get('limit', 10, type=int)
    leaderboard = get_leaderboard('goals_overall', limit=limit)
    return jsonify({"leaderboard": leaderboard})


@leaderboards_bp.route("/top-assists", methods=["GET"])
def get_top_assists():
    """
    Get Top Assists Leaderboard from Database
    
    Loads top assist providers from the relational database, sorted by assists_overall.
    ---
    tags:
      - Leaderboards
    parameters:
      - name: limit
        in: query
        type: integer
        default: 10
        example: 10
    responses:
      200:
        description: Top assists leaderboard from CSV
        schema:
          type: object
          properties:
            leaderboard:
              type: array
              items:
                type: object
                properties:
                  rank:
                    type: integer
                  full_name:
                    type: string
                  assists_overall:
                    type: number
                  goals_overall:
                    type: number
                  Current Club:
                    type: string
    """
    limit = request.args.get('limit', 10, type=int)
    leaderboard = get_leaderboard('assists_overall', limit=limit)
    return jsonify({"leaderboard": leaderboard})


@leaderboards_bp.route("/top-defenders", methods=["GET"])
def get_top_defenders():
    """
    Get Top Defenders Leaderboard from Database
    
    Loads top defenders from the relational database, filtered by position and sorted by tackles_per_90_overall.
    ---
    tags:
      - Leaderboards
    parameters:
      - name: limit
        in: query
        type: integer
        default: 10
        example: 10
    responses:
      200:
        description: Top defenders leaderboard from CSV
        schema:
          type: object
          properties:
            leaderboard:
              type: array
              items:
                type: object
                properties:
                  rank:
                    type: integer
                  full_name:
                    type: string
                  tackles_per_90_overall:
                    type: number
                  clean_sheets_overall:
                    type: number
                  position:
                    type: string
                  Current Club:
                    type: string
    """
    limit = request.args.get('limit', 10, type=int)
    leaderboard = get_leaderboard('tackles_per_90_overall', limit=limit, player_type='Defender')
    return jsonify({"leaderboard": leaderboard})


@leaderboards_bp.route("/standings", methods=["GET"])
def get_standings():
    """
    Get Team Standings from Database
    
    Loads team standings from database, sorted by points/performance.
    Includes team performance metrics (wins, draws, losses, goals, clean sheets).
    ---
    tags:
      - Leaderboards
    responses:
      200:
        description: Team standings from CSV
        schema:
          type: object
          properties:
            standings:
              type: array
              items:
                type: object
                properties:
                  position:
                    type: integer
                  country:
                    type: string
                  matches_played:
                    type: integer
                  wins:
                    type: integer
                  draws:
                    type: integer
                  losses:
                    type: integer
                  goals_scored:
                    type: integer
                  goals_conceded:
                    type: integer
                  clean_sheets:
                    type: integer
    """
    teams = get_all_teams()
    
    # Sort by wins (descending) and points
    sorted_teams = sorted(
        teams,
        key=lambda t: (t.get('wins', 0), t.get('points', 0)),
        reverse=True
    )
    
    standings = []
    for idx, team in enumerate(sorted_teams, 1):
        standings.append({
            'position': idx,
            'country': team.get('country'),
            'name': team.get('name'),
            'matches_played': team.get('matches_played', 0),
            'wins': team.get('wins', 0),
            'draws': team.get('draws', 0),
            'losses': team.get('losses', 0),
            'goals_scored': team.get('goals_scored', 0),
            'goals_conceded': team.get('goals_conceded', 0),
            'clean_sheets': team.get('clean_sheets', 0),
            'points': team.get('points', 0),
        })
    
    return jsonify({"standings": standings})
