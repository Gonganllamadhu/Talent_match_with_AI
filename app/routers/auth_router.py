from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session
from app.databse.models import UserDB
from ..databse.db import get_db
from app.core.authorization import require_roles 
from app.core.dependencies import get_current_user
from jose import JWTError
from app.databse.models import (UserDB, Role, DepartmentDB)

from app.core.authorization import require_roles 
from app.core.dependencies import get_current_user 
from app.core.security import decode_token

from ..schemas.auth import (
    LoginRequest,
    SignupRequest,
    SignupResponse,
    TokenResponse
)

from ..services.auth_service import (
    create_user,
    authenticate_user,
    generate_tokens,
    get_user_by_email,
    get_role_by_id, department_by_id
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    request: SignupRequest,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(
        db,
        request.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    if request.role_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="role_id is required"
        )
    role = get_role_by_id(
        db, request.role_id
    )
    if not role:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or Inactive role"
                )
    if request.department_id is not None:
        department = department_by_id(
            db, request.department_id
        )
        if not department:
            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid or Inactive department"
                            )

    user = create_user(
        db=db,
        email=request.email,
        name=request.name,
        password=request.password,
        phone=request.phone,
        role_id=request.role_id,
        department_id=request.department_id,
    )

    tokens = generate_tokens(user.id)

    return {
        "user": user,
        "tokens": tokens
    }


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db=db,
        email=request.email,
        password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return generate_tokens(user.id)


@router.get( "/me" ) 
def get_me( current_user: UserDB = Depends(get_current_user), ): 
    return current_user 

@router.get( "/hr-only" ) 
def hr_only( current_user: UserDB = Depends( require_roles("ADMIN", "HR") ), ): 
    return current_user



