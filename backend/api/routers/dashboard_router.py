from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from api.database import SessionLocal

from api.models.user import User
from api.models.document import Document
from api.models.department import Department

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def dashboard(db: Session = Depends(get_db)):
    return {
        "total_users": db.query(func.count(User.id)).scalar(),
        "total_documents": db.query(func.count(Document.id)).scalar(),
        "total_departments": db.query(func.count(Department.id)).scalar(),
    }