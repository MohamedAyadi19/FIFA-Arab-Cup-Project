from flask import Blueprint, jsonify
from services.csv_data_service import get_all_matches

matches_bp = Blueprint("matches", __name__, url_prefix="/api/matches")

@matches_bp.route("/", methods=["GET"])
def get_matches():
    """
    Get All Matches from CSV
    
    Loads all matches from matches.csv with complete match context:
    - Match details (date, home team, away team, venue, referee)
    - Match results (goals, shots, xG, cards, attendance)
    - League context (average goals, BTTS %, clean sheet % from league.csv)
    
    All data is sourced exclusively from CSV files with no external API calls.
    ---
    tags:
      - Matches
    responses:
      200:
        description: List of all matches with context from CSV
        schema:
          type: array
          items:
            type: object
            properties:
              date:
                type: string
                example: 2021-11-30
              home_team:
                type: string
                example: Qatar
              away_team:
                type: string
                example: Bahrain
              home_score:
                type: integer
                example: 1
              away_score:
                type: integer
                example: 0
              venue:
                type: string
                example: Al Bayt Stadium
              league_avg_goals:
                type: number
                example: 2.38
              league_btts_percentage:
                type: number
                example: 49
    """
    # Load matches from CSV with league context
    matches = get_all_matches()
    
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
    
    matches = [{k: convert_value(v) for k, v in match.items()} for match in matches]
    
    return jsonify(matches)
