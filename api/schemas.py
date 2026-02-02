from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Any

class GenerateTestRequest(BaseModel):
    domains: Dict[str, int] = Field(..., description="Domain -> question count")
    difficulty_mix: Dict[str, int] = Field(..., description="Difficulty -> percentage")
    level: Literal["Fresher", "Intermediate"]
    max_attempts: int = Field(default=50, ge=1, le=200)


class GenerateTestResponse(BaseModel):
    status: Literal["SUCCESS", "FAILED"]
    total_questions: int
    questions: List[Dict[str, Any]] = Field(
        ..., description="List of validated MCQs"
    )