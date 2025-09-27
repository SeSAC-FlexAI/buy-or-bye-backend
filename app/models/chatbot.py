from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class ChatbotSetting(Base):
    __tablename__ = "chatbot_setting"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)

    system_prompt = Column(Text, nullable=True)
    temperature   = Column(Float, nullable=True)   # 0~2 권장범위
    top_p         = Column(Float, nullable=True)   # 0~1

    user = relationship("User", back_populates="chatbot_setting")


class ChatbotMessage(Base):
    __tablename__ = "chatbot_message"

    id = Column(Integer, primary_key=True, index=True)
    # 게스트 허용 → user_id nullable
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    # 프런트 공유/조회용 식별자
    message_id = Column(String(64), unique=True, nullable=False, index=True)

    question  = Column(Text, nullable=False)
    answer    = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chatbot_messages")
