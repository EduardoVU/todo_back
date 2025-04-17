from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .repository import create_session, get_active_session
from .schemas import SessionCreate, SessionOut
from config import SECRET_KEY, ALGORITHM

def create_new_session(db: Session, session: SessionCreate, user_id: int):
    # Crear una nueva sesión, eliminando la anterior si ya existe
    new_session = create_session(db, user_id, session.token, session.expires_at)
    if not new_session:
        raise HTTPException(status_code=400, detail="Error al crear la sesión.")
    return SessionOut.model_validate(new_session)

def verify_code_controller(request, token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido")

    session = get_active_session(db, user_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    if session.code != request.code:
        raise HTTPException(status_code=401, detail="Código incorrecto")

    session.verified = True
    db.commit()

    return {"message": "Código verificado correctamente", "success": True}