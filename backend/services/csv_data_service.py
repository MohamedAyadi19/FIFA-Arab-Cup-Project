"""
CSV-based Data Service - Loads and processes all data exclusively from CSV files.
No external API calls. All data comes from:
- teams.csv
- players.csv
- matches.csv
- league.csv
"""

import pandas as pd
import os
import math
from pathlib import Path

# CSV file paths
DATA_DIR = Path(__file__).parent.parent / "data"
TEAMS_CSV = DATA_DIR / "teams.csv"
PLAYERS_CSV = DATA_DIR / "players.csv"
MATCHES_CSV = DATA_DIR / "matches.csv"
LEAGUE_CSV = DATA_DIR / "league.csv"


class CSVDataService:
    """Service to load and process data exclusively from CSV files"""
    
    _teams_df = None
    _players_df = None
    _matches_df = None
    _league_df = None
    
    @staticmethod
    def _clean_nan(data):
        """Replace NaN values with None in dict or list of dicts"""
        import math
        if isinstance(data, dict):
            return {k: (None if isinstance(v, float) and (math.isnan(v) or math.isinf(v)) else v) 
                    for k, v in data.items()}
        elif isinstance(data, list):
            return [CSVDataService._clean_nan(item) for item in data]
        return data
    
    @classmethod
    def load_teams(cls):
        """Load teams CSV"""
        if cls._teams_df is None:
            cls._teams_df = pd.read_csv(TEAMS_CSV)
            # Replace NaN with None for JSON serialization
            cls._teams_df = cls._teams_df.where(pd.notnull(cls._teams_df), None)
        return cls._teams_df
    
    @classmethod
    def load_players(cls):
        """Load players CSV"""
        if cls._players_df is None:
            cls._players_df = pd.read_csv(PLAYERS_CSV)
            # Replace NaN with None for JSON serialization
            cls._players_df = cls._players_df.where(pd.notnull(cls._players_df), None)
        return cls._players_df
    
    @classmethod
    def load_matches(cls):
        """Load matches CSV"""
        if cls._matches_df is None:
            cls._matches_df = pd.read_csv(MATCHES_CSV)
            # Replace NaN with None for JSON serialization
            cls._matches_df = cls._matches_df.where(pd.notnull(cls._matches_df), None)
        return cls._matches_df
    
    @classmethod
    def load_league(cls):
        """Load league CSV"""
        if cls._league_df is None:
            cls._league_df = pd.read_csv(LEAGUE_CSV)
            # Replace NaN with None for JSON serialization
            cls._league_df = cls._league_df.where(pd.notnull(cls._league_df), None)
        return cls._league_df
    
    @classmethod
    def get_all_teams(cls):
        """Get all teams with aggregated stats"""
        teams = cls.load_teams()
        return cls._clean_nan(teams.to_dict('records'))
    
    @classmethod
    def get_team_by_name(cls, country):
        """Get team by country name"""
        teams = cls.load_teams()
        team = teams[teams['country'].str.lower() == country.lower()]
        if len(team) > 0:
            return cls._clean_nan(team.iloc[0].to_dict())
        return None
    
    @classmethod
    def get_all_players(cls):
        """Get all players with position-aware stats"""
        players = cls.load_players()
        return cls._clean_nan(players.to_dict('records'))
    
    @classmethod
    def get_players_by_team(cls, team_country):
        """Get players for a specific team, with position-aware stat selection"""
        players = cls.load_players()
        team_players = players[players['Current Club'].str.lower() == team_country.lower()]
        
        result = []
        for _, player in team_players.iterrows():
            result.append(cls._enrich_player_stats(player))
        return result
    
    @classmethod
    def get_all_matches(cls):
        """Get all matches with context"""
        matches = cls.load_matches()
        league = cls.load_league()
        
        result = []
        for _, match in matches.iterrows():
            match_dict = match.to_dict()
            # Add league context
            if len(league) > 0:
                league_stats = league.iloc[0]
                match_dict['league_avg_goals'] = league_stats.get('average_goals_per_match', 0)
                match_dict['league_btts_percentage'] = league_stats.get('btts_percentage', 0)
                match_dict['league_clean_sheets_percentage'] = league_stats.get('clean_sheets_percentage', 0)
            result.append(match_dict)
        return cls._clean_nan(result)
    
    @classmethod
    def get_league_stats(cls):
        """Get league-level aggregated stats"""
        league = cls.load_league()
        if len(league) > 0:
            return league.iloc[0].to_dict()
        return {}
    
    @classmethod
    def _enrich_player_stats(cls, player_row):
        """
        Position-aware stat enrichment and filtering.
        Selects and includes relevant stats based on player position.
        """
        player_dict = player_row.to_dict()
        position = str(player_dict.get('position', 'Unknown')).lower()
        
        # Base stats for all positions
        base_stats = {
            'full_name': player_dict.get('full_name'),
            'age': player_dict.get('age'),
            'position': player_dict.get('position'),
            'nationality': player_dict.get('nationality'),
            'Current Club': player_dict.get('Current Club'),
            'appearances_overall': player_dict.get('appearances_overall', 0),
            'minutes_played_overall': player_dict.get('minutes_played_overall', 0),
            'goals_overall': player_dict.get('goals_overall', 0),
            'assists_overall': player_dict.get('assists_overall', 0),
            'yellow_cards_overall': player_dict.get('yellow_cards_overall', 0),
            'red_cards_overall': player_dict.get('red_cards_overall', 0),
            'average_rating_overall': player_dict.get('average_rating_overall', 0),
        }
        
        # Position-specific stats
        position_stats = {}
        
        if 'goalkeeper' in position or 'gk' in position:
            # Goalkeeper-specific stats
            position_stats = {
                'clean_sheets_overall': player_dict.get('clean_sheets_overall', 0),
                'saves_per_game_overall': player_dict.get('saves_per_game_overall', 0),
                'conceded_per_90_overall': player_dict.get('conceded_per_90_overall', 0),
                'save_percentage_overall': player_dict.get('save_percentage_overall', 0),
                'inside_box_saves_total_overall': player_dict.get('inside_box_saves_total_overall', 0),
                'punches_total_overall': player_dict.get('punches_total_overall', 0),
                'shots_faced_per_game_overall': player_dict.get('shots_faced_per_game_overall', 0),
                'penalties_saved': player_dict.get('pens_saved_total_overall', 0),
            }
        
        elif 'defender' in position or 'back' in position or 'cb' in position:
            # Defender-specific stats
            position_stats = {
                'clean_sheets_overall': player_dict.get('clean_sheets_overall', 0),
                'tackles_per_90_overall': player_dict.get('tackles_per_90_overall', 0),
                'interceptions_per_game_overall': player_dict.get('interceptions_per_game_overall', 0),
                'aerial_duels_won_per_game_overall': player_dict.get('aerial_duels_won_per_game_overall', 0),
                'blocks_per_game_overall': player_dict.get('blocks_per_game_overall', 0),
                'clearances_per_game_overall': player_dict.get('clearances_per_game_overall', 0),
                'dispossesed_per_game_overall': player_dict.get('dispossesed_per_game_overall', 0),
            }
        
        elif 'midfielder' in position or 'mid' in position:
            # Midfielder-specific stats
            position_stats = {
                'passes_per_90_overall': player_dict.get('passes_per_90_overall', 0),
                'key_passes_per_game_overall': player_dict.get('key_passes_per_game_overall', 0),
                'chances_created_per_game_overall': player_dict.get('chances_created_per_game_overall', 0),
                'tackles_per_90_overall': player_dict.get('tackles_per_90_overall', 0),
                'passes_completed_per_game_overall': player_dict.get('passes_completed_per_game_overall', 0),
                'pass_completion_rate_overall': player_dict.get('pass_completion_rate_overall', 0),
                'interceptions_per_game_overall': player_dict.get('interceptions_per_game_overall', 0),
            }
        
        elif 'forward' in position or 'striker' in position or 'st' in position or 'winger' in position or 'wing' in position:
            # Forward/Winger-specific stats
            position_stats = {
                'shots_on_target_per_game_overall': player_dict.get('shots_on_target_per_game_overall', 0),
                'shots_total_overall': player_dict.get('shots_total_overall', 0),
                'dribbles_successful_per_game_overall': player_dict.get('dribbles_successful_per_game_overall', 0),
                'dribbles_per_game_overall': player_dict.get('dribbles_per_game_overall', 0),
                'xg_per_game_overall': player_dict.get('xg_per_game_overall', 0),
                'goals_per_90_overall': player_dict.get('goals_per_90_overall', 0),
                'assists_per_90_overall': player_dict.get('assists_per_90_overall', 0),
            }
        
        # Merge stats
        enriched_stats = {**base_stats, **position_stats}
        
        # Add derived metrics
        enriched_stats['player_type'] = cls._get_player_type(position)
        enriched_stats['goals_involved_overall'] = enriched_stats['goals_overall'] + enriched_stats['assists_overall']
        
        return enriched_stats
    
    @classmethod
    def _get_player_type(cls, position_str):
        """Categorize player type from position string"""
        pos = position_str.lower() if position_str else ''
        
        if 'goalkeeper' in pos or 'gk' in pos:
            return 'Goalkeeper'
        elif 'defender' in pos or 'back' in pos or 'cb' in pos or 'lb' in pos or 'rb' in pos:
            return 'Defender'
        elif 'midfielder' in pos or 'mid' in pos or 'cm' in pos:
            return 'Midfielder'
        elif 'forward' in pos or 'striker' in pos or 'st' in pos or 'winger' in pos or 'wing' in pos:
            return 'Forward'
        else:
            return 'Unknown'
    
    @classmethod
    def get_leaderboard_data(cls, stat_name, limit=10, player_type=None):
        """
        Get leaderboard data sorted by specific stat.
        Filters by player type if specified.
        """
        players = cls.load_players()
        
        # Filter by position if specified
        if player_type:
            if player_type.lower() == 'goalkeeper' or player_type.lower() == 'gk':
                players = players[players['position'].str.contains('goalkeeper|gk', case=False, na=False)]
            elif player_type.lower() == 'defender':
                players = players[players['position'].str.contains('defender|back|cb|lb|rb', case=False, na=False)]
            elif player_type.lower() == 'midfielder':
                players = players[players['position'].str.contains('midfielder|mid|cm', case=False, na=False)]
            elif player_type.lower() == 'forward':
                players = players[players['position'].str.contains('forward|striker|st|winger|wing', case=False, na=False)]
        
        # Sort by stat and get top N
        if stat_name in players.columns:
            top_players = players.nlargest(limit, stat_name)
            result = []
            for idx, (_, player) in enumerate(top_players.iterrows(), 1):
                player_data = {
                    'rank': idx,
                    'full_name': str(player.get('full_name', '')).strip() or 'Unknown',
                    'position': player.get('position', 'Unknown'),
                    'nationality': player.get('nationality', 'Unknown'),
                    'Current Club': player.get('Current Club', 'Unknown'),
                    stat_name: float(player.get(stat_name, 0)) if not math.isnan(float(player.get(stat_name, 0))) else 0,
                }
                result.append(player_data)
            return result
        return []
    
    @classmethod
    def get_team_aggregated_stats(cls, team_country):
        """
        Get team-level aggregated stats from teams CSV with player context.
        Combines team CSV data with player-level aggregation.
        """
        def safe_float(val):
            """Convert value to float, handling NaN"""
            try:
                f = float(val)
                return f if not math.isnan(f) else 0
            except:
                return 0
        
        teams = cls.load_teams()
        players = cls.load_players()
        matches = cls.load_matches()
        league = cls.load_league()
        
        # Get team from CSV
        team_row = teams[teams['country'].str.lower() == team_country.lower()]
        if len(team_row) == 0:
            return None
        
        team_data = team_row.iloc[0]
        team_stats = {}
        
        # Convert all values, handling NaN
        for col in team_data.index:
            val = team_data[col]
            try:
                if isinstance(val, str):
                    team_stats[col] = val
                elif hasattr(val, '__float__'):
                    f = float(val)
                    team_stats[col] = f if not math.isnan(f) else 0
                else:
                    team_stats[col] = val
            except:
                team_stats[col] = 0
        
        # Aggregate player-level stats for this team
        team_players = players[players['Current Club'].str.lower() == team_country.lower()]
        
        if len(team_players) > 0:
            # Aggregate stats across all players in team
            team_stats['total_players'] = len(team_players)
            team_stats['total_goals'] = safe_float(team_players['goals_overall'].sum())
            team_stats['total_assists'] = safe_float(team_players['assists_overall'].sum())
            team_stats['total_appearances'] = safe_float(team_players['appearances_overall'].sum())
            team_stats['total_minutes'] = safe_float(team_players['minutes_played_overall'].sum())
            team_stats['avg_player_rating'] = safe_float(team_players['average_rating_overall'].mean())
            team_stats['total_yellow_cards'] = safe_float(team_players['yellow_cards_overall'].sum())
            team_stats['total_red_cards'] = safe_float(team_players['red_cards_overall'].sum())
        
        # Add league context
        if len(league) > 0:
            league_data = league.iloc[0]
            team_stats['league_avg_goals'] = safe_float(league_data.get('average_goals_per_match', 0))
            team_stats['league_clean_sheets_percentage'] = safe_float(league_data.get('clean_sheets_percentage', 0))
            team_stats['league_avg_corners'] = safe_float(league_data.get('average_corners_per_match', 0))
        
        return team_stats


# Exported convenience functions
def get_all_teams():
    """Get all teams"""
    return CSVDataService.get_all_teams()

def get_team_by_name(country):
    """Get specific team"""
    return CSVDataService.get_team_by_name(country)

def get_all_players():
    """Get all players with position-aware stats"""
    return CSVDataService.get_all_players()

def get_players_by_team(team_country):
    """Get players for a team with position-aware filtering"""
    return CSVDataService.get_players_by_team(team_country)

def get_all_matches():
    """Get all matches with context"""
    return CSVDataService.get_all_matches()

def get_league_stats():
    """Get league statistics"""
    return CSVDataService.get_league_stats()

def get_leaderboard(stat_name, limit=10, player_type=None):
    """Get leaderboard for a stat"""
    return CSVDataService.get_leaderboard_data(stat_name, limit, player_type)

def get_team_stats(team_country):
    """Get team aggregated stats"""
    return CSVDataService.get_team_aggregated_stats(team_country)
