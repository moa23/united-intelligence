
from app.agent.assistant import ask_agent


question = "Hvor mange av de siste 10 Premier League-kampene vant og tapte Manchester United?"

answer = ask_agent(question)

print("\n=== UNITED INTELLIGENCE ===")
print(f"Spørsmål: {question}\n")
print(f"AI-agentens svar:\n{answer}")
