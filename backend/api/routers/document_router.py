from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
)

from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.crud.document import (
    get_documents,
    create_document,
    delete_document,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_documents(db: Session = Depends(get_db)):
    return get_documents(db)


@router.post("/")
def add_document(
    title: str = Form(...),
    department_id: int = Form(...),
    uploaded_by: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return create_document(
        db=db,
        title=title,
        department_id=department_id,
        uploaded_by=uploaded_by,
        file=file,
    )


@router.delete("/{document_id}")
def remove_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    return delete_document(db, document_id)