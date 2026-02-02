import json
from core.llm_client import call_llm

def validate_mcq(mcq: dict) -> dict:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a strict MCQ validation service for IT hiring. "
                "You do not generate content."
            )
        },
        {
            "role": "user",
            "content": f"""
Validate the following MCQ for correctness and structure.

Rules:
- Exactly 4 options
- Only one correct answer
- Correctness of answer
- Question is clear and technical
- Suitable for IT fresher/intermediate
- Not outdated

Return ONLY one of the following:
VALID
INVALID

MCQ:
{json.dumps(mcq, indent=2)}
"""
        }
    ]

    response = call_llm(messages, temperature=0.1)
    response = response.strip().upper()

    return {
        "question_id": mcq.get("question_id"),
        "status": "VALID" if response == "VALID" else "INVALID"
    }