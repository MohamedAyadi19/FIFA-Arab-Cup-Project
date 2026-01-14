from auth_utils import token_required
from flask import Blueprint, jsonify
from services.sportsdb_service import fetch_matches, save_matches_to_db
from models import Match

matches_bp = Blueprint("matches", __name__, url_prefix="/api/matches")

@matches_bp.route("/sync", methods=["POST"])
@token_required
def sync_matches():
    matches = fetch_matches()
    saved_count = save_matches_to_db(matches, season="2021")
    return jsonify({"status": "matches synced", "count": saved_count, "note": "Data merged with existing records"})


@matches_bp.route("/", methods=["GET"])
def get_matches():
    matches = Match.query.all()
    return jsonify([
        {
            "season": m.season,
            "date": m.date,
            "home_team": m.home_team,
            "away_team": m.away_team,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "venue": m.venue
        } for m in matches
    ])
