import secrets
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.databse.models import ApplicationLinkDB, JobProfileDB


def generate_application_token ():
    """
    Generate a random token
    """
    return secrets.token_urlsafe(32)


def create_application_link(
        db : Session,
        job_profile_id : int,
        created_by : int,
        source : str | None,
        expires_at = None
):
    token = generate_application_token()
    application_link = ApplicationLinkDB(
        job_profile_id = job_profile_id,
        token = token,
        source = source,
        expires_at = expires_at, 
        is_active = True,
        created_by = created_by
    )

    db.add(application_link)
    db.commit()
    db.refresh(application_link)
    return application_link



def get_link_by_token(
        db : Session,
        token : str
):
    return (
        db.query(ApplicationLinkDB).filter(
            ApplicationLinkDB.token == token
        ).first()
    )



def get_link_by_id (
        db : Session,
        job_profile_id : int
):
    return (
        db.query(
            ApplicationLinkDB
        ).filter(
            ApplicationLinkDB.job_profile_id == job_profile_id
        ).first()
    )

def get_links_by_job (
        db : Session,
        job_profile_id : int
):
    return (
        db.query(
            ApplicationLinkDB
        ).filter(
             ApplicationLinkDB.job_profile_id == job_profile_id
        ).first()
    )


def deactivate_application_link(
        db : Session,
        application_link : ApplicationLinkDB
):
    application_link.is_active = False
    db.commit()
    db.refresh(application_link)

    return application_link

def is_link_valid(
        application_link : ApplicationLinkDB
):
    if not application_link.is_active:
        return False

    if application_link.expires_at is not None:
        

        return True


def get_public_job (
        db : Session,
        application_link : ApplicationLinkDB
):
    return (
        db.query(
            JobProfileDB
        ).filter(
            JobProfileDB.id == application_link.job_profile_id
        ).first()
    )