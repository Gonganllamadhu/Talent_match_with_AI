from datetime import datetime

from pydantic import BaseModel , HttpUrl, EmailStr



class CandidateApplicationCreate(BaseModel):
    first_name: str 
    last_name: str | None = None 
    email: EmailStr 
    phone: str | None = None 
    linkedin_url: HttpUrl | None = None 
    github_url: HttpUrl | None = None 
    portfolio_url: HttpUrl | None = None


class CandidateApplicationResponse(BaseModel): 
    application_id: int 
    candidate_id: int 
    candidate_profile_id: int 
    job_profile_id: int 
    application_link_id: int | None 
    status: str 
    applied_at: datetime