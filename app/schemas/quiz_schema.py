from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


class Question(BaseModel):
    id: int = Field(..., gt=0)
    question: str = Field(..., min_length=5)
    options: List[str]
    correct_answer: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=3)
    difficulty: Literal["easy", "medium"]

    @field_validator("options")
    @classmethod
    def validate_options(cls, value: List[str]) -> List[str]:
        if len(value) != 4:
            raise ValueError("Each question must contain exactly 4 options.")

        cleaned = [opt.strip() for opt in value]
        if any(not opt for opt in cleaned):
            raise ValueError("Options cannot be empty.")

        return cleaned

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Correct answer cannot be empty.")
        return value


class Quiz(BaseModel):
    topic: str = Field(..., min_length=2)
    questions: List[Question]

    @field_validator("questions")
    @classmethod
    def validate_question_count(cls, value: List[Question]) -> List[Question]:
        if len(value) != 5:
            raise ValueError("Quiz must contain exactly 5 questions.")
        return value