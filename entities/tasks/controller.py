from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import TaskCreate, TaskUpdate
from entities.users.models import User
from entities.homeworks.models import Homework
from . import repository
from .models import Task

def create_task(db: Session, task_data: TaskCreate, current_user: User):
    homework = db.query(Homework).filter_by(id=task_data.homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="La tarea no está asociada a ninguna homework válida")

    # Verificamos permisos
    if current_user.role == "cliente" and homework.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para agregar tareas a esta homework")

    return repository.create_task(db=db, task_data=task_data)

def get_tasks_by_homework_id(db: Session, homework_id: int, current_user: User):
    homework = db.query(Homework).filter_by(id=homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Homework no encontrada")

    if current_user.role == "cliente" and homework.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a las tareas de esta homework")

    return repository.get_tasks_by_homework_id(db=db, homework_id=homework_id)

def get_task_by_id(db: Session, task_id: int, current_user: User):
    task = repository.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Validar acceso según el usuario
    if current_user.role == "cliente":
        if not task.homework or task.homework.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes acceso a esta tarea")

    return task

def update_task(db: Session, task_data: TaskUpdate, current_user: User):
    task = db.query(Task).filter_by(id=task_data.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Verificar si el usuario tiene permiso para editar la tarea (basado en la homework asociada)
    homework = db.query(Homework).filter_by(id=task.homework_id).first()
    if current_user.role == "cliente" and homework.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta tarea")

    return repository.update_task(db=db, task_data=task_data, task=task)

def delete_task(db: Session, task_id: int, current_user: User):
    task = db.query(Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Verificar si el usuario tiene permiso para eliminar la tarea
    homework = db.query(Homework).filter_by(id=task.homework_id).first()
    if current_user.role == "cliente" and homework.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta tarea")
    
    return repository.delete_task(db=db, task=task)
