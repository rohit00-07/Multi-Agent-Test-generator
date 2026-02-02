from agents.generator import generate_mcq
from agents.validator import validate_mcq

mcq = generate_mcq("DBMS", "Easy", "Fresher")

if not mcq:
    print("Failed to generate MCQ")
else:
    result = validate_mcq(mcq)
    print("Validation result:", result)