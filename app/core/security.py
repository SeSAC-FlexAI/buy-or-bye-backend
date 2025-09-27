# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],  # bcrypt_sha256 우선, bcrypt 레거시 호환
    deprecated="auto",
)

def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: Dict[str, Any] = {"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(plain, hashed)
    except ValueError:
        # bcrypt 72바이트 등 예외는 False로 처리해 401로 매핑
        return False

def get_password_hash(plain: str) -> str:
    return pwd_context.hash(plain)

def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except (ExpiredSignatureError, JWTError):
        raise
