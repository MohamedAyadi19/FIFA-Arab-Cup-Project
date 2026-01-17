"""
Statistics calculator - Computes derived metrics from player and team data.
All metrics are calculated on-the-fly, not stored permanently.
"""

from models import PlayerStatistics, TeamStatistics, Player, Team


class PlayerStatsCalculator:
    """Calculate advanced player statistics"""
    
    @staticmethod
    def calculate_all_metrics(player_stats: PlayerStatistics) -> dict:
        """Calculate all metrics for a player"""
        player_stats.calculate_metrics()  # Update model metrics
        
        return {
            "basic": {
                "appearances": player_stats.appearances_overall,
                "minutes_played": player_stats.minutes_played_overall,
                "goals": player_stats.goals_overall,
                "assists": player_stats.assists_overall,
                "position": player_stats.position,
                "age": player_stats.age,
                "current_club": player_stats.current_club,
            },
            "computed": {
                "goals_per_90": round(player_stats.goals_per_90, 2),
                "assists_per_90": round(player_stats.assists_per_90, 2),
                "shots_per_goal": round(player_stats.shots_per_goal, 2),
                "efficiency_rating": round(player_stats.efficiency_rating, 2),
                "defensive_actions_per_90": round(player_stats.defensive_actions_per_90, 2),
                "pass_completion_rate": round(player_stats.pass_completion_rate, 1),
                "average_rating": round(player_stats.average_rating, 1),
            },
            "shooting": {
                "shots_total": player_stats.shots_total,
                "shots_on_target": player_stats.shots_on_target,
                "shot_accuracy": PlayerStatsCalculator.calculate_shot_accuracy(player_stats),
            },
            "defense": {
                "tackles": player_stats.tackles_overall,
                "interceptions": player_stats.interceptions_overall,
                "yellow_cards": player_stats.yellow_cards_overall,
                "red_cards": player_stats.red_cards_overall,
            },
        }
    
    @staticmethod
    def calculate_shot_accuracy(player_stats: PlayerStatistics) -> float:
        """Calculate shot accuracy percentage"""
        if player_stats.shots_total == 0:
            return 0.0
        return round((player_stats.shots_on_target / player_stats.shots_total) * 100, 1)
    
    @staticmethod
    def get_player_form_profile(player_stats: PlayerStatistics) -> str:
        """Determine player form/profile"""
        if player_stats.goals_per_90 > 1.0:
            return "Elite Scorer"
        elif player_stats.goals_per_90 > 0.5:
            return "Prolific Scorer"
        elif player_stats.assists_per_90 > 0.5:
            return "Playmaker"
        elif player_stats.defensive_actions_per_90 > 2.0:
            return "Defensive Rock"
        elif player_stats.minutes_played_overall < 100:
            return "Emerging Talent"
        else:
            return "Regular Player"


class TeamStatsCalculator:
    """Calculate advanced team statistics"""
    
    @staticmethod
    def calculate_all_metrics(team_stats: TeamStatistics) -> dict:
        """Calculate all metrics for a team"""
        team_stats.calculate_metrics()  # Update model metrics
        
        return {
            "record": {
                "matches_played": team_stats.matches_played,
                "wins": team_stats.wins,
                "draws": team_stats.draws,
                "losses": team_stats.losses,
                "points": team_stats.points,
            },
            "performance": {
                "win_percentage": round(team_stats.win_percentage, 1),
                "draw_percentage": TeamStatsCalculator.calculate_draw_percentage(team_stats),
                "loss_percentage": TeamStatsCalculator.calculate_loss_percentage(team_stats),
            },
            "goals": {
                "goals_scored": team_stats.goals_scored,
                "goals_conceded": team_stats.goals_conceded,
                "goal_difference": team_stats.goal_difference,
                "goals_per_match": round(team_stats.goals_per_match, 2),
                "goals_against_per_match": round(team_stats.goals_against_per_match, 2),
            },
            "defense": {
                "clean_sheets": team_stats.clean_sheets,
                "clean_sheet_percentage": round(team_stats.clean_sheet_percentage, 1),
            },
            "possession": {
                "average_possession": round(team_stats.average_possession, 1),
            },
            "shots": {
                "total_shots": team_stats.total_shots,
                "shots_on_target": team_stats.shots_on_target,
                "shot_accuracy": TeamStatsCalculator.calculate_shot_accuracy(team_stats),
            },
            "expected_goals": {
                "xg_for_avg": round(team_stats.xg_for_avg, 2),
                "xg_against_avg": round(team_stats.xg_against_avg, 2),
                "xg_difference": round(team_stats.xg_for_avg - team_stats.xg_against_avg, 2),
            },
            "attack_strength": TeamStatsCalculator.calculate_attack_strength(team_stats),
            "defensive_stability": TeamStatsCalculator.calculate_defensive_stability(team_stats),
        }
    
    @staticmethod
    def calculate_draw_percentage(team_stats: TeamStatistics) -> float:
        """Calculate draw percentage"""
        if team_stats.matches_played == 0:
            return 0.0
        return round((team_stats.draws / team_stats.matches_played) * 100, 1)
    
    @staticmethod
    def calculate_loss_percentage(team_stats: TeamStatistics) -> float:
        """Calculate loss percentage"""
        if team_stats.matches_played == 0:
            return 0.0
        return round((team_stats.losses / team_stats.matches_played) * 100, 1)
    
    @staticmethod
    def calculate_shot_accuracy(team_stats: TeamStatistics) -> float:
        """Calculate shot accuracy percentage"""
        if team_stats.total_shots == 0:
            return 0.0
        return round((team_stats.shots_on_target / team_stats.total_shots) * 100, 1)
    
    @staticmethod
    def calculate_attack_strength(team_stats: TeamStatistics) -> dict:
        """
        Calculate attack strength index
        Based on: goals per match + xG rating
        """
        attack_score = 0.0
        
        if team_stats.goals_per_match > 2.5:
            attack_score += 40
        elif team_stats.goals_per_match > 2.0:
            attack_score += 30
        elif team_stats.goals_per_match > 1.5:
            attack_score += 20
        else:
            attack_score += 10
        
        if team_stats.xg_for_avg > 1.8:
            attack_score += 40
        elif team_stats.xg_for_avg > 1.5:
            attack_score += 30
        elif team_stats.xg_for_avg > 1.2:
            attack_score += 20
        else:
            attack_score += 10
        
        attack_strength = min(attack_score / 2, 100)  # Normalize to 100
        
        return {
            "score": round(attack_strength, 1),
            "rating": TeamStatsCalculator._get_strength_rating(attack_strength),
        }
    
    @staticmethod
    def calculate_defensive_stability(team_stats: TeamStatistics) -> dict:
        """
        Calculate defensive stability index
        Based on: goals conceded + xG against + clean sheets
        """
        defense_score = 0.0
        
        if team_stats.goals_against_per_match < 1.0:
            defense_score += 40
        elif team_stats.goals_against_per_match < 1.5:
            defense_score += 30
        elif team_stats.goals_against_per_match < 2.0:
            defense_score += 20
        else:
            defense_score += 10
        
        if team_stats.xg_against_avg < 1.2:
            defense_score += 40
        elif team_stats.xg_against_avg < 1.5:
            defense_score += 30
        elif team_stats.xg_against_avg < 1.8:
            defense_score += 20
        else:
            defense_score += 10
        
        if team_stats.clean_sheet_percentage > 50:
            defense_score += 20
        elif team_stats.clean_sheet_percentage > 30:
            defense_score += 10
        
        defense_stability = min(defense_score / 2.5, 100)  # Normalize to 100
        
        return {
            "score": round(defense_stability, 1),
            "rating": TeamStatsCalculator._get_strength_rating(defense_stability),
        }
    
    @staticmethod
    def _get_strength_rating(score: float) -> str:
        """Convert numeric score to rating"""
        if score >= 80:
            return "Elite"
        elif score >= 65:
            return "Very Strong"
        elif score >= 50:
            return "Strong"
        elif score >= 35:
            return "Average"
        else:
            return "Weak"


