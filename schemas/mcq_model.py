from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict

class MCQ(BaseModel):
    question_id: str
    domain: Literal["DSA", "OOPs", "DBMS"]
    difficulty: Literal["Easy", "Medium", "Hard"]
    level: Literal["Fresher", "Intermediate"]
    question: str
    options: Dict[Literal["A", "B", "C", "D"], str]
    correct_option: Literal["A", "B", "C", "D"]
    explanation: str
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None