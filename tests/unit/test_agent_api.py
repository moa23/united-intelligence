
from fastapi.testclient import TestClient

from app.main import app
import app.main as main
from openai import APIError
from unittest.mock import Mock
client = TestClient(app)


def test_agent_ask_returns_answer(monkeypatch):
    def fake_ask_agent(question: str) -> str:
        return "Manchester United scoret 10 mål."

    monkeypatch.setattr(main, "ask_agent", fake_ask_agent)
    response = client.post(
        "/agent/ask",
        json={
            "question": "Hvor mange mål scoret Manchester United?"
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Hvor mange mål scoret Manchester United?"
    assert data["answer"] == "Manchester United scoret 10 mål."


def test_agent_ask_rejects_empty_question():
    response = client.post(
        "/agent/ask",
        json={"question": "   "},
    )

    assert response.status_code == 400

def test_agent_ask_handles_openai_error(monkeypatch):
    error = APIError(
        message="Service unavailable",
        request=Mock(),
        body=None,
    )

    def fake_ask_agent(question: str) -> str:
        raise error

    monkeypatch.setattr(main, "ask_agent", fake_ask_agent)

    response = client.post(
        "/agent/ask",
        json={"question": "Hvor mange mål scoret United?"},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "The AI service is temporarily unavailable."
    )
