
from app.tools.match_analysis import analyze_matches


def test_analyze_matches():
    matches = [
        {
            "home_team": "Manchester United",
            "away_team": "Arsenal",
            "home_goals": 2,
            "away_goals": 1,
        },
        {
            "home_team": "Liverpool",
            "away_team": "Manchester United",
            "home_goals": 1,
            "away_goals": 1,
        },
        {
            "home_team": "Manchester United",
            "away_team": "Chelsea",
            "home_goals": 0,
            "away_goals": 2,
        },
    ]

    result = analyze_matches(matches)

    assert result["matches_played"] == 3
    assert result["wins"] == 1
    assert result["draws"] == 1
    assert result["losses"] == 1
    assert result["goals_for"] == 3
    assert result["goals_against"] == 4
    assert result["goal_difference"] == -1
    assert result["points"] == 4
