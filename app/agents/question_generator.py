import json
import logging
from pathlib import Path
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from app.schemas.quiz_schema import Quiz
from app.tools.quiz_exporter import export_quiz_to_json
from app.utils.validator import validate_quiz_content


def setup_logger() -> logging.Logger:
    """
    Configure and return a logger for the Question Generator Agent.
    Logs are written to both console and output/question_generator.log.
    """
    log_dir = Path("output")
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("question_generator")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if the module is imported multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_dir / "question_generator.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class QuestionGeneratorAgent:
    """
    Agent responsible for generating structured MCQ quizzes
    from summarized lesson content using a local Ollama model.
    """

    def __init__(self, model_name: str = "llama3.1:8b") -> None:
        self.model_name = model_name
        self.logger = setup_logger()

        self.llm = ChatOllama(
            model=model_name,
            temperature=0.3
        )

        prompt_path = Path("app/prompts/question_generator_prompt.txt")
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        # Escape literal JSON braces in the system prompt
        self.system_prompt = self.system_prompt.replace("{", "{{").replace("}", "}}")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "user",
                    (
                        "Generate a quiz for the following topic and summary.\n\n"
                        "Topic: {topic}\n"
                        "Summary: {summary}\n"
                    ),
                ),
            ]
        )

        self.logger.info("QuestionGeneratorAgent initialized with model: %s", self.model_name)

    def generate_quiz(self, topic: str, summary: str) -> Quiz:
        """
        Generate a validated Quiz object from topic and summary input.

        Args:
            topic: Lesson topic.
            summary: Summarized study content.

        Returns:
            A validated Quiz object.

        Raises:
            ValueError: If topic or summary is invalid.
            json.JSONDecodeError: If the model output is not valid JSON.
        """
        topic = topic.strip()
        summary = summary.strip()

        if not topic:
            self.logger.error("Topic is empty.")
            raise ValueError("Topic cannot be empty.")

        if not summary:
            self.logger.error("Summary is empty.")
            raise ValueError("Summary cannot be empty.")

        self.logger.info("Generating quiz for topic: %s", topic)
        self.logger.info("Summary length: %d characters", len(summary))

        chain = self.prompt | self.llm
        response = chain.invoke({"topic": topic, "summary": summary})

        raw_text = response.content.strip()
        self.logger.info("Received raw response from model.")

        if raw_text.startswith("```json"):
            raw_text = raw_text.removeprefix("```json").removesuffix("```").strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.removeprefix("```").removesuffix("```").strip()

        quiz_dict = json.loads(raw_text)
        quiz = Quiz(**quiz_dict)
        validate_quiz_content(quiz)

        self.logger.info("Quiz validation successful. Generated %d questions.", len(quiz.questions))
        return quiz

    def run(self, state: Dict[str, Any], output_path: str = "output/quiz.json") -> Dict[str, Any]:
        """
        Execute the full question generation flow.

        Args:
            state: Shared workflow state containing at least 'summary' and optionally 'topic'.
            output_path: Destination path for exported quiz JSON.

        Returns:
            Updated state including quiz data and output file path.
        """
        topic = state.get("topic", "Generated Quiz")
        summary = state.get("summary", "")

        self.logger.info("Run started.")
        self.logger.info("Received topic: %s", topic)
        self.logger.info("Using model: %s", self.model_name)

        quiz = self.generate_quiz(topic=topic, summary=summary)
        saved_path = export_quiz_to_json(quiz, output_path)

        self.logger.info("Quiz exported successfully to: %s", saved_path)
        self.logger.info("Run completed successfully.")

        updated_state = dict(state)
        updated_state["quiz"] = quiz.model_dump()
        updated_state["quiz_file"] = saved_path

        return updated_state