from flask import Blueprint, jsonify
from auth_utils import token_required
from services.sportsdb_service import fetch_teams, save_teams_to_db
from models import Team

teams_bp = Blueprint("teams", __name__, url_prefix="/api/teams")

@teams_bp.route("/sync", methods=["POST"])
@token_required
def sync_teams():
    teams = fetch_teams()
    saved_count = save_teams_to_db(teams)
    return jsonify({"status": "teams synced", "count": saved_count, "note": "Data merged with existing records"})

@teams_bp.route("/", methods=["GET"])
def get_teams():
    teams = Team.query.all()
    return jsonify([
        {
            "name": t.name,
            "country": t.country,
            "badge": t.badge
        } for t in teams
    ])
