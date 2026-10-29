
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import APIError as OpenAIAPIError

from app.services.football_client import FootballClient, FootballAPIError
from app.tools.match_analysis import analyze_matches
from app.agent.assistant import ask_agent


app = FastAPI(
    title="United Intelligence",
    description="AI agent for Manchester United match analysis",
    version="0.1.0",
)


@app.get(
    "/health",
    summary="Health check",
    description="Check whether the United Intelligence API is running.",
)
def health_check():
    return {
        "status": "healthy",
        "application": "United Intelligence",
    }


@app.get(
    "/analysis/recent",
    summary="Analyze recent Manchester United matches",
    description=(
        "Retrieve completed Premier League fixtures from the 2024 season "
        "and calculate wins, draws, losses, goals, goal difference, and points."
    ),
)
def recent_match_analysis(limit: int = 10):
    if not 1 <= limit <= 20:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 20",
        )

    try:
        client = FootballClient()
        matches = client.get_recent_fixtures(limit=limit)
        analysis = analyze_matches(matches)

        return {
            "team": "Manchester United",
            "season": 2024,
            "competition": "Premier League",
            "matches": matches,
            "analysis": analysis,
        }
    except FootballAPIError as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve football data.",
        ) from exc


class AskRequest(BaseModel):
    question: str


@app.post(
    "/agent/ask",
    summary="Ask the Manchester United AI agent",
    description=(
        "Ask a question in natural language. The AI agent can retrieve "
        "match statistics and formulate an answer based on the returned data."
    ),
)
def ask_question(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    try:
        answer = ask_agent(question)
        return {
            "question": question,
            "answer": answer,
        }
    except FootballAPIError as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve football data.",
        ) from exc
    except OpenAIAPIError as exc:
        raise HTTPException(
            status_code=502,
            detail="The AI service is temporarily unavailable.",
        ) from exc
