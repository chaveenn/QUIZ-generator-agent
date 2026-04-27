import json
from pathlib import Path
from app.schemas.quiz_schema import Quiz


def export_quiz_to_json(quiz: Quiz, output_path: str) -> str:
    """
    Export a validated quiz object to a JSON file.

    Args:
        quiz: A validated Quiz object.
        output_path: Path where the JSON file should be saved.

    Returns:
        The absolute path to the saved JSON file.

    Raises:
        OSError: If the file cannot be written.
        ValueError: If the output path is invalid.
    """
    if not output_path.strip():
        raise ValueError("Output path cannot be empty.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(quiz.model_dump(), file, indent=2, ensure_ascii=False)

    return str(path.resolve())