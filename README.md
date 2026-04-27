# 🎓 Automated Personalized Study & Quiz Assistant

## 🧠 Question Generator Agent - IT22129376

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![LangChain](https://img.shields.io/badge/LangChain-Agentic%20AI-purple)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📌 Overview

This repository contains the implementation of the **Question Generator Agent**, developed as part of the **Automated Personalized Study & Quiz Assistant** multi-agent system for:

> 🎓 **SE4010 – CTSE Assignment 2 (Machine Learning)**

This agent is responsible for generating structured multiple-choice quizzes using a **local LLM (Ollama)** based on summarized study material.

---

## ⚙️ System Architecture

```text
Lecture Notes / Study Material
        ↓
Content Summarizer Agent
        ↓
🟢 Question Generator Agent (This Component)
        ↓
Performance Evaluator Agent
        ↓
Study Planner Agent
```

---

## 🎯 Responsibilities

The Question Generator Agent:

* 📥 Receives **topic + summary**
* 🧠 Generates **exactly 5 MCQs**
* ✅ Validates structure and logic
* 💾 Exports quiz to `output/quiz.json`
* 🔄 Returns updated state for next agent

---

## ✨ Features

* 🏠 Fully **local execution** (no paid APIs)
* 🤖 Powered by **Ollama (llama3.1:8b)**
* 📝 Generates structured MCQs:

  * Question ID
  * Question
  * 4 Options
  * Correct Answer
  * Explanation
  * Difficulty
* 🛡️ Schema validation using **Pydantic**
* 🔍 Logical validation layer
* 📦 JSON export support
* 🧪 Unit testing with **pytest**
* 📊 Logging (console + file)

---

## 🧰 Tech Stack

| Category   | Technology           |
| ---------- | -------------------- |
| Language   | Python               |
| LLM        | Ollama (llama3) |
| Framework  | LangChain            |
| Validation | Pydantic             |
| Testing    | Pytest               |
| Config     | python-dotenv        |

---

## 📁 Project Structure

```bash
ctse-assignment-2/
│
├── app/
│   ├── agents/
│   │   └── question_generator.py
│   ├── tools/
│   │   └── quiz_exporter.py
│   ├── utils/
│   │   └── validator.py
│   ├── schemas/
│   │   └── quiz_schema.py
│   ├── prompts/
│   │   └── question_generator_prompt.txt
│   └── main_question_generator.py
│
├── data/
│   └── sample_summary.json
│
├── output/
│   ├── quiz.json
│   └── question_generator.log
│
├── tests/
│   ├── conftest.py
│   └── test_question_generator.py
│
├── requirements.txt
└── .env
```

---

## 🔌 Input Format

```json
{
  "topic": "Linear Regression",
  "summary": "Linear regression is a supervised learning algorithm used to predict continuous numerical values..."
}
```

---

## 📤 Output Format

```json
{
  "topic": "Linear Regression",
  "questions": [
    {
      "id": 1,
      "question": "What type of values does linear regression predict?",
      "options": [
        "Categorical",
        "Discrete Numerical",
        "Continuous Numerical",
        "Ordinal"
      ],
      "correct_answer": "Continuous Numerical",
      "explanation": "Linear regression predicts continuous values.",
      "difficulty": "easy"
    }
  ]
}
```

---

## 🧠 Core Components

### 1. QuestionGeneratorAgent

Main agent responsible for:

* Loading prompt
* Calling Ollama model
* Generating quiz
* Validating output
* Exporting JSON

---

### 2. Quiz Exporter Tool

* Saves quiz to JSON
* Creates directories if needed
* Returns file path

---

### 3. Validator

Performs logical checks:

* ❌ No duplicate questions
* ✅ Correct answer exists in options
* 🎯 Valid difficulty levels

---

### 4. Schema (Pydantic)

Ensures:

* Exactly 5 questions
* Exactly 4 options per question
* Required fields exist

---

## ⚡ Setup Instructions

### 1️⃣ Clone Repo

```bash
git clone <your-repo-url>
cd ctse-assignment-2
```

---

### 2️⃣ Create Virtual Environment

**PowerShell**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**CMD**

```bash
python -m venv venv
venv\Scripts\activate.bat
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Install Ollama

👉 https://ollama.com

```bash
ollama --version
```

---

### 5️⃣ Pull Model

```bash
ollama pull llama3
```

---

### 6️⃣ Test Model

```bash
ollama run llama3
```

---

## ▶️ Running the Agent

```bash
python -m app.main_question_generator
```

### Expected Output

* Reads sample input
* Generates quiz
* Validates results
* Saves to `output/quiz.json`
* Logs execution

---

## 🧪 Running Tests

```bash
pytest
```

```bash
pytest -v
```

---

## 📊 Logging

Logs are stored in:

```bash
output/question_generator.log
```

Includes:

* Initialization
* Model execution
* Validation status
* Export success

---

## ✅ Validation Rules

### Schema Validation

* 5 questions required
* 4 options per question
* Required fields must exist

### Logical Validation

* No duplicate questions
* Correct answer must be valid
* Difficulty must be `easy` or `medium`

---

## 🔄 Workflow

1. Load summary
2. Generate quiz via LLM
3. Validate schema
4. Validate logic
5. Export JSON
6. Pass to next agent

---

## 👨‍💻 Contribution

**Student 2 – Question Generator Agent**

### ✔ Completed

* Agent implementation
* Custom tool development
* Testing & validation
* Logging system
* JSON output pipeline

---

## 📝 Notes

* Runs **fully locally**
* No external APIs required
* Ready for integration with downstream agents

---


