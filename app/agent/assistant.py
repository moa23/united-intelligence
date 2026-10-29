
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.agent.tools import get_recent_match_analysis

load_dotenv()


def get_openai_client() -> OpenAI:
    """Create the OpenAI client when the agent is called."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing from the environment."
        )

    return OpenAI(api_key=api_key)


TOOLS = [
    {
        "type": "function",
        "name": "get_recent_match_analysis",
        "description": (
            "Get real Manchester United Premier League results "
            "and statistics from the 2024 season. Use this tool "
            "when the user asks about recent results, performance, "
            "wins, losses, goals, or points."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": (
                        "Number of completed matches to analyze, "
                        "from 1 to 20."
                    ),
                }
            },
            "required": ["limit"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

INSTRUCTIONS = """
You are United Intelligence, a Manchester United match analysis assistant.

Use the match analysis tool when a question requires match statistics.
Base factual claims on the tool results.
Do not invent statistics or claim that results explain tactical causes
unless the available data supports that conclusion.
Clearly distinguish observed statistics from possible explanations.
The available match data is from the 2024 Premier League season.
Answer in the same language as the user.
"""

MAX_TOOL_ROUNDS = 5


def ask_agent(question: str) -> str:
    client = get_openai_client()

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=INSTRUCTIONS,
        input=question,
        tools=TOOLS,
    )

    for _ in range(MAX_TOOL_ROUNDS):
        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            return response.output_text

        tool_outputs = []

        for item in function_calls:
            if item.name != "get_recent_match_analysis":
                raise ValueError(f"Unknown tool: {item.name}")

            arguments = json.loads(item.arguments)
            limit = arguments.get("limit")

            if (
                not isinstance(limit, int)
                or isinstance(limit, bool)
                or not 1 <= limit <= 20
            ):
                raise ValueError(
                    "The requested match limit must be between 1 and 20."
                )

            result = get_recent_match_analysis(limit=limit)

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result),
                }
            )

        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS,
        )

    raise RuntimeError(
        f"Agent exceeded the maximum of {MAX_TOOL_ROUNDS} tool rounds."
    )
