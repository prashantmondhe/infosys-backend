from sqlalchemy.orm import Session

from api.models.activity_log import ActivityLog
from api.models.user import User

from api.schemas.activity_schema import ActivityCreate


def create_activity(db: Session, activity: ActivityCreate):
    db_activity = ActivityLog(**activity.model_dump())

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity


def get_activities(db: Session):
    activities = (
        db.query(ActivityLog)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )

    response = []

    for activity in activities:
        user = (
            db.query(User)
            .filter(User.id == activity.user_id)
            .first()
        )

        response.append(
            {
                "id": activity.id,
                "user_name": user.name if user else "System",
                "action": activity.action,
                "module": activity.module,
                "created_at": activity.created_at,
            }
        )

    return response