import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"
LEAGUE_ID = os.getenv("SPORTSDB_LEAGUE_ID", "5105")
SEASON = os.getenv("SPORTSDB_SEASON", "2021")

session = requests.Session()

retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
)

session.mount("https://", HTTPAdapter(max_retries=retries))

def fetch_matches():
    try:
        url = f"{BASE_URL}/eventsseason.php?id={LEAGUE_ID}&s={SEASON}"
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("events", []) or []
    except Exception as e:
        print("SportsDB API error:", e)
        return []

def fetch_raw_seasons():
    url = f"{BASE_URL}/search_all_seasons.php?id={LEAGUE_ID}"
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

from models import Match
from extensions import db

def save_matches_to_db(matches, season="2021"):
    saved_count = 0
    for m in matches:
        if not m.get("idEvent"):
            continue

        exists = Match.query.filter_by(event_id=m["idEvent"]).first()
        if exists:
            # Update existing match with new data
            exists.date = m.get("dateEvent", exists.date)
            exists.home_score = m.get("intHomeScore", exists.home_score)
            exists.away_score = m.get("intAwayScore", exists.away_score)
            exists.venue = m.get("strVenue", exists.venue)
            db.session.merge(exists)
        else:
            # Create new match
            home_team = Team.query.filter_by(name=m.get("strHomeTeam")).first()
            away_team = Team.query.filter_by(name=m.get("strAwayTeam")).first()

            match = Match(
                event_id=m["idEvent"],
                season=season,
                date=m.get("dateEvent"),
                home_team=m.get("strHomeTeam"),
                away_team=m.get("strAwayTeam"),
                home_team_id=home_team.id if home_team else None,
                away_team_id=away_team.id if away_team else None,
                home_score=m.get("intHomeScore"),
                away_score=m.get("intAwayScore"),
                venue=m.get("strVenue"),
            )
            db.session.add(match)
            saved_count += 1

    db.session.commit()
    return saved_count


def fetch_teams():
    url = f"{BASE_URL}/lookup_all_teams.php?id={LEAGUE_ID}"
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.json().get("teams", []) or []

from models import Team

def save_teams_to_db(teams):
    saved_count = 0
    for t in teams:
        if not t.get("idTeam"):
            continue

        exists = Team.query.filter_by(team_id=t["idTeam"]).first()
        if exists:
            # Update existing team with new data
            exists.name = t.get("strTeam", exists.name)
            exists.country = t.get("strCountry", exists.country)
            if t.get("strBadge"):  # Only update badge if provided
                exists.badge = t.get("strBadge")
            db.session.merge(exists)
        else:
            # Create new team
            team = Team(
                team_id=t["idTeam"],
                name=t.get("strTeam"),
                country=t.get("strCountry"),
                badge=t.get("strBadge"),
            )
            db.session.add(team)
        saved_count += 1

    db.session.commit()
    return saved_count

def fetch_players_by_team(team_api_id):
    try:
        url = f"{BASE_URL}/lookup_all_players.php?id={team_api_id}"
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("player") or []
    except Exception as e:
        print(f"Error fetching players for team {team_api_id}:", e)
        return []


from models import Player
from extensions import db

def save_players_to_db(players, team):
    saved_count = 0
    for p in players:
        if not p or not isinstance(p, dict) or not p.get("idPlayer"):
            continue

        exists = Player.query.filter_by(player_id=p["idPlayer"]).first()
        if exists:
            # Update existing player
            exists.name = p.get("strPlayer", exists.name)
            exists.position = p.get("strPosition", exists.position)
            exists.nationality = p.get("strNationality", exists.nationality)
            exists.date_of_birth = p.get("dateBorn", exists.date_of_birth)
            exists.height = p.get("strHeight", exists.height)
            db.session.merge(exists)
        else:
            # Create new player
            player = Player(
                player_id=p["idPlayer"],
                name=p.get("strPlayer"),
                position=p.get("strPosition"),
                nationality=p.get("strNationality"),
                date_of_birth=p.get("dateBorn"),
                height=p.get("strHeight"),
                team_id=team.id,
            )
            db.session.add(player)
            saved_count += 1

    db.session.commit()
    return saved_count
