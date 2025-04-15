from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import HomeworkCreate, HomeworkUpdate
from . import controller
from entities.users.models import User
from auth import get_current_user
import database

router = APIRouter()

@router.post("/homeworks")
def create_homework_endpoint(
    homework: HomeworkCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return controller.create_homework(db=db, homework_data=homework, current_user=current_user)

@router.get("/homeworks/user/{user_id}")
def get_homeworks_by_user_id(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return controller.get_homeworks_by_user_id(db=db, user_id=user_id, current_user=current_user)

@router.get("/homeworks/{homework_id}")
def get_homework_by_id(
    homework_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return controller.get_homework_by_id(db=db, homework_id=homework_id, current_user=current_user)

@router.put("/homeworks")
def update_homework(
    updated_homework: HomeworkUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return controller.update_homework(db=db, updated_homework=updated_homework, current_user=current_user)

@router.delete("/homeworks/{homework_id}")
def delete_homework(
    homework_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    print("Entramos al router")
    return controller.delete_homework(db=db, homework_id=homework_id, current_user=current_user)