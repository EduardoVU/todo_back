from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatusEnum(str, Enum):
    pendiente = "pendiente"
    completada = "completada"
    atrasada = "atrasada"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    status: Optional[TaskStatusEnum] = TaskStatusEnum.pendiente
    homework_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatusEnum] = None

class TaskOut(TaskBase):
    id: int

    class Config:
        from_attributes = True
