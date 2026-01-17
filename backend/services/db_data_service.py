"""
Database-backed Data Service.
Provides data from PostgreSQL via SQLAlchemy models.
"""

from sqlalchemy import func
from extensions import db
from models import Team, TeamStatistics, Player, PlayerStatistics, Match
from services.csv_data_service import CSVDataService


TEAM_NAME_MAP = {
    'uae': 'united arab emirates',
    'ksa': 'saudi arabia',
}


def normalize_team_name(name):
    if not isinstance(name, str):
        return ''
    trimmed = name.strip()
    lowered = trimmed.lower()
    mapped = TEAM_NAME_MAP.get(lowered) or TEAM_NAME_MAP.get(trimmed) or TEAM_NAME_MAP.get(trimmed.upper())
    return (mapped or lowered).strip()


def _player_aggregates_subquery():
    return db.session.query(
        Player.team_id.label('team_id'),
        func.count(Player.id).label('total_players'),
        func.coalesce(func.sum(PlayerStatistics.goals_overall), 0).label('total_goals'),
        func.coalesce(func.sum(PlayerStatistics.assists_overall), 0).label('total_assists'),
        func.coalesce(func.avg(PlayerStatistics.average_rating), 0).label('avg_player_rating'),
    ).outerjoin(PlayerStatistics, PlayerStatistics.player_id == Player.id).group_by(Player.team_id).subquery()


def get_all_teams():
    player_agg = _player_aggregates_subquery()

    rows = db.session.query(
        Team,
        TeamStatistics,
        player_agg.c.total_players,
        player_agg.c.total_goals,
        player_agg.c.total_assists,
        player_agg.c.avg_player_rating,
    ).outerjoin(
        TeamStatistics, TeamStatistics.team_id == Team.id
    ).outerjoin(
        player_agg, player_agg.c.team_id == Team.id
    ).all()

    teams = []
    for team, stats, total_players, total_goals, total_assists, avg_player_rating in rows:
        stats = stats or TeamStatistics(team_id=team.id)
        stats.calculate_metrics()
        teams.append({
            'team_name': team.name,
            'common_name': team.name,
            'country': team.country,
            'name': team.name,
            'badge': team.badge,
            'matches_played': stats.matches_played or 0,
            'wins': stats.wins or 0,
            'draws': stats.draws or 0,
            'losses': stats.losses or 0,
            'goals_scored': stats.goals_scored or 0,
            'goals_conceded': stats.goals_conceded or 0,
            'clean_sheets': stats.clean_sheets or 0,
            'shots': stats.total_shots or 0,
            'shots_on_target': stats.shots_on_target or 0,
            'average_possession': stats.average_possession or 0,
            'points': stats.points or 0,
            'goal_difference': stats.goal_difference or 0,
            'total_players': total_players or 0,
            'total_goals': total_goals or 0,
            'total_assists': total_assists or 0,
            'avg_player_rating': float(avg_player_rating or 0),
        })

    return teams


def get_team_stats(team_name):
    target = normalize_team_name(team_name)
    teams = Team.query.all()
    match = None
    for team in teams:
        if normalize_team_name(team.country) == target or normalize_team_name(team.name) == target:
            match = team
            break

    if not match:
        return None

    stats = TeamStatistics.query.filter_by(team_id=match.id).first()
    stats = stats or TeamStatistics(team_id=match.id)
    stats.calculate_metrics()

    player_agg = _player_aggregates_subquery()
    agg = db.session.query(
        player_agg.c.total_players,
        player_agg.c.total_goals,
        player_agg.c.total_assists,
        player_agg.c.avg_player_rating,
    ).filter(player_agg.c.team_id == match.id).first()

    team_stats = {
        'country': match.country,
        'name': match.name,
        'team_name': match.name,
        'matches_played': stats.matches_played or 0,
        'wins': stats.wins or 0,
        'draws': stats.draws or 0,
        'losses': stats.losses or 0,
        'goals_scored': stats.goals_scored or 0,
        'goals_conceded': stats.goals_conceded or 0,
        'clean_sheets': stats.clean_sheets or 0,
        'shots': stats.total_shots or 0,
        'shots_on_target': stats.shots_on_target or 0,
        'average_possession': stats.average_possession or 0,
        'points': stats.points or 0,
        'goal_difference': stats.goal_difference or 0,
        'total_players': agg[0] if agg else 0,
        'total_goals': agg[1] if agg else 0,
        'total_assists': agg[2] if agg else 0,
        'avg_player_rating': float(agg[3] or 0) if agg else 0,
    }

    league_stats = CSVDataService.get_league_stats()
    if league_stats:
        team_stats['league_avg_goals'] = league_stats.get('average_goals_per_match', 0)
        team_stats['league_clean_sheets_percentage'] = league_stats.get('clean_sheets_percentage', 0)
        team_stats['league_avg_corners'] = league_stats.get('average_corners_per_match', 0)

    return team_stats


