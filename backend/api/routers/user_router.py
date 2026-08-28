from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.schemas.user import UserCreate, UserResponse
from api.services.user_service import (
    get_users,
    create_user,
    delete_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)

    if user:
        return {"message": "User deleted successfully"}

    return {"message": "User not found"}