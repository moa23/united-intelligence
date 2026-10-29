
from app.services.football_client import FootballClient
from app.tools.match_analysis import analyze_matches


def get_recent_match_analysis(limit: int = 10) -> dict:
    """Get recent completed Premier League match statistics for Manchester United."""

    client = FootballClient()
    matches = client.get_recent_fixtures(limit=limit)

    return {
        "team": "Manchester United",
        "season": 2024,
        "competition": "Premier League",
        "matches": matches,
        "analysis": analyze_matches(matches),
    }