def get_all_players():
    rows = db.session.query(Player, PlayerStatistics).outerjoin(
        PlayerStatistics, PlayerStatistics.player_id == Player.id
    ).all()

    players = []
    for player, stats in rows:
        stats = stats or PlayerStatistics(player_id=player.id)
        stats.calculate_metrics()
        players.append({
            'full_name': player.name,
            'name': player.name,
            'position': stats.position or player.position or 'Unknown',
            'player_type': stats.position or player.position or 'Unknown',
            'nationality': player.nationality,
            'Current Club': stats.current_club or player.nationality,
            'age': stats.age or 0,
            'appearances_overall': stats.appearances_overall or 0,
            'minutes_played_overall': stats.minutes_played_overall or 0,
            'goals_overall': stats.goals_overall or 0,
            'assists_overall': stats.assists_overall or 0,
            'yellow_cards_overall': stats.yellow_cards_overall or 0,
            'red_cards_overall': stats.red_cards_overall or 0,
            'average_rating_overall': stats.average_rating or 0,
            'goals_per_90_overall': round(stats.goals_per_90, 2) if stats.goals_per_90 else 0,
            'assists_per_90_overall': round(stats.assists_per_90, 2) if stats.assists_per_90 else 0,
            'pass_completion_rate_overall': stats.pass_completion_rate or 0,
            'shots_on_target_overall': stats.shots_on_target or 0,
            'shots_total_overall': stats.shots_total or 0,
            'tackles_total_overall': stats.tackles_overall or 0,
            'interceptions_total_overall': stats.interceptions_overall or 0,
            'tackles_per_90_overall': round(stats.defensive_actions_per_90, 2) if stats.defensive_actions_per_90 else 0,
            'interceptions_per_game_overall': stats.interceptions_overall or 0,
            'clean_sheets_overall': 0,
            'saves_per_game_overall': 0,
            'save_percentage_overall': 0,
            'conceded_per_90_overall': 0,
            'xg_per_game_overall': 0,
            'dribbles_per_game_overall': 0,
            'dribbles_successful_per_game_overall': 0,
            'key_passes_per_game_overall': 0,
            'passes_per_90_overall': 0,
            'blocks_per_game_overall': 0,
            'clearances_per_game_overall': 0,
        })

    return players


def get_players_by_team(team_country):
    target = normalize_team_name(team_country)
    rows = db.session.query(Player, PlayerStatistics).outerjoin(
        PlayerStatistics, PlayerStatistics.player_id == Player.id
    ).all()

    result = []
    for player, stats in rows:
        stats = stats or PlayerStatistics(player_id=player.id)
        current_team = stats.current_club or player.nationality or ''
        if normalize_team_name(current_team) != target:
            continue
        stats.calculate_metrics()
        result.append({
            'full_name': player.name,
            'name': player.name,
            'position': stats.position or player.position or 'Unknown',
            'player_type': stats.position or player.position or 'Unknown',
            'nationality': player.nationality,
            'Current Club': stats.current_club or player.nationality,
            'appearances_overall': stats.appearances_overall or 0,
            'minutes_played_overall': stats.minutes_played_overall or 0,
            'goals_overall': stats.goals_overall or 0,
            'assists_overall': stats.assists_overall or 0,
            'yellow_cards_overall': stats.yellow_cards_overall or 0,
            'red_cards_overall': stats.red_cards_overall or 0,
            'average_rating_overall': stats.average_rating or 0,
            'goals_per_90_overall': round(stats.goals_per_90, 2) if stats.goals_per_90 else 0,
            'assists_per_90_overall': round(stats.assists_per_90, 2) if stats.assists_per_90 else 0,
        })

    return result


def get_leaderboard(stat_name, limit=10, player_type=None):
    query = PlayerStatistics.query

    if player_type:
        query = query.filter(PlayerStatistics.position.ilike(f"%{player_type}%"))

    if stat_name == 'tackles_per_90_overall':
        tackles_per_90 = (PlayerStatistics.tackles_overall * 90.0) / func.nullif(PlayerStatistics.minutes_played_overall, 0)
        query = query.order_by(tackles_per_90.desc())
    elif hasattr(PlayerStatistics, stat_name):
        query = query.order_by(getattr(PlayerStatistics, stat_name).desc())
    else:
        query = query.order_by(PlayerStatistics.goals_overall.desc())

    players = query.limit(limit).all()

    leaderboard = []
    for idx, stats in enumerate(players, 1):
        player = Player.query.get(stats.player_id) if stats.player_id else None
        leaderboard.append({
            'rank': idx,
            'full_name': player.name if player else 'Unknown',
            'position': stats.position or (player.position if player else 'Unknown'),
            'nationality': player.nationality if player else 'Unknown',
            'Current Club': stats.current_club or (player.nationality if player else 'Unknown'),
            stat_name: getattr(stats, stat_name, None) if stat_name != 'tackles_per_90_overall' else (
                round((stats.tackles_overall * 90.0) / stats.minutes_played_overall, 2) if stats.minutes_played_overall else 0
            )
        })

    return leaderboard


def get_all_matches():
    matches = Match.query.all()
    return [
        {
            'event_id': m.event_id,
            'date': m.date,
            'home_team': m.home_team,
            'away_team': m.away_team,
            'home_score': m.home_score,
            'away_score': m.away_score,
            'venue': m.venue,
        }
        for m in matches
    ]


def get_league_stats():
    return CSVDataService.get_league_stats()
