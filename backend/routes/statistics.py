"""
League and team statistics endpoints.
All data is sourced exclusively from CSV files with no external API calls.
"""

from flask import Blueprint, jsonify
from services.csv_data_service import get_league_stats, get_team_stats, CSVDataService


statistics_bp = Blueprint("statistics", __name__, url_prefix="/api/statistics")


@statistics_bp.route("/league", methods=["GET"])
def get_league_statistics():
    """
    Get League-Wide Statistics from CSV
    
    Loads aggregated league statistics from league.csv including:
    - Match aggregates: average goals per match, BTTS percentage, clean sheet percentage
    - Goal distribution: time-based goal patterns
    - Tactical stats: average corners, cards, xG metrics
    - Performance metrics: win/draw/loss distribution
    
    All data is sourced exclusively from CSV files with no external API calls.
    ---
    tags:
      - Statistics
    responses:
      200:
        description: Comprehensive league statistics
        schema:
          type: object
          properties:
            average_goals_per_match:
              type: number
              example: 2.38
            btts_percentage:
              type: number
              example: 49
            clean_sheets_percentage:
              type: number
              example: 67
            average_corners_per_match:
              type: number
              example: 8.77
            average_cards_per_match:
              type: number
              example: 3.03
            xg_avg_per_match:
              type: number
              example: 2.31
    """
    league_stats = get_league_stats()
    return jsonify(league_stats)


@statistics_bp.route("/league/summary", methods=["GET"])
def get_league_summary():
    """
    Get League Summary from CSV
    
    Returns a concise summary of key league-wide metrics for dashboard display.
    ---
    tags:
      - Statistics
    responses:
      200:
        description: League summary statistics
        schema:
          type: object
          properties:
            total_matches:
              type: integer
            total_goals:
              type: integer
            avg_goals_per_match:
              type: number
            clean_sheet_percentage:
              type: number
            both_teams_scored_percentage:
              type: number
    """
    league_stats = get_league_stats()
    
    summary = {
        'average_goals_per_match': league_stats.get('average_goals_per_match', 0),
        'clean_sheet_percentage': league_stats.get('clean_sheets_percentage', 0),
        'both_teams_scored_percentage': league_stats.get('btts_percentage', 0),
        'average_corners': league_stats.get('average_corners_per_match', 0),
        'average_cards': league_stats.get('average_cards_per_match', 0),
        'average_xg': league_stats.get('xg_avg_per_match', 0),
    }
    
    return jsonify(summary)


@statistics_bp.route("/teams/<team_name>", methods=["GET"])
def get_team_statistics(team_name):
    """
    Get Team Statistics from CSV
    
    Loads team statistics from teams.csv with:
    - Team performance (matches, wins, draws, losses)
    - Goals and defense (scored, conceded, clean sheets)
    - Tactical metrics (possession, corners, cards, xG)
    - Player aggregate stats (total players, goals, assists)
    - League context for comparison
    
    All data is sourced exclusively from CSV files.
    ---
    tags:
      - Statistics
    parameters:
      - name: team_name
        in: path
        type: string
        required: true
        enum: [Egypt, Algeria, Morocco, Tunisia, Saudi Arabia, Oman, Comoros, Palestine, Libya, Syria, South Sudan, Bahrain, Djibouti, Somalia, Yemen, Lebanon, Sudan, Qatar, Kuwait, Jordan, UAE, Iraq]
        example: Egypt
    responses:
      200:
        description: Comprehensive team statistics
        schema:
          type: object
          properties:
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
            total_players:
              type: integer
            avg_player_rating:
              type: number
      404:
        description: Team not found
    """
    team_stats = get_team_stats(team_name)
    
    if not team_stats:
        return jsonify({"error": f"Team '{team_name}' not found"}), 404
    
    return jsonify(team_stats)


@statistics_bp.route("/comparison/<team1>/<team2>", methods=["GET"])
def compare_teams(team1, team2):
    """
    Compare Two Teams with Differential Analysis
    
    Compares statistics between two teams from CSV data with computed differentials.
    Helpful for match preview analysis and head-to-head comparison.
    ---
    tags:
      - Statistics
    parameters:
      - name: team1
        in: path
        type: string
        required: true
        enum: [Egypt, Algeria, Morocco, Tunisia, Saudi Arabia, Oman, Comoros, Palestine, Libya, Syria, South Sudan, Bahrain, Djibouti, Somalia, Yemen, Lebanon, Sudan, Qatar, Kuwait, Jordan, UAE, Iraq]
        example: Egypt
      - name: team2
        in: path
        type: string
        required: true
        enum: [Egypt, Algeria, Morocco, Tunisia, Saudi Arabia, Oman, Comoros, Palestine, Libya, Syria, South Sudan, Bahrain, Djibouti, Somalia, Yemen, Lebanon, Sudan, Qatar, Kuwait, Jordan, UAE, Iraq]
        example: Morocco
    responses:
      200:
        description: Detailed comparison between two teams with analysis
        schema:
          type: object
          properties:
            team1:
              type: object
              properties:
                name:
                  type: string
                points:
                  type: integer
                wins:
                  type: integer
                goals_scored:
                  type: integer
                goals_conceded:
                  type: integer
            team2:
              type: object
            comparison:
              type: object
              properties:
                points_difference:
                  type: integer
                leader:
                  type: string
                better_attack:
                  type: string
                better_defense:
                  type: string
      404:
        description: One or both teams not found
    """
    stats1 = get_team_stats(team1)
    stats2 = get_team_stats(team2)
    
    if not stats1 or not stats2:
        return jsonify({"error": "One or both teams not found"}), 404
    
    # Calculate comparative metrics (calculate points from wins/draws)
    wins1 = stats1.get('wins', 0)
    draws1 = stats1.get('draws', 0)
    wins2 = stats2.get('wins', 0)
    draws2 = stats2.get('draws', 0)
    
    pts1 = wins1 * 3 + draws1
    pts2 = wins2 * 3 + draws2
    gf1 = stats1.get('goals_scored', 0)
    gf2 = stats2.get('goals_scored', 0)
    ga1 = stats1.get('goals_conceded', 0)
    ga2 = stats2.get('goals_conceded', 0)
    
    return jsonify({
        "team1": {
            "name": team1,
            "stats": stats1
        },
        "team2": {
            "name": team2,
            "stats": stats2
        },
        "comparison": {
            "points_difference": abs(pts1 - pts2),
            "leader": team1 if pts1 > pts2 else (team2 if pts2 > pts1 else "Equal"),
            "goal_difference_advantage": team1 if (gf1 - ga1) > (gf2 - ga2) else (team2 if (gf2 - ga2) > (gf1 - ga1) else "Equal"),
            "better_attack": team1 if gf1 > gf2 else (team2 if gf2 > gf1 else "Equal"),
            "better_defense": team1 if ga1 < ga2 else (team2 if ga2 < ga1 else "Equal"),
            "goal_spread": {
                "team1_for_against": f"{int(gf1)}:{int(ga1)}",
                "team2_for_against": f"{int(gf2)}:{int(ga2)}"
            },
            "team1_points": pts1,
            "team2_points": pts2
        }
    })
