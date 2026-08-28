from sqlalchemy import func
from sqlalchemy.orm import Session

from api.models.document import Document


def get_document_trend(db: Session):
    month = func.date_trunc("month", Document.created_at)

    result = (
        db.query(
            month.label("month"),
            func.count(Document.id).label("documents"),
        )
        .group_by(month)
        .order_by(month)
        .all()
    )

    return [
        {
            "month": row.month.strftime("%b"),
            "documents": row.documents,
        }
        for row in result
    ]