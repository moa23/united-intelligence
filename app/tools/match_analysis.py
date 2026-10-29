
def analyze_matches(matches: list[dict]) -> dict:
    """Calculate basic statistics from completed Manchester United matches."""

    wins = 0
    draws = 0
    losses = 0
    goals_for = 0
    goals_against = 0

    for match in matches:
        home_team = match["home_team"]
        away_team = match["away_team"]
        home_goals = match["home_goals"]
        away_goals = match["away_goals"]

        if home_goals is None or away_goals is None:
            continue

        is_home = home_team == "Manchester United"

        if is_home:
            united_goals = home_goals
            opponent_goals = away_goals
        elif away_team == "Manchester United":
            united_goals = away_goals
            opponent_goals = home_goals
        else:
            continue

        goals_for += united_goals
        goals_against += opponent_goals

        if united_goals > opponent_goals:
            wins += 1
        elif united_goals == opponent_goals:
            draws += 1
        else:
            losses += 1

    played = wins + draws + losses

    return {
        "matches_played": played,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "goal_difference": goals_for - goals_against,
        "points": wins * 3 + draws,
    }
