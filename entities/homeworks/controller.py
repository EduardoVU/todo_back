from fastapi import HTTPException
from sqlalchemy.orm import Session
from entities.users.models import RoleEnum, User
from .schemas import HomeworkCreate, HomeworkUpdate
from .models import HomeworkStatusEnum
from . import repository
from datetime import datetime, timezone

def create_homework(db: Session, homework_data: HomeworkCreate, current_user: User):
    # Si el usuario actual es cliente, solo puede asignarse tareas a sí mismo
    if current_user.role == RoleEnum.cliente and homework_data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para asignar tareas a otros usuarios")

    return repository.create_homework(db=db, homework_data=homework_data)

def get_homeworks_by_user_id(db: Session, user_id: int, current_user: User):
    # Si el usuario es cliente y está intentando acceder a las tareas de otro usuario
    if current_user.role == RoleEnum.cliente and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver las tareas de otros usuarios")

    homeworks = repository.get_homeworks_by_user_id(db=db, user_id=user_id)
    updated = False

    for hw in homeworks:
        if hw.due_date.tzinfo is None:
            hw.due_date = hw.due_date.replace(tzinfo=timezone.utc)

        # Marcar como atrasada si la fecha ya pasó y aún está pendiente
        if hw.status == HomeworkStatusEnum.pendiente and hw.due_date < datetime.now(timezone.utc):
            hw.status = HomeworkStatusEnum.atrasada
            updated = True

    if updated:
        db.commit()
        for hw in homeworks:
            db.refresh(hw)

    return homeworks

def get_homework_by_id(db: Session, homework_id: int, current_user: User):
    homework = repository.get_homework_by_id(db=db, homework_id=homework_id)

    if not homework:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Solo el admin o el dueño de la tarea puede verla
    if current_user.role == RoleEnum.cliente and homework.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta tarea")

    # Asegurarse de que homework.due_date es "aware"
    if homework.due_date.tzinfo is None:
        homework.due_date = homework.due_date.replace(tzinfo=timezone.utc)

    # Marcar como atrasada si corresponde
    if homework.status == HomeworkStatusEnum.pendiente and homework.due_date < datetime.now(timezone.utc):
        homework.status = HomeworkStatusEnum.atrasada
        db.commit()
        db.refresh(homework)

    return homework

def update_homework(db: Session, updated_homework: HomeworkUpdate, current_user: User):
    homework = repository.get_homework_by_id(db, updated_homework.id)

    if not homework:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Si es cliente, solo puede editar sus propias tareas
    if current_user.role == RoleEnum.cliente and homework.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta tarea")

    return repository.update_homework(db=db, homework=homework, updated_data=updated_homework)

def delete_homework(db: Session, homework_id: int, current_user: User):
    homework = repository.get_homework_by_id(db=db, homework_id=homework_id)

    if not homework:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if current_user.role == RoleEnum.cliente and homework.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta tarea")

    return repository.delete_homework(db=db, homework=homework)