class LeaderboardCalculator:
    """Calculate leaderboards"""
    
    @staticmethod
    def get_top_scorers(limit: int = 10) -> list:
        """Get top scorers by goals"""
        players = PlayerStatistics.query.order_by(
            PlayerStatistics.goals_overall.desc()
        ).limit(limit).all()
        
        return [
            {
                "rank": idx + 1,
                "player_id": p.player_id,
                "player_name": Player.query.get(p.player_id).name if p.player_id else "Unknown",
                "goals": p.goals_overall,
                "assists": p.assists_overall,
                "goals_per_90": round(p.goals_per_90, 2),
                "team": Player.query.get(p.player_id).team_id if p.player_id else None,
            }
            for idx, p in enumerate(players)
        ]
    
    @staticmethod
    def get_top_assisters(limit: int = 10) -> list:
        """Get top assisters"""
        players = PlayerStatistics.query.order_by(
            PlayerStatistics.assists_overall.desc()
        ).limit(limit).all()
        
        return [
            {
                "rank": idx + 1,
                "player_id": p.player_id,
                "player_name": Player.query.get(p.player_id).name if p.player_id else "Unknown",
                "assists": p.assists_overall,
                "goals": p.goals_overall,
                "assists_per_90": round(p.assists_per_90, 2),
                "team": Player.query.get(p.player_id).team_id if p.player_id else None,
            }
            for idx, p in enumerate(players)
        ]
    
    @staticmethod
    def get_top_defenders(limit: int = 10) -> list:
        """Get top defenders by defensive actions"""
        players = PlayerStatistics.query.filter(
            PlayerStatistics.position.in_(['Defender', 'Defensive Midfield'])
        ).order_by(
            (PlayerStatistics.tackles_overall + PlayerStatistics.interceptions_overall).desc()
        ).limit(limit).all()
        
        return [
            {
                "rank": idx + 1,
                "player_id": p.player_id,
                "player_name": Player.query.get(p.player_id).name if p.player_id else "Unknown",
                "tackles": p.tackles_overall,
                "interceptions": p.interceptions_overall,
                "defensive_actions_per_90": round(p.defensive_actions_per_90, 2),
                "team": Player.query.get(p.player_id).team_id if p.player_id else None,
            }
            for idx, p in enumerate(players)
        ]
    
    @staticmethod
    def get_team_standings(limit: int = 16) -> list:
        """Get team standings by points"""
        teams = TeamStatistics.query.order_by(
            TeamStatistics.points.desc(),
            TeamStatistics.goal_difference.desc()
        ).limit(limit).all()
        
        return [
            {
                "position": idx + 1,
                "team_id": t.team_id,
                "team_name": Team.query.get(t.team_id).name if t.team_id else "Unknown",
                "matches": t.matches_played,
                "wins": t.wins,
                "draws": t.draws,
                "losses": t.losses,
                "goals_for": t.goals_scored,
                "goals_against": t.goals_conceded,
                "goal_difference": t.goal_difference,
                "points": t.points,
            }
            for idx, t in enumerate(teams)
        ]
