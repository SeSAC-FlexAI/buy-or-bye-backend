from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User

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