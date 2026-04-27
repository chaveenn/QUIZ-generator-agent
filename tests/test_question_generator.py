import json
from pathlib import Path

import pytest

from app.schemas.quiz_schema import Quiz
from app.tools.quiz_exporter import export_quiz_to_json
from app.utils.validator import validate_quiz_content


@pytest.fixture
def valid_quiz_dict():
    return {
        "topic": "Linear Regression",
        "questions": [
            {
                "id": 1,
                "question": "What is the main purpose of linear regression?",
                "options": [
                    "To classify data into groups",
                    "To predict continuous values",
                    "To encrypt information",
                    "To remove missing values"
                ],
                "correct_answer": "To predict continuous values",
                "explanation": "Linear regression predicts continuous numerical outputs.",
                "difficulty": "easy"
            },
            {
                "id": 2,
                "question": "Linear regression is mainly used in which type of learning?",
                "options": [
                    "Reinforcement learning",
                    "Supervised learning",
                    "Unsupervised learning",
                    "Transfer learning"
                ],
                "correct_answer": "Supervised learning",
                "explanation": "Linear regression learns from labeled training data.",
                "difficulty": "easy"
            },
            {
                "id": 3,
                "question": "What kind of values does linear regression predict?",
                "options": [
                    "Continuous values",
                    "Images only",
                    "Boolean values only",
                    "Encrypted values"
                ],
                "correct_answer": "Continuous values",
                "explanation": "Its output is usually a numerical continuous value.",
                "difficulty": "easy"
            },
            {
                "id": 4,
                "question": "What does linear regression fit to the observed data?",
                "options": [
                    "A tree structure",
                    "A straight line",
                    "A pie chart",
                    "A database table"
                ],
                "correct_answer": "A straight line",
                "explanation": "Linear regression models data with a straight line.",
                "difficulty": "easy"
            },
            {
                "id": 5,
                "question": "Which of these is a common use of linear regression?",
                "options": [
                    "Trend analysis",
                    "Virus scanning",
                    "Image encryption",
                    "Packet routing"
                ],
                "correct_answer": "Trend analysis",
                "explanation": "Linear regression is often used for forecasting and trend analysis.",
                "difficulty": "medium"
            }
        ]
    }


def test_valid_quiz_schema(valid_quiz_dict):
    quiz = Quiz(**valid_quiz_dict)
    assert quiz.topic == "Linear Regression"
    assert len(quiz.questions) == 5


def test_each_question_has_four_options(valid_quiz_dict):
    quiz = Quiz(**valid_quiz_dict)
    for question in quiz.questions:
        assert len(question.options) == 4


def test_correct_answer_in_options(valid_quiz_dict):
    quiz = Quiz(**valid_quiz_dict)
    validate_quiz_content(quiz)


def test_export_quiz_to_json(tmp_path, valid_quiz_dict):
    quiz = Quiz(**valid_quiz_dict)
    output_file = tmp_path / "quiz.json"

    saved_path = export_quiz_to_json(quiz, str(output_file))

    assert Path(saved_path).exists()

    with open(saved_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data["topic"] == "Linear Regression"
    assert len(saved_data["questions"]) == 5


def test_duplicate_question_detection(valid_quiz_dict):
    valid_quiz_dict["questions"][4]["question"] = valid_quiz_dict["questions"][0]["question"]
    quiz = Quiz(**valid_quiz_dict)

    with pytest.raises(ValueError, match="Duplicate question detected"):
        validate_quiz_content(quiz)


def test_invalid_correct_answer(valid_quiz_dict):
    valid_quiz_dict["questions"][0]["correct_answer"] = "Invalid Option"
    quiz = Quiz(**valid_quiz_dict)

    with pytest.raises(ValueError, match="Correct answer must be one of the provided options"):
        validate_quiz_content(quiz)