from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum

class TaskStatusEnum(PyEnum):
    pendiente = "pendiente"
    completada = "completada"
    atrasada = "atrasada"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.pendiente)
    homework_id = Column(Integer, ForeignKey("homeworks.id"), nullable=False)

    homework = relationship("Homework", back_populates="tasks")
