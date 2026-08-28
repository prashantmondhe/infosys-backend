from sqlalchemy.orm import Session

from api.models.user import User
from api.models.activity_log import ActivityLog

from api.schemas.user import UserCreate


def get_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        department=user.department,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Activity Log
    activity = ActivityLog(
        user_id=db_user.id,
        action=f"Created User: {db_user.name}",
        module="Users",
    )

    db.add(activity)
    db.commit()

    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user_name = user.name

    # Create activity BEFORE deleting the user
    activity = ActivityLog(
        user_id=user.id,
        action=f"Deleted User: {user_name}",
        module="Users",
    )

    db.add(activity)
    db.commit()

    # Delete the user
    db.delete(user)
    db.commit()

    return user