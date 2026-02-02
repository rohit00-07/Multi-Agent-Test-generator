from agents.generator import generate_mcq
from agents.validator import validate_mcq

def generate_node(state):
    state.attempts += 1
    index = len(state.collected_questions)
    difficulty = state.difficulty_plan[index]
    domain = state.domain_plan[index]

    print(f"🔄 Generating MCQ for domain: {domain}")

    previous_questions = [
        q["question"] for q in state.collected_questions
    ]

    mcq = generate_mcq(
        domain=domain,
        difficulty=difficulty,
        level="Fresher",
        avoid_questions=previous_questions
    )

    state.current_mcq = mcq
    return state

def validate_node(state):
    print("🔍 Validating MCQ...")
    mcq = state.current_mcq

    if not mcq:
        print("⚠️ No MCQ to validate")
        state.is_valid = False
        return state

    result = validate_mcq(mcq)
    print("🧪 Validator result:", result["status"])

    state.is_valid = result["status"] == "VALID"
    return state

def store_node(state):
    if state.is_valid:
        new_q = state.current_mcq["question"]

        existing_questions = {
            q["question"] for q in state.collected_questions
        }

        if new_q in existing_questions:
            print("⚠️ Duplicate question detected, skipping")
        else:
            print("✅ MCQ accepted")
            state.collected_questions.append(state.current_mcq)
    else:
        print("❌ MCQ rejected")

    return state