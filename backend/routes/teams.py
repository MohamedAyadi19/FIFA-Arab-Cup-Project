from flask import Blueprint, jsonify
from services.db_data_service import get_all_teams, get_team_stats

teams_bp = Blueprint("teams", __name__, url_prefix="/api/teams")

@teams_bp.route("/", methods=["GET"])
def get_teams():
    """
    Get All Teams from Database
    
    Loads all teams from teams.csv with complete team statistics:
    - Team identity (name, country, badge)
    - Performance metrics (matches played, wins, draws, losses)
    - Goals and defense (scored, conceded, clean sheets)
    - Tactical stats (possession, corners, cards, xG)
    - Player count and aggregate player stats
    
    All data is sourced from the relational database.
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
    # Load teams from database with aggregated stats
    teams = get_all_teams()
    
    return jsonify(teams)



