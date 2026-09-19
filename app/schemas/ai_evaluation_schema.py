
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AIEvaluationResponse(BaseModel):
    id: int

    candidate_id: int
    job_profile_id: int
    application_id: int

    match_score: int = Field(
        ge=0,
        le=100,
    )

    is_match: bool

    recommendation: str

    summary: str | None

    matched_skills: list[str] | None

    missing_skills: list[str] | None

    experience_analysis: str | None

    education_analysis: str | None

    pros: list[str] | None

    cons: list[str] | None

    detailed_analysis: dict[str, Any] | None

    ai_model: str | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class AIEvaluationRequest(BaseModel):
    application_id: int
