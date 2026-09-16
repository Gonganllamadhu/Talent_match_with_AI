from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer 
from jose import JWTError, jwt 
from sqlalchemy.orm import Session

from config import settings
from app.databse.db import get_db
from app.databse.models import UserDB

security = HTTPBearer()

def get_current_user(
        credentials : HTTPAuthorizationCredentials= Depends(security),
        db : Session = Depends(get_db)
):
    token = credentials.credentials

    try :

        payload = jwt.decode(
            token,
            settings.Settings.SECRET_KEY,
            algorithms=[settings.Settings.ALGORITHM]
        )
    
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if user_id is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token", headers={"WWW-Authenticate": "Bearer"},
            )

        if token_type != "access": 
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token required", headers={"WWW-Authenticate": "Bearer"}, )

    except JWTError: raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"}, )

    user = ( db.query(UserDB) .filter(UserDB.id == int(user_id)) .first() )

    if not user: 
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={"WWW-Authenticate": "Bearer"}, ) 
    if not user.is_active: 
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive", ) 
    return user