from fastapi import (
     Depends, HTTPException, Request, status, APIRouter

)

from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.databse.db import get_db
from app.databse.models import ApplicationLinkDB, UserDB
from app.schemas.application_link import ApplicationLinkCreate, ApplicationLinkResponse
from app.services.application_link_service import (
    create_application_link, generate_application_token, deactivate_application_link, get_link_by_id, get_links_by_job, get_link_by_token, get_public_job
)
from app.services.job_profile_service import get_job_by_id


router = APIRouter(
    prefix="/application-links",
    tags=['Application Links']
)


def serialize_application_link (
        link : ApplicationLinkDB
):
    return {
        "id": link.id,
        "job_profile_id":link.job_profile_id,
        "token": link.token,
        "source": link.source,
        "expires_at": link.expires_at,
        "is_active" : link.is_active,
        "created_by" : link.created_by,
        "created_at": link.created_at,

    }


@router.post(
    "/{job_id}",
    response_model=ApplicationLinkResponse,
    status_code=status.HTTP_201_CREATED
)
def create_link (
    job_id : int,
    data : ApplicationLinkCreate,
    request : Request,
    db : Session = Depends(get_db),
    current_user : UserDB = Depends(
        require_roles("ADMIN", "HR")
    )
):
    job = get_job_by_id(
        db ,
        job_id
    )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if job.status != "PUBLISHED":
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Application link can be created for published jobs"
        )

    link = create_application_link(
        db = db,
        job_profile_id=job.id,
        created_by= current_user.id,
        source= data.source,
        expires_at= data.expires_at
    )

    return link


@router.get(
    "/job/{job_id}"
)
def list_job_links (
    job_id : int,
    db : Session = Depends(
        get_db
    ),
    current_user : UserDB = Depends(
        require_roles("HR", "MANAGER")
    )
):
    job = get_job_by_id(
        db, 
        job_profile_id =job_id
    )
    if not job : 
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= "Job not found"
        )

    return get_link_by_id(
        db,
        job_profile_id =job.id
    )


@router.get(
    "/{link_id}",
    response_model=ApplicationLinkResponse
)
def get_link(
    link_id : int,
    db : Session = Depends(get_db),
    current_user : UserDB = Depends(
        require_roles("HR", 'MANAGER')
    )
):
    link = get_link_by_id (
        db,
        link_id
    )
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'application link not found'
        )

    return link


@router.post(
    "/{link_id}/deactivate",
    response_model=ApplicationLinkResponse
)
def deactivate_link (
    link_id : int,
    request : Request,
    db : Session = Depends(get_db),
    current_user :UserDB = Depends(
require_roles('HR', 'ADMIN')
    )
):
    link = get_link_by_id(
        db, 
        link_id
    )
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Link not found"
        )

    deactivate = deactivate_application_link(
        db= db,
        application_link= link
    )
    return deactivate


    