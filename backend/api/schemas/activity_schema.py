from pydantic import BaseModel


class ActivityCreate(BaseModel):
    user_id: int
    action: str
    module: str


class ActivityResponse(ActivityCreate):
    id: int

    class Config:
        from_attributes = True