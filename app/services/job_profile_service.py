from app.databse.models import (
    JobProfileDB, DepartmentDB, Role
)

from datetime import datetime, timezone

from sqlalchemy.orm import Session



def get_job_by_id(
        db : Session,
        job_id : int
):
    return db.query(JobProfileDB).filter(
        JobProfileDB.id == job_id
    ).first()


def get_job_by_code(
        db : Session,
        job_code : str
):
    return db.query(JobProfileDB).filter(
        JobProfileDB.id == job_code
    ).first()


def get_department_by_id(
        db : Session,
        department_id : int
):
    return db.query(DepartmentDB).filter(
        DepartmentDB.id == department_id,
        DepartmentDB.is_active.is_(True)
    ).first()


def create_job_profile(
        db : Session,
        data,
        created_by : int
):
    job = JobProfileDB(
      job_code=data.job_code.strip().upper(), 
      title=data.title.strip(),
        description=data.description.strip(), 
        responsibilities=( data.responsibilities.strip() if data.responsibilities else None ), 
        requirements=( data.requirements.strip() if data.requirements else None ), 
        department_id=data.department_id, 
        created_by=created_by, 
        employment_type=data.employment_type.strip(), 
        work_mode=data.work_mode.strip(), 
        location=( data.location.strip() if data.location else None ),
        min_experience=data.min_experience, 
        max_experience=data.max_experience, 
        required_skills=data.required_skills, 
        preferred_skills=data.preferred_skills, 
        salary_min=data.salary_min, 
        salary_max=data.salary_max, 
        status="DRAFT",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def update_job_profile( db: Session, job: JobProfileDB, data, ): 
    update_data = data.model_dump( exclude_unset=True ) 
    for field, value in update_data.items(): 
        if isinstance(value, str): 
            value = value.strip() 
            setattr( job, field, value, ) 

    job.updated_at = datetime.now( timezone.utc ) 
    db.commit() 
    db.refresh(job) 
    return job



def publish_job_profile(
        db : Session,
        job : JobProfileDB
):
    if job.status == "CLOSED":
        return None
    if job.status == "PUBLISHED":
        return job
    job.status ="PUBLISHED"

    job.published_at = datetime.now( timezone.utc )
    job.closed_at = None

    db.commit() 
    db.refresh(job) 
    return job


def pause_job_profile(
        db : Session,
        job : JobProfileDB
):
    if job.status != "PUBLISHED":
        return None
    job.status = "PAUSED"
    db.commit() 
    db.refresh(job) 
    return job


def close_job_profile(
        db : Session,
        job : JobProfileDB
):
    if job.status == "CLOSED":
        return job
    job.status == "CLOSED"

    job.closed_at= datetime.now(
        timezone.utc
    )
    db.commit()
    db.refresh(job)
    return job



def list_job_profiles(
        db : Session,
        skip : int = 0,
        limit : int = 50
):
    return (
        db.query(JobProfileDB).filter(
            JobProfileDB.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )