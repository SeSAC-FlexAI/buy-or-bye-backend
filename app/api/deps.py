from typing import Generator
from fastapi import Security, HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.core.config import settings
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.security import decode_token
from app.db.init_db import get_db
from app.models.user import User
from typing import Optional

security = HTTPBearer(auto_error=True)
security_optional = HTTPBearer(auto_error=False)

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

def get_current_user(
    creds: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
) -> User:
    token = creds.credentials
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")

    # subject를 user.id로 넣었다면 int 변환
    user = db.query(User).filter(User.id == int(sub)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def get_current_user_optional(
    creds: Optional[HTTPAuthorizationCredentials] = Security(security_optional),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if not creds:
        return None
    try:
        payload = decode_token(creds.credentials)
        sub = payload.get("sub")
        if not sub:
            return None
        return db.query(User).filter(User.id == int(sub)).first()
    except Exception:
        return None