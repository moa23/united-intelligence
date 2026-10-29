# United Intelligence ⚽

An AI-powered football analysis agent for Manchester United that combines real match data with large language models to answer questions about team performance.

## Overview

United Intelligence retrieves Premier League match results, calculates performance statistics, and uses an AI agent to explain the results in natural language.

The project demonstrates how to build an AI application that combines external APIs, backend development, tool calling, automated testing, and cloud deployment.

## Features

- **Real match data:** Retrieves Premier League fixtures and results from API-Football.
- **Performance analysis:** Calculates wins, draws, losses, goals scored, goals conceded, goal difference, and points.
- **AI agent:** Uses OpenAI to answer questions and explain statistics in natural language.
- **Tool calling:** Allows the agent to request structured match analysis instead of inventing statistics.
- **REST API:** Exposes endpoints through FastAPI.
- **Automated testing:** Uses pytest and GitHub Actions.
- **Cloud deployment:** Deployed to Google Cloud Run.
- **Secret management:** Uses Google Secret Manager for API credentials.

## Tech Stack

- Python 3.11
- FastAPI
- OpenAI API
- API-Football
- HTTPX
- Pytest
- GitHub Actions
- Docker
- Google Cloud Run
- Google Secret Manager

## Architecture

1. The client sends a request to the FastAPI backend.
2. The backend retrieves match data from API-Football.
3. The analysis service calculates team performance statistics.
4. The AI agent can call the analysis tool when answering a question.
5. OpenAI generates a natural-language response based on the retrieved statistics.
6. The API returns the result to the client.

## API Endpoints

| Method | Endpoint                    | Description                                        |
| ------ | --------------------------- | -------------------------------------------------- |
| GET    | `/health`                   | Checks application health                          |
| GET    | `/analysis/recent?limit=10` | Retrieves recent matches and calculated statistics |
| POST   | `/agent/ask`                | Asks the AI agent a football-related question      |

### Example request

```http
POST /agent/ask
Content-Type: application/json
```

```json
{
  "question": "Analyze Manchester United's last 10 Premier League matches. How many points did the team earn?"
}
```

The agent uses the available match-analysis tool to retrieve the relevant statistics before answering.

## Local Development

### Requirements

- Python 3.11
- An API-Football API key
- An OpenAI API key

### Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/moa23/united-intelligence.git
cd united-intelligence
```

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root and add your own API credentials:

```env
API_FOOTBALL_KEY=your_api_football_key
OPENAI_API_KEY=your_openai_api_key
```

**Never commit `.env` or API credentials to Git.**

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

GitHub Actions also runs the tests automatically when changes are pushed to the repository.

## Deployment

The application is deployed to Google Cloud Run.

Production API URL:

https://united-intelligence-171508549368.europe-north1.run.app

Health check:

https://united-intelligence-171508549368.europe-north1.run.app/health

The application uses Google Secret Manager to provide API credentials securely at runtime.

## Example Analysis

For the 10 completed Manchester United Premier League matches retrieved from the 2024/25 season, the calculated results were:

- Matches played: 10
- Wins: 2
- Draws: 2
- Losses: 6
- Goals scored: 10
- Goals conceded: 14
- Goal difference: -4
- Points: 8

These figures describe that specific sample of matches, not the team's overall season performance.

## Future Improvements

- Add more football statistics and analysis tools.
- Introduce tactical analysis using additional match data.
- Add a simple web interface for asking questions.
- Expand test coverage and monitoring.

## License

No license has been specified yet.
