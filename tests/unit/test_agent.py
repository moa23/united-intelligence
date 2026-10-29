
from types import SimpleNamespace
from unittest.mock import Mock
import pytest
from app.agent import assistant


def test_agent_calls_tool_and_returns_final_answer(monkeypatch):
    first_response = SimpleNamespace(
        id="response_1",
        output=[
            SimpleNamespace(
                type="function_call",
                name="get_recent_match_analysis",
                arguments='{"limit": 10}',
                call_id="call_1",
            )
        ],
        output_text="",
    )

    final_response = SimpleNamespace(
        id="response_2",
        output=[
            SimpleNamespace(type="message")
        ],
        output_text="Manchester United scoret 10 mål.",
    )

    fake_openai = Mock()
    fake_openai.responses.create.side_effect = [
        first_response,
        final_response,
    ]

    monkeypatch.setattr(assistant, "client", fake_openai)

    fake_analysis = {
        "team": "Manchester United",
        "analysis": {"goals_for": 10},
    }

    fake_tool = Mock(return_value=fake_analysis)
    monkeypatch.setattr(
        assistant,
        "get_recent_match_analysis",
        fake_tool,
    )

    answer = assistant.ask_agent(
        "Hvor mange mål scoret Manchester United?"
    )

    assert answer == "Manchester United scoret 10 mål."
    fake_tool.assert_called_once_with(limit=10)
    assert fake_openai.responses.create.call_count == 2




def test_agent_rejects_invalid_tool_limit(monkeypatch):
    invalid_response = SimpleNamespace(
        id="response_invalid",
        output=[
            SimpleNamespace(
                type="function_call",
                name="get_recent_match_analysis",
                arguments='{"limit": 100}',
                call_id="call_invalid",
            )
        ],
        output_text="",
    )

    fake_openai = Mock()
    fake_openai.responses.create.return_value = invalid_response
    monkeypatch.setattr(assistant, "client", fake_openai)

    fake_tool = Mock()
    monkeypatch.setattr(
        assistant,
        "get_recent_match_analysis",
        fake_tool,
    )

    with pytest.raises(ValueError, match="between 1 and 20"):
        assistant.ask_agent("Analyser 100 kamper")

    fake_tool.assert_not_called()
