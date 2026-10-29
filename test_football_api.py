
from app.services.football_client import FootballClient


client = FootballClient()

try:
    fixtures = client.get_recent_fixtures()

    if not fixtures:
        print("No fixtures returned. Check season and API access.")
    else:
        for match in fixtures:
            print(
                f"{match['date'][:10]} | "
                f"{match['home_team']} "
                f"{match['home_goals']} - "
                f"{match['away_goals']} "
                f"{match['away_team']} | "
                f"Status: {match['status']}"
            )

except Exception as exc:
    print(f"Could not retrieve fixtures: {exc}")
