from flask import Blueprint, jsonify
from services.csv_data_service import get_all_teams, get_team_stats

teams_bp = Blueprint("teams", __name__, url_prefix="/api/teams")

@teams_bp.route("/", methods=["GET"])
def get_teams():
    """
    Get All Teams from CSV
    
    Loads all teams from teams.csv with complete team statistics:
    - Team identity (name, country, badge)
    - Performance metrics (matches played, wins, draws, losses)
    - Goals and defense (scored, conceded, clean sheets)
    - Tactical stats (possession, corners, cards, xG)
    - Player count and aggregate player stats
    
    All data is sourced exclusively from CSV files with no external API calls.
    ---
    tags:
      - Teams
    responses:
      200:
        description: List of all teams with comprehensive stats from CSV
        schema:
          type: array
          items:
            type: object
            properties:
              country:
                type: string
                example: Egypt
              name:
                type: string
                example: Egypt
              badge:
                type: string
              matches_played:
                type: integer
              wins:
                type: integer
              draws:
                type: integer
              losses:
                type: integer
              total_players:
                type: integer
              total_goals:
                type: integer
              total_assists:
                type: integer
    """
    # Load teams from CSV with aggregated stats
    teams = get_all_teams()
    
    # Convert numpy types and handle NaN values for JSON serialization
    import numpy as np
    import math
    
    def convert_value(v):
        if isinstance(v, (np.integer, np.int64)):
            return int(v)
        elif isinstance(v, (np.floating, np.float64)):
            if math.isnan(v) or math.isinf(v):
                return None
            return float(v)
        return v
    
    teams = [{k: convert_value(v) for k, v in team.items()} for team in teams]
    
    return jsonify(teams)



