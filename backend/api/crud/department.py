from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models.department import Department
from api.models.document import Document

from api.models.activity_log import ActivityLog
from api.schemas.department import DepartmentCreate


def get_departments(db: Session):
    return db.query(Department).all()


def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(
        name=department.name,
        department_head=department.department_head,
        is_active=department.is_active,
    )

    db.add(db_department)
    db.commit()
    db.refresh(db_department)

    # Activity Log
    activity = ActivityLog(
        user_id=1,  # Change later when login is implemented
        action=f"Created Department: {db_department.name}",
        module="Departments",
    )

    db.add(activity)
    db.commit()

    return db_department


def delete_department(db: Session, department_id: int):
    department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if not department:
        return {"message": "Department not found"}

    document_count = (
        db.query(Document)
        .filter(Document.department_id == department_id)
        .count()
    )

    if document_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete department because {document_count} document(s) belong to it."
        )

    department_name = department.name

    db.delete(department)
    db.commit()

    # Activity Log
    activity = ActivityLog(
        user_id=1,  # Change later when login is implemented
        action=f"Deleted Department: {department_name}",
        module="Departments",
    )

    db.add(activity)
    db.commit()

    return {"message": "Department deleted successfully"}