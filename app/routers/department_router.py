from fastapi import (
    APIRouter, Depends, HTTPException,status
)

from sqlalchemy.orm import Session

from ..databse.db import get_db

from app.schemas.department_schema import DepartmentRequest, DepartmentResponse
from app.services.department_service import (create_department as create_department_service, get_department, get_department_by_id)


router = APIRouter( prefix="/department", tags=["Department"] )



@router.post("/create", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
     request : DepartmentRequest,
    db : Session = Depends(get_db)
   
):
    role = create_department_service(
        db = db,
        name = request.name,
        description = request.description,
        is_active = request.is_active
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role is not created"
        )
    return role


router.get("/", response_model=list[DepartmentResponse], status_code=status.HTTP_200_OK)
def get_departments(
        db : Session = Depends(get_db)
):
    return get_department(
        db = db
    )


router.get("/{id}", response_model=DepartmentResponse, status_code=status.HTTP_200_OK)
def get_department_by_ids(
         id : int,
        db : Session = Depends(get_db),
       
):
    return get_department_by_id(
        db = db,
        id = id
    )