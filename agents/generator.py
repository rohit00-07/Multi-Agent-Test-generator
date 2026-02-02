import re
from pydantic import ValidationError
from schemas.mcq_model import MCQ
from core.llm_client import call_llm

MAX_RETRIES = 5

def parse_mcq(text: str, domain: str, difficulty: str, level: str) -> dict | None:    
    try:
        question = re.search(r"QUESTION:\n(.+?)\n\nOPTIONS:", text, re.S).group(1).strip()
        options_block = re.search(r"OPTIONS:\n(.+?)\n\nANSWER:", text, re.S).group(1)
        answer = re.search(r"ANSWER:\n([A-D])", text).group(1)
        explanation = re.search(r"EXPLANATION:\n(.+)", text, re.S).group(1).strip()

        options = {}
        for line in options_block.strip().split("\n"):
            key, value = line.split(".", 1)
            options[key.strip()] = value.strip()

        return {
            "question_id": "auto-generated",
            "domain": domain,
            "difficulty": difficulty,
            "level": level,
            "question": question,
            "options": options,
            "correct_option": answer,
            "explanation": explanation,
            "sample_input": None,
            "sample_output": None
        }
    except Exception:
        return None


def generate_mcq(domain: str, difficulty: str, level: str, avoid_questions=None) -> dict | None:
    if avoid_questions is None:
        avoid_questions = []
    for _ in range(MAX_RETRIES):
        messages = [
    {
        "role": "system",
        "content": "You generate technical MCQs for IT hiring."
    },
    {
        "role": "user",
        "content": f"""
Generate ONE MCQ in the following format:

QUESTION:
<question>

OPTIONS:
A. <option>
B. <option>
C. <option>
D. <option>

ANSWER:
<single letter>

EXPLANATION:
<short explanation>

IMPORTANT:
Do NOT generate questions similar to the following:
{avoid_questions}

Domain: {domain}
Difficulty: {difficulty}
Level: {level}
"""
    }
    ]

        raw = call_llm(messages, temperature=0.4)
        parsed = parse_mcq(raw, domain, difficulty, level)

        if not parsed:
            print("⚠️ Failed to parse MCQ")
            continue

        try:
            mcq = MCQ(**parsed)
            return mcq.model_dump()
        except ValidationError as e:
            print("⚠️ Validation error:", e)
            continue

    return None