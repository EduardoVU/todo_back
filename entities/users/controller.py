# controller.py
from fastapi import HTTPException, status
from auth import verify_password, create_access_token, generate_verification_code
from sqlalchemy.orm import Session
from entities.users.models import User
from .repository import UserRepository
from .schemas import UserCreate, UserUpdate
from fastapi.security import OAuth2PasswordRequestForm
from entities.sessions import repository as session_repository
from .models import User, RoleEnum
from sqlalchemy.exc import NoResultFound

def create_user(db: Session, user: UserCreate, current_user: User):
    if user.role == RoleEnum.admin and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Solo un administrador puede crear un usuario administrador")
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este correo")
    
    # Usamos el repositorio para crear el usuario
    return UserRepository.create_user(db=db, user_data=user)

def get_all_users(db: Session, current_user: User):
    if current_user.role != RoleEnum.admin:
         raise HTTPException(status_code=403, detail="Solo un administrador puede ver todos los usuarios")
     
    return UserRepository.get_all_users(db=db)

def get_by_id_users(db: Session, user_id: int, current_user: User):
    if current_user.role != RoleEnum.admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este usuario")
    
    return UserRepository.get_by_id_users(db=db, user_id=user_id)

def update_user(db: Session, user: UserUpdate, current_user: User):
    # Obtener el usuario objetivo (el que se quiere editar)
    user_to_update = UserRepository.get_by_id_users(db, user.id)

    # Prevenir que alguien que no sea admin se asigne el rol de admin
    if user.role == RoleEnum.admin and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Solo un administrador puede asignar el rol de administrador")

    if not user_to_update:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Clientes solo pueden editarse a sí mismos
    if current_user.role == RoleEnum.cliente and current_user.id != user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar a este usuario")

    # Admins no pueden editar a otros admins (solo a sí mismos o a clientes)
    if current_user.role == RoleEnum.admin and current_user.id != user.id and user_to_update.role == RoleEnum.admin:
        raise HTTPException(status_code=403, detail="No puedes editar a otro administrador")

    return UserRepository.update_user(db=db, user_data=user)

def delete_user(db: Session, user_id: int, current_user: User):
    try:
        user_to_delete = UserRepository.get_by_id_users(db, user_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado"
        )

    # Validaciones de rol
    from entities.users.models import RoleEnum

    if current_user.role == RoleEnum.admin:
        if RoleEnum(user_to_delete.role) == RoleEnum.admin and user_to_delete.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Un administrador no puede eliminar a otro administrador"
            )
    elif current_user.role == RoleEnum.cliente:
        if user_to_delete.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Un cliente solo puede eliminar su propia cuenta"
            )

    return UserRepository.delete_user(db=db, user_id=user_id)

def login_user(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Creamos el token de acceso y su expiración
    token, expires_at = create_access_token(data={"sub": str(user.id)})

    # Generamos un código alfanumérico de verificación
    verification_code = generate_verification_code()

    # Guardamos la sesión sin incluir el token, solo el código y expires_at
    session_repository.create_session(
        db=db,
        user_id=user.id,
        code=verification_code,
        expires_at=expires_at
    )

    user_data = get_by_id_users(db=db, user_id=user.id, current_user=user)

    return { "success": True, "access_token": token, "token_type": "bearer", "user": user_data }

def logout_user(db: Session, current_user: User):
    session = session_repository.get_active_session(db, current_user.id)

    if not session:
        raise HTTPException(status_code=404, detail="No hay sesión activa para cerrar")

    session_repository.delete_session(db, session.id)

    return { "detail": "Sesión cerrada correctamente", "success": True }