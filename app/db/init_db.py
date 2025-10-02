# app/db/init_db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.base import Base
from app.core.security import get_password_hash
from app.models.user import User

# ⬇⬇⬇ 추가
import sqlite3
from sqlalchemy import event

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./project.db")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
engine = create_engine(DB_URL, echo=False, future=True, connect_args=connect_args)

# ⬇⬇⬇ 추가: SQLite일 때 PRAGMA 활성화
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    # sqlite3.Connection 인스턴스일 때만 적용
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

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
