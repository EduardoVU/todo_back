from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class HomeworkStatusEnum(str, Enum):
    pendiente = "pendiente"
    terminada = "terminada"
    atrasada = "atrasada"

class HomeworkBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime = Field(..., description="Fecha de entrega con zona horaria (UTC o local aware)")
    status: Optional[HomeworkStatusEnum] = HomeworkStatusEnum.pendiente

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HomeworkCreate(HomeworkBase):
    user_id: int

class HomeworkUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[HomeworkStatusEnum] = None

    class Config:
        from_attributes = True

class HomeworkOut(HomeworkBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
