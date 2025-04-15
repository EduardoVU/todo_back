from pydantic import BaseModel
from enum import Enum
from typing import Optional

# Enum para los roles
class RoleEnum(str, Enum):
    admin = "admin"
    cliente = "cliente"

class UserCreate(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    role: RoleEnum = RoleEnum.cliente  # Valor por defecto

    class Config:
        from_attributes = True 

class UserUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

    class Config:
        from_attributes = True

# Esquema para la respuesta, que no incluye la contraseña
class UserResponse(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    role: RoleEnum

    class Config:
        from_attributes = True
        from_attributes = True