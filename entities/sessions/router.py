from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from .controller import verify_code_controller
from .schemas import VerifyCodeRequest 
from auth import oauth2_scheme

router = APIRouter()

@router.post("/auth")
def verify_code(request: VerifyCodeRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return verify_code_controller(request, token, db)

