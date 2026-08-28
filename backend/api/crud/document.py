import os
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from api.models.document import Document
from api.models.user import User
from api.models.department import Department
from api.models.activity_log import ActivityLog

UPLOAD_FOLDER = "uploads/documents"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_documents(db: Session):
    documents = db.query(Document).all()

    response = []

    for doc in documents:
        user = db.query(User).filter(User.id == doc.uploaded_by).first()
        department = (
            db.query(Department)
            .filter(Department.id == doc.department_id)
            .first()
        )

        response.append({
            "id": doc.id,
            "title": doc.title,
            "file_name": doc.file_name,
            "file_path": doc.file_path,
            "uploaded_by": user.name if user else "",
            "department": department.name if department else "",
            "created_at": doc.created_at,
        })

    return response


def create_document(
    db: Session,
    title: str,
    department_id: int,
    uploaded_by: int,
    file: UploadFile,
):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_document = Document(
        title=title,
        file_name=file.filename,
        file_path=file_path,
        department_id=department_id,
        uploaded_by=uploaded_by,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # -----------------------------
    # Create Activity Log
    # -----------------------------
    activity = ActivityLog(
        user_id=uploaded_by,
        action=f"Uploaded Document: {db_document.title}",
        module="Documents",
    )

    db.add(activity)
    db.commit()

    return db_document


def delete_document(db: Session, document_id: int):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        return None

    document_title = document.title
    uploaded_by = document.uploaded_by

    # Delete file from storage
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    # Delete database record
    db.delete(document)
    db.commit()

    # -----------------------------
    # Create Activity Log
    # -----------------------------
    activity = ActivityLog(
        user_id=uploaded_by,
        action=f"Deleted Document: {document_title}",
        module="Documents",
    )

    db.add(activity)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }