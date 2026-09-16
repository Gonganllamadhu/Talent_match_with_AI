
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


class JobProfileCreate(BaseModel):
    job_code: str = Field(
        min_length=2,
        max_length=50,
    )

    title: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str = Field(
        min_length=10,
    )

    responsibilities: str | None = None

    requirements: str | None = None

    department_id: int

    employment_type: str = Field(
        min_length=2,
        max_length=50,
    )

    work_mode: str = Field(
        min_length=2,
        max_length=50,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    min_experience: Decimal | None = Field(
        default=None,
        ge=0,
        le=50,
    )

    max_experience: Decimal | None = Field(
        default=None,
        ge=0,
        le=50,
    )

    required_skills: list[str] | None = None

    preferred_skills: list[str] | None = None

    salary_min: Decimal | None = Field(
        default=None,
        ge=0,
    )

    salary_max: Decimal | None = Field(
        default=None,
        ge=0,
    )


class JobProfileUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        min_length=10,
    )

    responsibilities: str | None = None

    requirements: str | None = None

    department_id: int | None = None

    employment_type: str | None = Field(
        default=None,
        max_length=50,
    )

    work_mode: str | None = Field(
        default=None,
        max_length=50,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    min_experience: Decimal | None = Field(
        default=None,
        ge=0,
        le=50,
    )

    max_experience: Decimal | None = Field(
        default=None,
        ge=0,
        le=50,
    )

    required_skills: list[str] | None = None

    preferred_skills: list[str] | None = None

    salary_min: Decimal | None = Field(
        default=None,
        ge=0,
    )

    salary_max: Decimal | None = Field(
        default=None,
        ge=0,
    )


class JobProfileResponse(BaseModel):
    id: int
    job_code: str
    title: str
    description: str
    responsibilities: str | None
    requirements: str | None

    department_id: int
    created_by: int

    employment_type: str
    work_mode: str
    location: str | None

    min_experience: Decimal | None
    max_experience: Decimal | None

    required_skills: list[str] | None
    preferred_skills: list[str] | None

    salary_min: Decimal | None
    salary_max: Decimal | None

    status: str

    published_at: datetime | None
    closed_at: datetime | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

