from typing import Generator
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.core.config import settings
from app.repositories.user_repo import UserRepository

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(token: str | None = None, authorization: str | None = None) -> int:
    # 허용: Authorization: Bearer <token> 또는 쿼리/폼의 token
    raw = None
    if authorization and authorization.startswith("Bearer "):
        raw = authorization.split(" ")[1]
    elif token:
        raw = token
    if not raw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(raw, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
