
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://v3.football.api-sports.io"

class FootballAPIError(Exception):
    """Raised when the football API request fails."""

class FootballClient:
    def __init__(self) -> None:
        api_key = os.getenv("API_FOOTBALL_KEY")
        if not api_key:
            raise FootballAPIError(
                "API_FOOTBALL_KEY is missing from the environment."
            )

        self.headers = {"x-apisports-key": api_key}

    def _get(self, endpoint: str, params: dict) -> list[dict]:
        try:
            response = httpx.get(
                f"{BASE_URL}/{endpoint}",
                headers=self.headers,
                params=params,
                timeout=20.0,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise FootballAPIError(
                f"Football API request failed: {exc}"
            ) from exc

        data = response.json()

        if data.get("errors"):
            raise FootballAPIError(
                f"Football API returned errors: {data['errors']}"
            )

        return data.get("response", [])

    def search_team(
        self, name: str = "Manchester United"
    ) -> list[dict]:
        return self._get("teams", {"search": name})
    def get_recent_fixtures(
        self,
        team_id: int = 33,
        season: int = 2024,
        league_id: int = 39,
        limit: int = 10,
    ) -> list[dict]:
        if not 1 <= limit <= 20:
            raise ValueError("limit must be between 1 and 20")

        fixtures = self._get(
            "fixtures",
            {
                "team": team_id,
                "season": season,
                "league": league_id,
            },
        )

        results = []

        for item in fixtures:
            fixture = item["fixture"]
            teams = item["teams"]
            goals = item["goals"]

            # Include completed matches only.
            if fixture["status"]["short"] != "FT":
                continue

            results.append(
                {
                    "fixture_id": fixture["id"],
                    "date": fixture["date"],
                    "status": fixture["status"]["short"],
                    "home_team": teams["home"]["name"],
                    "away_team": teams["away"]["name"],
                    "home_goals": goals["home"],
                    "away_goals": goals["away"],
                }
            )

        results.sort(key=lambda match: match["date"], reverse=True)
        return results[:limit]
