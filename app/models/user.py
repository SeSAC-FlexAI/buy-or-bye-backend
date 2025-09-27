from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # ✅ ChatbotSetting.user(back_populates="chatbot_setting") 와 1:1 매칭
    chatbot_setting  = relationship(
        "ChatbotSetting",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # ✅ ChatbotMessage.user(back_populates="chatbot_messages") 와 1:N 매칭
    chatbot_messages = relationship(
        "ChatbotMessage",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    fpti_list = relationship("FPTI", back_populates="user", cascade="all, delete-orphan")
    fpa_list = relationship("FPA", back_populates="user", cascade="all, delete-orphan")
    fsd_setting = relationship("FSDSetting", back_populates="user", uselist=False, cascade="all, delete-orphan")
    pattern_setting = relationship("PatternSetting", back_populates="user", uselist=False, cascade="all, delete-orphan")