from flask import Blueprint, jsonify
from services.db_data_service import get_all_matches

matches_bp = Blueprint("matches", __name__, url_prefix="/api/matches")

@matches_bp.route("/", methods=["GET"])
def get_matches():
    """
    Get All Matches from Database
    
    Loads all matches from matches.csv with complete match context:
    - Match details (date, home team, away team, venue, referee)
    - Match results (goals, shots, xG, cards, attendance)
    - League context (average goals, BTTS %, clean sheet % from league.csv)
    
    All data is sourced from the relational database.
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
    # Load matches from database
    matches = get_all_matches()
    return jsonify(matches)
