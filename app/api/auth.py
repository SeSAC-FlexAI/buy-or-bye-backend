from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(subject=str(user.id), expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": token, "token_type": "bearer"}
