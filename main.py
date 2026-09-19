import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth_router import router as auth_router
from app.routers.role_router import router as role_router
from app.routers.department_router import router as department_router
from app.routers.job_profile_router import router as job_profile_router
from app.routers.application_link_router import router as application_link_router
from app.routers.public_application_router import router as public_application_router
from app.routers.public_candidate_router import router as public_candidate_router
from app.databse.db import Base
from app.databse.db import engine
app = FastAPI(
    title= "Resume builder",
    description="Conversational AI Resume Builder Web Application",
    version="1.0.0"
)


from app.databse.models import (
    UserDB,
   Role,
    DepartmentDB,
    
)



Base.metadata.create_all(
    bind=engine
)



app.include_router(
    auth_router
)
app.include_router(
    role_router
)
app.include_router(
    department_router
)
app.include_router(
    job_profile_router
)

app.include_router(application_link_router)
app.include_router(public_application_router)
app.include_router(public_candidate_router)


@app.get("/")
def root():
    return {
        'message':"AI recrutiment system API"
    }