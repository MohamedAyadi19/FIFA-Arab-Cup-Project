from flask import Blueprint, jsonify, request
from services.db_data_service import get_all_players


players_bp = Blueprint("players", __name__, url_prefix="/api/players")

@players_bp.route("/", methods=["GET"])
def get_players():
    """
    Get All Players with Position-Aware Stats
    
    Loads players from the relational database with position-aware stats.
    Each player receives position-relevant statistics:
    - Goalkeepers: clean_sheets, saves_per_game, save_percentage, conceded_per_90
    - Defenders: clean_sheets, tackles_per_90, interceptions, aerial_duels, blocks, clearances
    - Midfielders: passes_per_90, key_passes, chances_created, tackles, goals, assists
    - Forwards: goals, assists, shots_on_target, dribbles, xG metrics
    
    Query Parameters:
    - team: Filter by team/country name
    - position: Filter by position (Goalkeeper, Defender, Midfielder, Forward)
    ---
    tags:
      - Players
    parameters:
      - name: team
        in: query
        type: string
        description: Filter players by team/country name
        enum: [Egypt, Algeria, Morocco, Tunisia, Saudi Arabia, Oman, Comoros, Palestine, Libya, Syria, South Sudan, Bahrain, Djibouti, Somalia, Yemen, Lebanon, Sudan, Qatar, Kuwait, Jordan, UAE, Iraq]
        example: Egypt
      - name: position
        in: query
        type: string
        description: Filter by position category
        enum: [Goalkeeper, Defender, Midfielder, Forward]
        example: Forward
    responses:
      200:
        description: List of all players with position-aware stats from CSV
        schema:
          type: array
          items:
            type: object
            properties:
              full_name:
                type: string
                example: Mohamed Salah
              position:
                type: string
                example: Forward
              player_type:
                type: string
                example: Forward
              nationality:
                type: string
                example: Egypt
              Current Club:
                type: string
                example: Egypt
              goals_overall:
                type: number
                example: 47
              assists_overall:
                type: number
                example: 18
    """
    team_filter = request.args.get('team', '').lower()
    position_filter = request.args.get('position', '').lower()
    
    # Load all players from the database with position-aware stats
    players = get_all_players()
    
    # Apply team filter if specified (filter by nationality, not club)
    if team_filter:
        players = [p for p in players if (p.get('nationality') or '').lower() == team_filter]
    
    # Apply position filter if specified
    if position_filter:
        players = [p for p in players if (p.get('position') or '').lower() == position_filter]
    
    return jsonify(players)

