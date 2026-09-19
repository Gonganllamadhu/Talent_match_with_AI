

from sqlalchemy.orm import Session 


from app.databse.models import (
    CandidateApplicationDB, CandidateDB, CandidateProfileDB
)


def get_candidate_by_email(
        db : Session,
        email : str
):
    return (
        db.query(
            CandidateDB
        ).filter(
            CandidateDB.email == email.lower().strip()
        ).first()
    )


def create_candidate (
        db: Session, 
        first_name: str,
        last_name: str | None,
        email: str, 
        phone: str | None,
):
    candidate = CandidateDB(
        first_name = first_name,
        last_name = last_name,
        email = email, 
        phone = phone,
        is_active = True
    )

    db.add(candidate)
    db.refresh()

    return candidate

def create_candidate_profile( db: Session, candidate_id: int, linkedin_url: str | None, github_url: str | None, portfolio_url: str | None, resume_file_name: str, resume_file_path: str, ):
    profile = CandidateProfileDB( candidate_id=candidate_id, linkedin_url=linkedin_url, github_url=github_url, portfolio_url=portfolio_url, resume_file_name=resume_file_name, resume_file_path=resume_file_path, )

    db.add(profile)
    db.refresh()

    return profile



def create_candidate_application( db: Session, candidate_id: int, job_profile_id: int, application_link_id: int | None, ):
    application = CandidateApplicationDB( candidate_id=candidate_id, job_profile_id=job_profile_id, application_link_id=application_link_id, status="SUBMITTED", )

    db.add(application)
    db.refresh()

    return application


def get_existing_application( db: Session, candidate_id: int, job_profile_id: int, ):
    return ( db.query(CandidateApplicationDB) .filter( CandidateApplicationDB.candidate_id == candidate_id, CandidateApplicationDB.job_profile_id == job_profile_id, ) .first() )

