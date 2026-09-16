from fastapi import ( APIRouter, Depends, HTTPException, Query, status, )
from sqlalchemy.orm import Session
from app.core.authorization import require_roles
from app.core.dependencies import get_current_user
from app.databse.db import get_db
from app.databse.models import (UserDB, JobProfileDB)
from app.schemas.job_profile_schema import (
    JobProfileCreate, JobProfileResponse, JobProfileUpdate
)
from app.services.job_profile_service import (
    create_job_profile, close_job_profile, get_department_by_id, 
    get_job_by_code, get_job_by_id, list_job_profiles,
    pause_job_profile, publish_job_profile, update_job_profile
)

router = APIRouter(
    prefix="/job-profile",
    tags=['Job Profiles']
)


@router.post(
    "",
    response_model=JobProfileResponse,
    status_code= status.HTTP_201_CREATED
)
def create_job (
    request : JobProfileCreate,
    current_user : UserDB = Depends(
        require_roles(
            "ADMIN",
            "HR"
        )
    ),
    db : Session = Depends(get_db) 
):
    department = get_department_by_id(
        db, request.department_id
    )
    if not department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Invalid or inactive department"
        )
    if (request.min_experience is not None 
        and request.max_experience is not None
        and request.min_experience > request.max_experience
        ):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Minimum experince can not be exceed the maximum experience"
        )
    if (request.salary_min is not None 
            and request.salary_max is not None
            and request.salary_min > request.salary_max
            ):
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Minimum salary can not be exceed the maximum salary"
            )

    job = create_job_profile(
         db = db,
         data = request,
         created_by= current_user.id
    )
    return job


@router.get(
     "",
     response_model=list[JobProfileResponse]
)
def get_jobs (
     skip : int = Query(
          default=0,
          ge=0
     ),
     limit : int = Query(
          default= 50,
          ge=1,
          le=100
     ),
     current_user : UserDB = Depends(
          require_roles(
               "ADMIN",
               "HR",
               "MANAGER"
          )
     ),
     db : Session = Depends(get_db)
):
     return list_job_profiles(
          db=db,
          skip=skip,
          limit=limit
     )



@router.get(
     "/{job_id}",
     response_model= JobProfileResponse
)
def get_job(
     job_id : int,
       current_user : UserDB = Depends(
               require_roles(
                    "ADMIN",
                    "HR",
                    "MANAGER"
               )
       ),
       db : Session = Depends(get_db)
):
     job = get_job_by_id(
          db, job_id
     )

     if not job:
          raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= "Job profile not found"
          )

     return job


@router.patch(
     "/{job_id}",
     response_model=JobProfileResponse
)
def update_job (
     job_id : int,
     request : JobProfileUpdate,
     current_user : UserDB = Depends(
                    require_roles(
                         "ADMIN",
                         "HR",
                         "MANAGER"
                    )
            ),
            db : Session = Depends(get_db)

):
     job = get_job_by_id(
          db,
          job_id
     )
     if not job:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail= "Job profile not found"
          )
     if job.status == "CLOSED":
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail= "Closed job profiile can not be updated"
          )

     return update_job_profile( db=db, job=job, data=request, ) 


@router.post(
     "/{job_id}/publish",
     response_model=JobProfileResponse
)
def publish_job (
     job_id : int,
       current_user : UserDB = Depends(
                         require_roles(
                              "ADMIN",
                              "HR",
                              "MANAGER"
                         )
        ),
    db : Session = Depends(get_db)
):
     job = get_job_by_id(
          db, job_id
     )
     if not job:
          raise HTTPException(
               status_code= status.HTTP_404_NOT_FOUND, 
               detail= "Job profile not found"
          )
     published_job = publish_job_profile(
          db, 
          job
     )
     if not published_job:
          raise HTTPException(
               status_code= status.HTTP_400_BAD_REQUEST,
               detail= "Job profile can not be published"
          )
     return published_job



@router.post(
     "/{job_id}/pause",
     response_model=JobProfileResponse
)
def pause_job (
          job_id: int, current_user: UserDB = Depends( require_roles( "ADMIN", "HR", ) ), db: Session = Depends(get_db),
):
     job = get_job_by_id(
               db, job_id
          )
     if not job:
               raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND, 
                    detail= "Job profile not found"
               )
     published_job = pause_job_profile(
               db, 
               job
          )
     if not published_job:
               raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST,
                    detail= "Job profile can not be paused"
               )
     return published_job


@router.post(
     "/{job_id}/close",
     response_model=JobProfileResponse
)
def close_job (
          job_id: int, current_user: UserDB = Depends( require_roles( "ADMIN", "HR", ) ), db: Session = Depends(get_db),
):
     job = get_job_by_id(
               db, job_id
          )
     if not job:
               raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND, 
                    detail= "Job profile not found"
               )
     published_job = close_job_profile(
               db, 
               job
          )
     if not published_job:
               raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST,
                    detail= "Job profile can not be closed"
               )
     return published_job