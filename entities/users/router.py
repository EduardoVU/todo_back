from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .schemas import UserCreate
from . import schemas, controller
from .models import User
from auth import SECRET_KEY, ALGORITHM, get_current_user
from entities.sessions.repository import get_active_session
import database


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post("/users")
def create_user(user_create: UserCreate, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return controller.create_user(db, user_create, current_user)

@router.get("/users")
def get_all_user_endpoint(db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return controller.get_all_users(db=db, current_user=current_user)

@router.get("/users/{user_id}")
def get_user_by_id_endpoint(user_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return controller.get_by_id_users(db=db, user_id=user_id, current_user=current_user)

@router.put("/users")
def edit_user_endpoint(user: schemas.UserUpdate, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return controller.update_user(db=db, user=user, current_user=current_user)

@router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return controller.delete_user(db=db, user_id=user_id, current_user=current_user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return controller.login_user(form_data, db)

@router.post("/logout")
def logout(db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return controller.logout_user(db=db, current_user=current_user)

