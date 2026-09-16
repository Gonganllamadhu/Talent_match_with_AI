from sqlalchemy.orm import Session
from app.databse.models import Role



def create_role(
        db : Session,
        name : str,
        description : str,
        is_active : bool
):
    role = Role(
        name= name,
        description= description,
        is_active=is_active
    )

    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_role(
        db : Session
):
    role = db.query(Role).all()
    return role


def get_role_by_id (
        db : Session,
        id : int
):
    return db.query(Role).filter(Role.id == id).first()
    