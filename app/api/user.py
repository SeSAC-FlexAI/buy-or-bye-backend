from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import register_user
from app.repositories.user_repo import UserRepository

router = APIRouter()

@router.post("/", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, payload)
    return user

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return UserRepository(db).list()


