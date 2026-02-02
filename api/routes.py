from fastapi import APIRouter, Header, HTTPException, Depends
from api.schemas import GenerateTestRequest, GenerateTestResponse
from orchestrator.runner import run_orchestrator
from api.utils import expand_domain_plan, expand_difficulty_plan
from db.database import SessionLocal
from db.models import Test, Question
import os
from dotenv import load_dotenv

load_dotenv()
HR_SECRET_KEY = os.getenv("HR_SECRET_KEY")

router = APIRouter()

@router.post("/generate-test", response_model=GenerateTestResponse)
def generate_test(payload: GenerateTestRequest):
    domain_plan = expand_domain_plan(payload.domains)
    difficulty_plan = expand_difficulty_plan(
        total=len(domain_plan),
        mix=payload.difficulty_mix
    )

    questions = run_orchestrator(
        domain_plan=domain_plan,
        difficulty_plan=difficulty_plan,
        max_attempts=payload.max_attempts
    )

    status = "SUCCESS" if questions else "FAILED"

    # Store in DB only if generation succeeded
    if status == "SUCCESS":
        db = SessionLocal()

        test = Test(
            level=payload.level,
            domains=payload.domains,
            difficulty_mix=payload.difficulty_mix,
            total_questions=len(questions)
        )
        db.add(test)
        db.commit()
        db.refresh(test)

        for q in questions:
            question = Question(
                test_id=test.test_id,
                domain=q["domain"],
                difficulty=q["difficulty"],
                question=q["question"],
                options=q["options"],
                correct_option=q["correct_option"],
                explanation=q["explanation"]
            )
            db.add(question)

        db.commit()
        db.close()

        return {
            "status": status,
            "total_questions": len(questions),
            "questions": questions,
        }

    return {
        "status": status,
        "total_questions": 0,
        "questions": []
    }

@router.get("/tests")
def list_tests():
    db = SessionLocal()
    tests = db.query(Test).all()
    db.close()

    return [
        {
            "test_id": t.test_id,
            "created_at": t.created_at,
            "level": t.level,
            "total_questions": t.total_questions
        }
        for t in tests
    ]

@router.get("/tests/{test_id}")
def get_test(test_id: str):
    db = SessionLocal()

    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        db.close()
        return {"error": "Test not found"}

    questions = (
        db.query(Question)
        .filter(Question.test_id == test_id)
        .all()
    )

    db.close()

    return {
        "test_id": test.test_id,
        "level": test.level,
        "domains": test.domains,
        "difficulty_mix": test.difficulty_mix,
        "total_questions": test.total_questions,
        "questions": [
            {
                "domain": q.domain,
                "difficulty": q.difficulty,
                "question": q.question,
                "options": q.options
                # 🔒 correct_option & explanation intentionally hidden
            }
            for q in questions
        ]
    }
def verify_hr(x_hr_key: str = Header(...)):
    if x_hr_key != HR_SECRET_KEY:
        raise HTTPException(status_code=403, detail="HR access only")

@router.get("/tests/{test_id}/answer-key")
def get_answer_key(test_id: str, _: str = Depends(verify_hr)):
    db = SessionLocal()

    test = db.query(Test).filter(Test.test_id == test_id).first()
    if not test:
        db.close()
        return {"error": "Test not found"}

    questions = (
        db.query(Question)
        .filter(Question.test_id == test_id)
        .all()
    )

    db.close()

    return {
        "test_id": test.test_id,
        "total_questions": test.total_questions,
        "answer_key": [
            {
                "question": q.question,
                "correct_option": q.correct_option,
                "explanation": q.explanation
            }
            for q in questions
        ]
    }
