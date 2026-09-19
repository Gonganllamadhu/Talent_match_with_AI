
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.databse.db import get_db
from app.schemas.candidate_schemas import CandidateApplicationResponse

from app.services.application_link_service import (
    get_link_by_token,
    get_public_job,
    is_link_valid,
)
from app.services.candidate_service import (
    create_candidate,
    create_candidate_application,
    create_candidate_profile,
    get_candidate_by_email,
    get_existing_application,
)
from app.utils.file_storage import save_resume


router = APIRouter(
    prefix="/public",
    tags=["Public Candidate Applications"],
)


@router.post(
    "/apply/{token}",
    response_model=CandidateApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_application(
    token: str,

    first_name: str = Form(...),
    last_name: str | None = Form(None),
    email: str = Form(...),
    phone: str | None = Form(None),

    linkedin_url: str | None = Form(None),
    github_url: str | None = Form(None),
    portfolio_url: str | None = Form(None),

    resume: UploadFile = File(...),

    db: Session = Depends(get_db),
):
    # --------------------------------------------------
    # 1. Validate application link
    # --------------------------------------------------

    application_link = get_link_by_token(
        db,
        token,
    )

    if not application_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application link not found",
        )

    if not is_link_valid(application_link):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Application link is expired or inactive",
        )

    # --------------------------------------------------
    # 2. Get job
    # --------------------------------------------------

    job = get_public_job(
        db,
        application_link,
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job profile not found",
        )

    if job.status != "PUBLISHED":
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This job is no longer accepting applications",
        )

    # --------------------------------------------------
    # 3. Validate basic candidate data
    # --------------------------------------------------

    first_name = first_name.strip()
    email = email.strip().lower()

    if not first_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="First name is required",
        )

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required",
        )

    # --------------------------------------------------
    # 4. Check whether candidate already exists
    # --------------------------------------------------

    candidate = get_candidate_by_email(
        db,
        email,
    )

    if candidate is None:
        candidate = create_candidate(
            db=db,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )

    # --------------------------------------------------
    # 5. Prevent duplicate application
    # --------------------------------------------------

    existing_application = get_existing_application(
        db=db,
        candidate_id=candidate.id,
        job_profile_id=job.id,
    )

    if existing_application:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied for this job",
        )

    # --------------------------------------------------
    # 6. Save resume
    # --------------------------------------------------

    original_filename, stored_path = await save_resume(
        resume
    )

    # --------------------------------------------------
    # 7. Create candidate profile
    # --------------------------------------------------

    profile = (
        db.query(
            __import__(
                "app.models.candidate_profile",
                fromlist=[
                    "CandidateProfileDB"
                ],
            ).CandidateProfileDB
        )
        .filter(
            __import__(
                "app.models.candidate_profile",
                fromlist=[
                    "CandidateProfileDB"
                ],
            ).CandidateProfileDB.candidate_id
            == candidate.id
        )
        .first()
    )

    if profile is None:
        profile = create_candidate_profile(
            db=db,
            candidate_id=candidate.id,
            linkedin_url=linkedin_url,
            github_url=github_url,
            portfolio_url=portfolio_url,
            resume_file_name=original_filename,
            resume_file_path=stored_path,
        )
    else:
        profile.linkedin_url = linkedin_url
        profile.github_url = github_url
        profile.portfolio_url = portfolio_url
        profile.resume_file_name = original_filename
        profile.resume_file_path = stored_path

    # --------------------------------------------------
    # 8. Create application
    # --------------------------------------------------

    application = create_candidate_application(
        db=db,
        candidate_id=candidate.id,
        job_profile_id=job.id,
        application_link_id=application_link.id,
    )

    # --------------------------------------------------
    # 9. Commit everything
    # --------------------------------------------------

    db.commit()

    db.refresh(application)
    db.refresh(profile)

    return {
        "application_id": application.id,
        "candidate_id": candidate.id,
        "candidate_profile_id": profile.id,
        "job_profile_id": job.id,
        "application_link_id": application_link.id,
        "status": application.status,
        "applied_at": application.applied_at,
    }
