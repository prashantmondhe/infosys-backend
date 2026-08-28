from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.schemas.activity_schema import ActivityCreate
from api.crud.activity import create_activity, get_activities

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    return create_activity(db, activity)


@router.get("/")
def list_activities(db: Session = Depends(get_db)):
    return get_activities(db)