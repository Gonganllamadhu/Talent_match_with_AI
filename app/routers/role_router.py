from fastapi import (
    APIRouter, Depends, HTTPException,status
)

from sqlalchemy.orm import Session

from ..databse.db import get_db

from app.schemas.role_schemas import RoleRequest, RoleResponse
from app.services.role_service import (create_role as create_role_service, get_role, get_role_by_id)


router = APIRouter( prefix="/role", tags=["Roles"] )



@router.post("/create", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
     request : RoleRequest,
    db : Session = Depends(get_db)
   
):
    role = create_role_service(
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


@router.get("/", response_model=list[RoleResponse], status_code=status.HTTP_200_OK)
def get_roles_data(
        db : Session = Depends(get_db)
):
    return get_role(
        db = db
    )


@router.get("/{id}", response_model=RoleResponse, status_code=status.HTTP_200_OK)
def get_role_by_id(
         id : int,
        db : Session = Depends(get_db),
       
):
    return get_role_by_id(
        db = db,
        id = id
    )