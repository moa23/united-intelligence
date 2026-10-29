
from app.services.football_client import FootballClient
from app.tools.match_analysis import analyze_matches


def main():
    client = FootballClient()

    matches = client.get_recent_fixtures(limit=10)
    analysis = analyze_matches(matches)

    print("\n=== UNITED INTELLIGENCE ===")
    print("Manchester United – kampanalyse")
    print("============================")

    for key, value in analysis.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
