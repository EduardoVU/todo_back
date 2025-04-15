# repository.py
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, UserResponse, UserUpdate
from passlib.context import CryptContext  # Usamos passlib para hash de contraseñas
from sqlalchemy.orm.exc import NoResultFound

# Crear un contexto de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        hashed_password = pwd_context.hash(user_data.password)
        
        db_user = User(
            name=user_data.name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserRepository.get_by_id_users(db, db_user.id)

    @staticmethod
    def get_all_users(db: Session):
        users = db.query(User).all()
        return [UserResponse.model_validate(user) for user in users]

    @staticmethod
    def get_by_id_users(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NoResultFound(f"Usuario con id {user_id} no encontrado")
        return UserResponse.model_validate(user)

    @staticmethod
    def update_user(db: Session, user_data: UserUpdate):
        db_user = db.query(User).filter(User.id == user_data.id).first()
        if not db_user:
            raise NoResultFound(f"Usuario con id {user_data.id} no encontrado")
        
        if user_data.name is not None:
            db_user.name = user_data.name
        if user_data.last_name is not None:
            db_user.last_name = user_data.last_name
        if user_data.email is not None:
            db_user.email = user_data.email
        if user_data.password is not None:
            db_user.password = pwd_context.hash(user_data.password)
        if user_data.role is not None:
            db_user.role = user_data.role
        
        db.commit()
        db.refresh(db_user)
        return UserRepository.get_by_id_users(db, db_user.id)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise NoResultFound(f"Usuario con id {user_id} no encontrado")
        
        db.delete(db_user)
        db.commit()
        return {"message": f"Usuario con id {user_id} eliminado correctamente"}