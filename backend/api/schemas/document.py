from pydantic import BaseModel
from datetime import datetime


class DocumentCreate(BaseModel):
    title: str
    department_id: int
    uploaded_by: int


class DocumentResponse(BaseModel):
    id: int
    title: str
    file_name: str
    file_path: str

    uploaded_by: str      # User name
    department: str       # Department name

    created_at: datetime

    class Config:
        from_attributes = True