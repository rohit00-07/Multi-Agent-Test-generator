from agents.generator import generate_mcq

mcq = generate_mcq("DBMS", "Easy", "Fresher")

if mcq:
    print("MCQ generated successfully:")
    print(mcq)
else:
    print("Invalid MCQ output")