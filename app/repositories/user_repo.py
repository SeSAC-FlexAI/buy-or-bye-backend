from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException, status

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def list(self) -> list[User]:
        return self.db.query(User).all()

    def create(self, email: str, nickname: str, hashed_password: str) -> User:
        obj = User(email=email, nickname=nickname, hashed_password=hashed_password)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def is_email_taken(self, email: str) -> bool:
        return self.db.query(User.id).filter(User.email == email).first() is not None

    def update_password(self, user_id: int, new_hashed: str) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None
        user.hashed_password = new_hashed
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def hard_delete_by_id(self, user_id: int) -> None:
        user = self.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.db.delete(user)      # ★ 자식은 CASCADE로 자동 삭제
        self.db.commit()