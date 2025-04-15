from sqlalchemy.orm import Session
from .models import Task, TaskStatusEnum
from .schemas import TaskCreate, TaskUpdate

def create_task(db: Session, task_data: TaskCreate):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        status=TaskStatusEnum.pendiente,
        homework_id=task_data.homework_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks_by_homework_id(db: Session, homework_id: int):
    return db.query(Task).filter_by(homework_id=homework_id).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_data: TaskUpdate, task: Task):

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.status is not None:
        task.status = task_data.status
    
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
    return {"detail": "Actividad eliminada correctamente"}