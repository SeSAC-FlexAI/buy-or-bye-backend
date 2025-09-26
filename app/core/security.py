# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    # timezone-aware 추천
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: Dict[str, Any] = {
        "sub": subject,                # user.id 또는 email (문자열 권장)
        "iat": int(now.timestamp()),   # 발급시각 (옵션)
        "exp": int(exp.timestamp()),   # 만료시각
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(plain: str) -> str:
    return pwd_context.hash(plain)

# ⬇⬇⬇ 추가: 토큰 검증(디코드)
def decode_token(token: str) -> Dict[str, Any]:
    """
    유효한 토큰이면 payload(dict)를 반환, 아니면 예외 발생
    - ExpiredSignatureError: 만료
    - JWTError: 서명 불일치/형식 오류
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise
    except JWTError:
        raise
