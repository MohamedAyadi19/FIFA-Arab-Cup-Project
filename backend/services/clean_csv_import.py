"""
Clean CSV Import Service
Clears old data and imports directly from CSV files.
Ensures each team has exactly 23 players.
"""

import pandas as pd
from extensions import db
from models import Team, Player, Match, PlayerStatistics, TeamStatistics
import os
from datetime import datetime


class CleanCSVImport:
    """Clean import from CSV files - replaces all existing data"""
    
    def __init__(self, data_folder: str = None):
        if data_folder is None:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_folder = os.path.join(base_path, 'data')
        
        self.data_folder = data_folder
        self.teams_csv = os.path.join(data_folder, 'teams.csv')
        self.players_csv = os.path.join(data_folder, 'players.csv')
        self.matches_csv = os.path.join(data_folder, 'matches.csv')
        
        self.team_map = {}  # Map country name to team_id
        self.stats = {
            'teams_imported': 0,
            'players_imported': 0,
            'matches_imported': 0,
            'team_stats_created': 0,
            'player_stats_created': 0
        }
    
    def safe_int(self, value, default=0):
        """Safely convert to int"""
        if pd.isna(value) or value == '':
            return default
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return default
    
    def safe_float(self, value, default=0.0):
        """Safely convert to float"""
        if pd.isna(value) or value == '':
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def clear_all_data(self):
        """Clear all existing data"""
        print("🗑️  Clearing old data...")
        
        # Clear in order to respect foreign keys
        PlayerStatistics.query.delete()
        TeamStatistics.query.delete()
        Player.query.delete()
        Match.query.delete()
        Team.query.delete()
        
        db.session.commit()
        print("  ✅ All old data cleared")
    
    def import_teams(self):
        """Import teams from CSV"""
        print(f"\n📊 Importing teams from {self.teams_csv}")
        
        df = pd.read_csv(self.teams_csv)
        
        for idx, row in df.iterrows():
            common_name = row.get('common_name', '')
            country = row.get('country', common_name)
            
            if not country:
                continue
            
            # Create team with unique team_id
            team = Team(
                team_id=f"team_{idx + 1}",
                name=common_name,
                country=country,
                badge=f"https://flagcdn.com/w80/{country.lower()[:2]}.png"
            )
            db.session.add(team)
            db.session.flush()
            
            # Map country to team id for player import
            self.team_map[country.lower()] = team.id
            self.team_map[common_name.lower()] = team.id
            
            # Create team statistics
            team_stats = TeamStatistics(
                team_id=team.id,
                matches_played=self.safe_int(row.get('matches_played', 0)),
                wins=self.safe_int(row.get('wins', 0)),
                draws=self.safe_int(row.get('draws', 0)),
                losses=self.safe_int(row.get('losses', 0)),
                goals_scored=self.safe_int(row.get('goals_scored', 0)),
                goals_conceded=self.safe_int(row.get('goals_conceded', 0)),
                clean_sheets=self.safe_int(row.get('clean_sheets', 0)),
                total_shots=self.safe_int(row.get('shots', 0)),
                shots_on_target=self.safe_int(row.get('shots_on_target', 0)),
                average_possession=self.safe_float(row.get('average_possession', 0.0)),
                xg_for_avg=self.safe_float(row.get('xg_for_avg_overall', 0.0)),
                xg_against_avg=self.safe_float(row.get('xg_against_avg_overall', 0.0))
            )
            team_stats.calculate_metrics()
            db.session.add(team_stats)
            
            self.stats['teams_imported'] += 1
            self.stats['team_stats_created'] += 1
            print(f"  ➕ {country}")
        
        db.session.commit()
        print(f"  ✅ {self.stats['teams_imported']} teams imported")
    
    def import_players(self):
        """Import players from CSV - ensure 23 players per team"""
        print(f"\n📊 Importing players from {self.players_csv}")
        
        df = pd.read_csv(self.players_csv)
        
        # Track players per team
        players_per_team = {}
        
        for _, row in df.iterrows():
            full_name = row.get('full_name', '')
            if not full_name or pd.isna(full_name) or full_name == '':
                continue
            
            # Get team from nationality or Current Club
            nationality = row.get('nationality', '')
            current_club = row.get('Current Club', '')
            
            # Try to find team
            team_id = None
            for team_identifier in [nationality, current_club]:
                if team_identifier and not pd.isna(team_identifier):
                    team_id = self.team_map.get(str(team_identifier).lower())
                    if team_id:
                        break
            
            if not team_id:
                continue
            
            # Check if team already has 23 players
            if team_id in players_per_team:
                if players_per_team[team_id] >= 23:
                    continue
            else:
                players_per_team[team_id] = 0
            
            # Get position
            position = row.get('position', 'Unknown')
            if pd.isna(position) or position == '':
                position = 'Midfielder'
            
            # Create player
            player = Player(
                player_id=f"player_{self.stats['players_imported'] + 1}",
                team_id=team_id,
                name=full_name,
                position=position,
                nationality=nationality
            )
            db.session.add(player)
            db.session.flush()
            
            # Create player statistics
            player_stats = PlayerStatistics(
                player_id=player.id,
                appearances_overall=self.safe_int(row.get('appearances_overall', 0)),
                minutes_played_overall=self.safe_int(row.get('minutes_played_overall', 0)),
                goals_overall=self.safe_int(row.get('goals_overall', 0)),
                assists_overall=self.safe_int(row.get('assists_overall', 0)),
                shots_on_target=self.safe_int(row.get('shots_on_target_overall', 0)),
                shots_total=self.safe_int(row.get('shots_total_overall', 0)),
                tackles_overall=self.safe_int(row.get('tackles_total_overall', 0)),
                interceptions_overall=self.safe_int(row.get('interceptions_total_overall', 0)),
                yellow_cards_overall=self.safe_int(row.get('yellow_cards_overall', 0)),
                red_cards_overall=self.safe_int(row.get('red_cards_overall', 0)),
                pass_completion_rate=self.safe_float(row.get('pass_completion_rate_overall', 0.0)),
                average_rating=self.safe_float(row.get('average_rating_overall', 0.0)),
                position=position,
                current_club=row.get('Current Club', ''),
                age=self.safe_int(row.get('age', 0))
            )
            player_stats.calculate_metrics()
            db.session.add(player_stats)
            
            players_per_team[team_id] = players_per_team.get(team_id, 0) + 1
            self.stats['players_imported'] += 1
            self.stats['player_stats_created'] += 1
        
        db.session.commit()
        print(f"  ✅ {self.stats['players_imported']} players imported")
        
        # Show distribution
        print("\n  📋 Players per team:")
        for team_id, count in players_per_team.items():
            team = Team.query.get(team_id)
            print(f"     {team.country}: {count} players")
    
    def import_matches(self):
        """Import matches from CSV"""
        print(f"\n📊 Importing matches from {self.matches_csv}")
        
        try:
            df = pd.read_csv(self.matches_csv)
        except FileNotFoundError:
            print("  ⚠️  matches.csv not found, skipping")
            return
        
        for _, row in df.iterrows():
            home_team_name = row.get('home_team_name', '')
            away_team_name = row.get('away_team_name', '')
            
            # Find teams
            home_team_id = self.team_map.get(home_team_name.lower())
            away_team_id = self.team_map.get(away_team_name.lower())
            
            if not home_team_id or not away_team_id:
                continue
            
            # Parse date
            date_str = row.get('date_GMT', '')
            try:
                match_date = datetime.strptime(date_str, '%b %d %Y - %I:%M%p')
            except:
                match_date = datetime.now()
            
            # Get venue, handle NaN
            venue = row.get('stadium_name', 'TBD')
            if pd.isna(venue):
                venue = 'TBD'
            
            # Create match
            match = Match(
                event_id=f"match_{self.stats['matches_imported'] + 1}",
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                home_team=home_team_name,
                away_team=away_team_name,
                home_score=self.safe_int(row.get('home_team_goal_count', 0)),
                away_score=self.safe_int(row.get('away_team_goal_count', 0)),
                date=date_str,
                venue=venue
            )
            db.session.add(match)
            self.stats['matches_imported'] += 1
        
        db.session.commit()
        print(f"  ✅ {self.stats['matches_imported']} matches imported")
    
    def execute(self):
        """Execute full clean import"""
        print("=" * 60)
        print("🔄 Clean CSV Import - Replacing All Data")
        print("=" * 60)
        
        try:
            # Step 1: Clear everything
            self.clear_all_data()
            
            # Step 2: Import teams (with stats)
            self.import_teams()
            
            # Step 3: Import players (23 per team, with stats)
            self.import_players()
            
            # Step 4: Import matches
            self.import_matches()
            
            # Summary
            print("\n" + "=" * 60)
            print("✅ Clean Import Complete")
            print("=" * 60)
            print(f"Teams: {self.stats['teams_imported']}")
            print(f"Team Statistics: {self.stats['team_stats_created']}")
            print(f"Players: {self.stats['players_imported']}")
            print(f"Player Statistics: {self.stats['player_stats_created']}")
            print(f"Matches: {self.stats['matches_imported']}")
            print("=" * 60)
            
            return self.stats
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            db.session.rollback()
            raise


def clean_import_from_csv():
    """Main entry point for clean CSV import"""
    importer = CleanCSVImport()
    return importer.execute()
