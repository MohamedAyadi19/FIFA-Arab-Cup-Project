from flask import Blueprint, jsonify
from services.sportsdb_service import fetch_players_by_team, save_players_to_db
from models import Team, Player
from auth_utils import token_required
import time


players_bp = Blueprint("players", __name__, url_prefix="/api/players")

@players_bp.route("/sync", methods=["POST"])
@token_required
def sync_players():
    # Arab Cup countries only
    arab_cup_countries = [
        "Qatar", "Tunisia", "Syria", "Palestine", "Morocco", "Saudi Arabia", "Oman", "Comoros",
        "Egypt", "Jordan", "United Arab Emirates", "Kuwait", "Algeria", "Iraq", "Bahrain", "Sudan"
    ]
    
    teams = Team.query.filter(Team.country.in_(arab_cup_countries)).all()
    total = 0

    for team in teams:
        players = fetch_players_by_team(team.team_id)
        if players:
            count = save_players_to_db(players, team)
            total += count
            print(f"Synced {count} new players for team: {team.name}")
        else:
            print(f"No new players found for team: {team.name} (ID: {team.team_id})")
        time.sleep(2)  # Respect API rate limit (free tier: 1 req per 2 seconds)

    return jsonify({"status": "players synced", "count": total, "note": "Data merged with existing records"})



@players_bp.route("/", methods=["GET"])
def get_players():
    players = Player.query.all()
    return jsonify([
        {
            "name": p.name,
            "position": p.position,
            "nationality": p.nationality,
            "team_id": p.team_id,
            "team": Team.query.get(p.team_id).country if p.team_id and Team.query.get(p.team_id) else "Unknown"
        } for p in players
    ])
