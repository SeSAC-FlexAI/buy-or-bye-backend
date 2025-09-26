from sqlalchemy.orm import Session
from app.db.base import Base, engine
from app.models.user import User
from app.core.security import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    with Session(bind=engine, future=True) as db:
        if not db.query(User).filter(User.email == "admin@example.com").first():
            admin = User(email="admin@example.com", nickname="admin", hashed_password=get_password_hash("admin1234"))
            db.add(admin)
            db.commit()

if __name__ == "__main__":
    init_db()
