from extensions import db

class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(50), unique=True, nullable=False)
    season = db.Column(db.String(20))

    date = db.Column(db.String(50))

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

class PlayerStatistics(db.Model):
    __tablename__ = "player_statistics"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), unique=True, nullable=False)
    
    # Basic stats from CSV
    appearances_overall = db.Column(db.Integer, default=0)
    minutes_played_overall = db.Column(db.Integer, default=0)
    goals_overall = db.Column(db.Integer, default=0)
    assists_overall = db.Column(db.Integer, default=0)
    shots_on_target = db.Column(db.Integer, default=0)
    shots_total = db.Column(db.Integer, default=0)
    tackles_overall = db.Column(db.Integer, default=0)
    interceptions_overall = db.Column(db.Integer, default=0)
    yellow_cards_overall = db.Column(db.Integer, default=0)
    red_cards_overall = db.Column(db.Integer, default=0)
    
    # Computed metrics (calculated dynamically)
    goals_per_90 = db.Column(db.Float, default=0.0)
    assists_per_90 = db.Column(db.Float, default=0.0)
    shots_per_goal = db.Column(db.Float, default=0.0)
    efficiency_rating = db.Column(db.Float, default=0.0)  # (goals + assists) / shots_on_target
    defensive_actions_per_90 = db.Column(db.Float, default=0.0)  # (tackles + interceptions) / 90
    pass_completion_rate = db.Column(db.Float, default=0.0)
    average_rating = db.Column(db.Float, default=0.0)
    
    # Position-specific
    position = db.Column(db.String(50))
    current_club = db.Column(db.String(100))
    age = db.Column(db.Integer)
    
    player = db.relationship("Player", backref="statistics", uselist=False)
    
    def calculate_metrics(self):
        """Recalculate all derived metrics"""
        if self.minutes_played_overall > 0:
            self.goals_per_90 = (self.goals_overall / self.minutes_played_overall) * 90
            self.assists_per_90 = (self.assists_overall / self.minutes_played_overall) * 90
            self.defensive_actions_per_90 = ((self.tackles_overall + self.interceptions_overall) / self.minutes_played_overall) * 90
        
        if self.shots_total > 0:
            self.shots_per_goal = self.shots_total / max(self.goals_overall, 1)
        
        if self.shots_on_target > 0:
            self.efficiency_rating = (self.goals_overall + self.assists_overall) / self.shots_on_target
        
        return self


class TeamStatistics(db.Model):
    __tablename__ = "team_statistics"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), unique=True, nullable=False)
    
    # Basic stats from CSV
    matches_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    goals_scored = db.Column(db.Integer, default=0)
    goals_conceded = db.Column(db.Integer, default=0)
    clean_sheets = db.Column(db.Integer, default=0)
    total_shots = db.Column(db.Integer, default=0)
    shots_on_target = db.Column(db.Integer, default=0)
    
    # Computed metrics
    goals_per_match = db.Column(db.Float, default=0.0)
    goals_against_per_match = db.Column(db.Float, default=0.0)
    average_possession = db.Column(db.Float, default=0.0)
    clean_sheet_percentage = db.Column(db.Float, default=0.0)
    win_percentage = db.Column(db.Float, default=0.0)
    goal_difference = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    
    # xG stats
    xg_for_avg = db.Column(db.Float, default=0.0)
    xg_against_avg = db.Column(db.Float, default=0.0)
    
    team = db.relationship("Team", backref="statistics", uselist=False)
    
    def calculate_metrics(self):
        """Recalculate all derived metrics"""
        if self.matches_played > 0:
            self.goals_per_match = self.goals_scored / self.matches_played
            self.goals_against_per_match = self.goals_conceded / self.matches_played
            self.clean_sheet_percentage = (self.clean_sheets / self.matches_played) * 100
            self.win_percentage = (self.wins / self.matches_played) * 100
        
        self.goal_difference = self.goals_scored - self.goals_conceded
        self.points = (self.wins * 3) + (self.draws * 1)
        
        return self


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
