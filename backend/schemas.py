from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class PredictionResponse(BaseModel):
    bmi: float
    calorie_level: str
    created_at: datetime

    class Config:
        from_attributes = True
