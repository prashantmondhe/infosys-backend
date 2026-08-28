from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from api.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    # Display title
    title = Column(String, nullable=False)

    # Original uploaded filename
    file_name = Column(String, nullable=False)

    # File location on disk
    file_path = Column(String, nullable=False)

    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    uploader = relationship("User")
    department = relationship("Department")