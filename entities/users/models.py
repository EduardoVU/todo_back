from sqlalchemy import Column, Integer, String, Enum
from database import Base
from sqlalchemy.orm import relationship

from enum import Enum as PyEnum

# Enum para los roles
class RoleEnum(PyEnum):
    admin = "admin"
    cliente = "cliente"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # Nombre obligatorio
    last_name = Column(String(50), nullable=False)  # Apellido obligatorio
    email = Column(String(100), unique=True, nullable=False)  # Correo obligatorio
    password = Column(String(255), nullable=False)  # Contraseña obligatoria (hashed)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.cliente)  # Role obligatorio

    sessions = relationship("Session", back_populates="user")
    homeworks = relationship("Homework", back_populates="user")

