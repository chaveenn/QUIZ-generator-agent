from typing import Set
from app.schemas.quiz_schema import Quiz


def validate_quiz_content(quiz: Quiz) -> None:
    """
    Perform additional semantic validations beyond schema validation.
    Raises ValueError if validation fails.
    """
    seen_questions: Set[str] = set()

    for question in quiz.questions:
        question_text = question.question.strip().lower()

        if question_text in seen_questions:
            raise ValueError("Duplicate question detected.")
        seen_questions.add(question_text)

        if question.correct_answer not in question.options:
            raise ValueError(
                f"Correct answer must be one of the provided options for question ID {question.id}."
            )

        if question.difficulty not in {"easy", "medium"}:
            raise ValueError(
                f"Invalid difficulty value for question ID {question.id}."
            )