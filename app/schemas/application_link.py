from datetime import datetime
from pydantic import BaseModel


class ApplicationLinkCreate(BaseModel):
    source : str | None = None
    expires_at : datetime | None


class ApplicationLinkResponse(BaseModel):
    id : int
    job_profile_id : int
    token : str
    source : str = None
    expires_at : datetime | None
    is_active : bool
    created_by : int
    created_at : datetime


    class PublicJobResponse(BaseModel): 
        job_profile_id: int 
        job_code: str 
        title: str 
        description: str 
        responsibilities: str | None 
        requirements: str | None 
        employment_type: str 
        work_mode: str 
        location: str | None 
        min_experience: float | None 
        max_experience: float | None 
        required_skills: list[str] | None 
        preferred_skills: list[str] | None 
        salary_min: float | None 
        salary_max: float | None 
        application_link_id: int