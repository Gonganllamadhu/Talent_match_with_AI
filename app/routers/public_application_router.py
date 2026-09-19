from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.databse.db import get_db
from app.schemas.application_link import ApplicationLinkResponse 

from app.services.application_link_service import (
    is_link_valid, get_link_by_token, get_public_job
)

router = APIRouter(
    prefix="/public",
    tags=['Public application']
)


@router.get(
    '/apply/{token}'
)
def get_public_application (
    token : str,
    db : Session = Depends(
        get_db
    )
):
    link = get_link_by_token(
        db=db,
        token=token
    )
    if not link :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Application Link not found"
        )

    if not  is_link_valid(link):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Application link is expired or inactive"
        )

    job = get_public_job(
        db,
        link
    )

    if not job : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "job not found"
        )

    return {
    "job_profile_id": job.id,
    "job_code": job.job_code,
    "title": job.title,
    "description": job.description,
    "responsibilities": job.responsibilities,
    "requirements": job.requirements,
    "employment_type": job.employment_type,
    "work_mode": job.work_mode,
    "location": job.location,
    "min_experience": ( float(job.min_experience) if job.min_experience is not None else None ),
    "max_experience": ( float(job.max_experience) if job.max_experience is not None else None ),
    "required_skills": job.required_skills,
    "preferred_skills": job.preferred_skills,
    "salary_min": ( float(job.salary_min) if job.salary_min is not None else None ),
    "salary_max": ( float(job.salary_max) if job.salary_max is not None else None ),
    "application_link_id": link.id,
}