from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .models import Session
from sqlalchemy.exc import SQLAlchemyError

# Obtener una sesión activa
def get_active_session(db: Session, user_id: int):
    return db.query(Session).filter(
        Session.user_id == user_id,
        Session.expires_at > datetime.now(timezone.utc)
    ).first()

# Eliminar una sesión activa
def delete_session(db: Session, session_id: int):
    session_to_delete = db.query(Session).filter(Session.id == session_id).first()
    if session_to_delete:
        db.delete(session_to_delete)
        db.commit()

# Crear una nueva sesión, eliminando primero la anterior si existe
def create_session(db: Session, user_id: int, code: str, expires_at: datetime):
    active_session = get_active_session(db, user_id)
    if active_session:
        delete_session(db, active_session.id)  # Eliminar la sesión activa anterior

    new_session = Session(user_id=user_id, code=code, expires_at=expires_at)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session
