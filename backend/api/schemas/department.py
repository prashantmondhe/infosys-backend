from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    department_head: str
    is_active: bool = True


class DepartmentResponse(DepartmentCreate):
    id: int

    class Config:
        from_attributes = True