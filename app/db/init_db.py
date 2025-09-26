# app/db/init_db.py
from sqlalchemy.orm import Session, sessionmaker
from app.db.base import Base, engine
from app.models.user import User
from app.core.security import get_password_hash

# 1) 의존성으로 사용할 세션 팩토리
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

# 2) FastAPI Depends 용 DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3) 최초 테이블 생성 + 시드(admin) (개발용)
def init_db():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if not db.query(User).filter(User.email == "admin@example.com").first():
            admin = User(
                email="admin@example.com",
                nickname="admin",
                hashed_password=get_password_hash("admin1234"),
            )
            db.add(admin)
            db.commit()

if __name__ == "__main__":
    init_db()
