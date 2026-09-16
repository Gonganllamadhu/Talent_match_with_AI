from sqlalchemy.orm import Session
from app.databse.models import DepartmentDB



def create_department(
        db : Session,
        name : str,
        description : str,
        is_active : bool
):
    role = DepartmentDB(
        name= name,
        description= description,
        is_active=is_active
    )

    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_department(
        db : Session
):
    role = db.query(DepartmentDB).all()
    return role


def get_department_by_id (
        db : Session,
        id : int
):
    return db.query(DepartmentDB).filter(DepartmentDB.id == id).first()
    