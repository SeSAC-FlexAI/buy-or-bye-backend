from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password, create_access_token
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.schemas.user_extra import UserEmailOut, PasswordChangeIn, EmailCheckOut
from app.models.user import User

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

def get_email_by_user_id(db: Session, user_id: int) -> Optional[UserEmailOut]:
    repo = UserRepository(db)
    u = repo.get(user_id)
    if not u:
        return None
    return UserEmailOut(user_id=u.id, email=u.email)

def check_email_available(db: Session, email: str) -> EmailCheckOut:
    repo = UserRepository(db)
    # 이메일은 소문자/trim 정규화 권장
    norm = email.strip().lower()
    return EmailCheckOut(email=norm, available=not repo.is_email_taken(norm))

def change_password(db: Session, user_id: int, payload: PasswordChangeIn) -> bool:
    repo = UserRepository(db)
    u = repo.get(user_id)
    if not u:
        return False
    # 현재 비번 확인
    if not verify_password(payload.current_password, u.hashed_password):
        return False
    # 동일 비번 방지
    if payload.current_password == payload.new_password:
        return False
    # 해시 후 저장
    new_hashed = get_password_hash(payload.new_password)
    updated = repo.update_password(user_id, new_hashed)
    return updated is not None

def delete_me(db: Session, current_user: User) -> None:
    UserRepository(db).hard_delete_by_id(current_user.id)

def admin_delete_user(db: Session, target_user_id: int) -> None:
    UserRepository(db).hard_delete_by_id(target_user_id)