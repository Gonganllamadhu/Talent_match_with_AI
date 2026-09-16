import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Integer, Boolean, Numeric, JSON, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy.dialects.postgresql import JSON


Base = declarative_base()

def utc_now():
    return datetime.now(timezone.utc)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    phone = Column(String(20), nullable=True)
    role_id = Column(
        Integer, 
        ForeignKey("roles.id"),
        nullable=False
    )
    department_id =Column (
        Integer, 
        ForeignKey('departments.id'),
        nullable=True
    )
    is_active = Column(
        Boolean, default=True
    )



class Role (Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    description = Column(
        String(255),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )




class DepartmentDB(Base):
    __tablename__ = "departments"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description = Column(
        String(255),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )



class JobProfileDB(Base):
    __tablename__ = "job_profiles"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    job_code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    responsibilities = Column(
        Text,
        nullable=True,
    )

    requirements = Column(
        Text,
        nullable=True,
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False,
        index=True,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    employment_type = Column(
        String(50),
        nullable=False,
    )

    work_mode = Column(
        String(50),
        nullable=False,
    )

    location = Column(
        String(255),
        nullable=True,
    )

    min_experience = Column(
        Numeric(4, 1),
        nullable=True,
    )

    max_experience = Column(
        Numeric(4, 1),
        nullable=True,
    )

    required_skills = Column(
        JSON,
        nullable=True,
    )

    preferred_skills = Column(
        JSON,
        nullable=True,
    )

    salary_min = Column(
        Numeric(12, 2),
        nullable=True,
    )

    salary_max = Column(
        Numeric(12, 2),
        nullable=True,
    )

    status = Column(
        String(30),
        default="DRAFT",
        nullable=False,
        index=True,
    )

    published_at = Column(
        DateTime,
        nullable=True,
    )

    closed_at = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )

    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
    )


class ApplicationLinkDB(Base):
    __tablename__ = "application_links"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    job_profile_id = Column(
        Integer,
        ForeignKey("job_profiles.id"),
        nullable=False,
        index=True,
    )

    token = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    source = Column(
        String(50),
        nullable=True,
    )

    expires_at = Column(
        DateTime,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )



class CandidateDB(Base):
    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    first_name = Column(
        String(100),
        nullable=False,
    )

    last_name = Column(
        String(100),
        nullable=True,
    )

    email = Column(
        String(255),
        nullable=False,
        index=True,
    )

    phone = Column(
        String(20),
        nullable=True,
    )

    location = Column(
        String(255),
        nullable=True,
    )

    linkedin_url = Column(
        String(500),
        nullable=True,
    )

    github_url = Column(
        String(500),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )

    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
    )


class CandidateProfileDB(Base):
    __tablename__ = "candidate_profiles"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    professional_summary = Column(
        Text,
        nullable=True,
    )

    current_company = Column(
        String(255),
        nullable=True,
    )

    current_designation = Column(
        String(255),
        nullable=True,
    )

    total_experience_years = Column(
        Numeric(5, 2),
        nullable=True,
    )

    highest_education = Column(
        String(255),
        nullable=True,
    )

    education_details = Column(
        JSON,
        nullable=True,
    )

    skills = Column(
        JSON,
        nullable=True,
    )

    work_experience = Column(
        JSON,
        nullable=True,
    )

    projects = Column(
        JSON,
        nullable=True,
    )

    certifications = Column(
        JSON,
        nullable=True,
    )

    languages = Column(
        JSON,
        nullable=True,
    )

    resume_url = Column(
        String(1000),
        nullable=True,
    )

    resume_text = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )

    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
    )



class CandidateApplicationDB(Base):
    __tablename__ = "candidate_applications"

    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "job_profile_id",
            name="uq_candidate_job_application",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    job_profile_id = Column(
        Integer,
        ForeignKey("job_profiles.id"),
        nullable=False,
        index=True,
    )

    application_link_id = Column(
        Integer,
        ForeignKey("application_links.id"),
        nullable=True,
        index=True,
    )

    status = Column(
        String(50),
        default="APPLIED",
        nullable=False,
        index=True,
    )

    applied_at = Column(
        DateTime,
        default=utc_now,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )

    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
    )

class AIEvaluationDB(Base):
    __tablename__ = "ai_evaluations"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    job_profile_id = Column(
        Integer,
        ForeignKey("job_profiles.id"),
        nullable=False,
        index=True,
    )

    application_id = Column(
        Integer,
        ForeignKey("candidate_applications.id"),
        nullable=False,
        index=True,
    )

    overall_score = Column(
        Numeric(5, 2),
        nullable=False,
    )

    skill_match_score = Column(
        Numeric(5, 2),
        nullable=True,
    )

    experience_match_score = Column(
        Numeric(5, 2),
        nullable=True,
    )

    education_match_score = Column(
        Numeric(5, 2),
        nullable=True,
    )

    role_match_score = Column(
        Numeric(5, 2),
        nullable=True,
    )

    is_match = Column(
        Boolean,
        nullable=False,
    )

    match_level = Column(
        String(50),
        nullable=False,
    )

    recommendation = Column(
        String(50),
        nullable=False,
    )

    summary = Column(
        Text,
        nullable=True,
    )

    pros = Column(
        JSON,
        nullable=True,
    )

    cons = Column(
        JSON,
        nullable=True,
    )

    missing_skills = Column(
        JSON,
        nullable=True,
    )

    matched_skills = Column(
        JSON,
        nullable=True,
    )

    reasoning = Column(
        Text,
        nullable=True,
    )

    confidence_score = Column(
        Numeric(5, 2),
        nullable=True,
    )

    ai_model = Column(
        String(100),
        nullable=True,
    )

    prompt_version = Column(
        String(50),
        nullable=True,
    )

    status = Column(
        String(30),
        default="COMPLETED",
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )

    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
    )


class CandidateNoteDB(Base):
    __tablename__ = "candidate_notes"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    job_profile_id = Column(
        Integer,
        ForeignKey("job_profiles.id"),
        nullable=True,
        index=True,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    note = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )

    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
    )



class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    action = Column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_type = Column(
        String(100),
        nullable=False,
    )

    entity_id = Column(
        Integer,
        nullable=True,
        index=True,
    )

    old_data = Column(
        JSON,
        nullable=True,
    )

    new_data = Column(
        JSON,
        nullable=True,
    )

    ip_address = Column(
        String(50),
        nullable=True,
    )

    user_agent = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
    )