from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, timezone
from database import Base
from enum import Enum as PyEnum

class HomeworkStatusEnum(str, PyEnum):
    pendiente = "pendiente"
    completada = "completada"
    atrasada = "atrasada"

class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    status = Column(SqlEnum(HomeworkStatusEnum), default=HomeworkStatusEnum.pendiente, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="homeworks")
    tasks = relationship("Task", back_populates="homework", cascade="all, delete-orphan")
