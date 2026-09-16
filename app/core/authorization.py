from fastapi import Depends, HTTPException, status 
from sqlalchemy.orm import Session 
from app.core.dependencies import get_current_user 

from app.databse.db import get_db
from app.databse.models import (Role, UserDB)



def require_roles(*allowed_roles: str):
    def role_checker(
        current_user: UserDB = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        role = (
            db.query(Role)
            .filter(Role.id == current_user.role_id)
            .first()
        )

        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not found",
            )

        if role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return role_checker

