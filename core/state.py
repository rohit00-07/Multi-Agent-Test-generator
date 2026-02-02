from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class OrchestratorState(BaseModel):
    # planning
    domain_plan: List[str]
    difficulty_plan: List[str]

    # limits
    required_count: int
    max_attempts: int

    # runtime
    collected_questions: List[Dict[str, Any]]
    current_mcq: Optional[Dict[str, Any]]
    is_valid: bool
    attempts: int