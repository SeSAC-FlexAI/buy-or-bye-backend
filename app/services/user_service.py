from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password, create_access_token
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate

def register_user(db: Session, payload: UserCreate):
    repo = UserRepository(db)
    if repo.get_by_email(payload.email):
        raise ValueError("Email already registered")
    user = repo.create(
        email=payload.email,
        nickname=payload.nickname,
        hashed_password=get_password_hash(payload.password)
    )
    return user

def authenticate(db: Session, email: str, password: str) -> str | None:
    repo = UserRepository(db)
    user = repo.get_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return create_access_token(subject=str(user.id))
