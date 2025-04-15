from sqlalchemy.orm import Session
from .models import Homework
from .schemas import HomeworkCreate, HomeworkUpdate

def create_homework(db: Session, homework_data: HomeworkCreate):
    # Crear nueva tarea
    new_homework = Homework(
        title=homework_data.title,
        description=homework_data.description,
        due_date=homework_data.due_date,
        user_id=homework_data.user_id
    )
    
    db.add(new_homework)
    db.flush()  # Hacemos flush para asegurarnos de que se genere el ID antes de hacer commit
    db.commit()
    db.refresh(new_homework)
    return new_homework

def get_homeworks_by_user_id(db: Session, user_id: int):
    # Obtener todas las tareas de un usuario por su ID
    return db.query(Homework).filter(Homework.user_id == user_id).all()

def get_homework_by_id(db: Session, homework_id: int):
    # Obtener una tarea específica por ID
    return db.query(Homework).filter(Homework.id == homework_id).first()

def update_homework(db: Session, homework: Homework, updated_data: HomeworkUpdate):
    # Actualizar la tarea con los nuevos datos
    if updated_data.title is not None:
        homework.title = updated_data.title
    if updated_data.description is not None:
        homework.description = updated_data.description
    if updated_data.due_date is not None:
        homework.due_date = updated_data.due_date

    db.commit()  # Hacemos commit para aplicar los cambios
    db.refresh(homework)  # Refresca el objeto con los datos de la base de datos
    return homework

def delete_homework(db: Session, homework: Homework):
    # Eliminar una tarea
    db.delete(homework)
    db.commit()
    return {"detail": "Tarea eliminada correctamente"}
