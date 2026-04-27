import json
from pathlib import Path

from app.agents.question_generator import QuestionGeneratorAgent


def load_sample_input(file_path: str) -> dict:
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    state = load_sample_input("data/sample_summary.json")

    agent = QuestionGeneratorAgent(model_name="llama3.1:8b")
    result = agent.run(state)

    print("\n=== Updated State ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))