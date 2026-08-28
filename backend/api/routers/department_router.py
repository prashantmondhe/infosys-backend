from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.schemas.department import DepartmentCreate
from api.crud.department import (
    get_departments,
    create_department,
    delete_department,
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_departments(db: Session = Depends(get_db)):
    return get_departments(db)


@router.post("/")
def add_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
):
    return create_department(db, department)


@router.delete("/{department_id}")
def remove_department(
    department_id: int,
    db: Session = Depends(get_db),
):
    return delete_department(db, department_id)