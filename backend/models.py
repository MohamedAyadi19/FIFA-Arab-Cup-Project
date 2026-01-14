from extensions import db

class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(50), unique=True, nullable=False)
    season = db.Column(db.String(20))

    date = db.Column(db.String(20))

    home_team = db.Column(db.String(100))
    away_team = db.Column(db.String(100))

    home_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    away_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))

    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    venue = db.Column(db.String(100))

class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String(50), unique=True, nullable=False)

    name = db.Column(db.String(100))
    country = db.Column(db.String(100))
    badge = db.Column(db.String(255))

class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(50), unique=True, nullable=False)

    name = db.Column(db.String(100))
    position = db.Column(db.String(50))
    nationality = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(20))
    height = db.Column(db.String(50))

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
