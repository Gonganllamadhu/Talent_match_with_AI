from sqlalchemy.orm import Session

from ..core.security import (
    create_access_token, create_refresh_token, hash_password, verify_password
)

from ..databse.models import UserDB
from ..databse.models import Role
from ..databse.models import DepartmentDB


def get_user_by_email(
        db : Session,
        email : str
):
    return (
        db.query(UserDB).filter(UserDB.email == email).first()
    )

def get_role_by_id(
        db : Session,
        role_id : int
):
    return (
        db.query(Role).filter(
            Role.id == role_id,
            Role.is_active.is_(True)
        ).first()
    )


def department_by_id(
        db : Session,
        department_id : int
):
    return (
        db.query(DepartmentDB).filter(
            DepartmentDB.id == department_id,
            DepartmentDB.is_active.is_(True)
        ).first()
    )

def create_user(
        db : Session, 
        email : str,
        name : str,
        password : str,
        phone : str | None = None, 
        role_id : int | None= None,
        department_id : int |None = None
):
    password_hash = hash_password(password)

    user = UserDB(
        email = email,
        name = name,
        password_hash = password_hash,
        phone = phone,
        role_id = role_id,
        department_id = department_id,
        is_active = True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def authenticate_user(
        db : Session,
        email : str,
        password : str
):
    user = get_user_by_email(
        db,email
    )
    if not user:
        return None

    if not verify_password(
        password, user.password_hash
    ):
        return None
    if not user.is_active:
        return None

    return user


def generate_tokens(user_id : int):
    access_token = create_access_token(
        user_id
    )
    refresh_token = create_refresh_token(
        user_id
    )
    return {
        "access_token" :access_token,
        "refresh_token" :  refresh_token,
         "token_type": "bearer"
    }
