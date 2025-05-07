from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import controller
from .schemas import TaskCreate, TaskOut, TaskUpdate
from entities.users.models import User
from auth import get_current_user
import database
from typing import List

router = APIRouter()

@router.post("/tasks", response_model=TaskOut)
def create_task_endpoint(
    task: TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return controller.create_task(db=db, task_data=task, current_user=current_user)

@router.get("/tasks/homework/{homework_id}", response_model=List[TaskOut])
def get_tasks_by_homework_id_endpoint(
    homework_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return controller.get_tasks_by_homework_id(db=db, homework_id=homework_id, current_user=current_user)

@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task_by_id_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    return controller.get_task_by_id(db=db, task_id=task_id, current_user=current_user)

@router.put("/tasks", response_model=TaskOut)
def update_task_endpoint(
    task: TaskUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return controller.update_task(db=db, task_data=task, current_user=current_user)

@router.delete("/tasks/{task_id}", response_model=None)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return controller.delete_task(db=db, task_id=task_id, current_user=current_user)



