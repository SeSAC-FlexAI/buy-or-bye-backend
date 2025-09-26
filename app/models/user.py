from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    fpti_list = relationship("FPTI", back_populates="user", cascade="all, delete-orphan")