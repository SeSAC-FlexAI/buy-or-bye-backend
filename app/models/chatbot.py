from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class ChatbotSetting(Base):
    __tablename__ = "chatbot_setting"  # ← 기존 테이블명 유지 (마이그레이션 피함)

    id = Column(Integer, primary_key=True, index=True)
    # ✅ 1:1 보장: unique=True
    # ✅ 하드 딜리트 연쇄 삭제: ondelete="CASCADE"
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    system_prompt = Column(Text, nullable=True)
    temperature   = Column(Float, nullable=True)   # 0~2 권장범위
    top_p         = Column(Float, nullable=True)   # 0~1

    # ✅ User.chatbot_setting (단수)와 정확히 매칭
    user = relationship("User", back_populates="chatbot_setting")


class ChatbotMessage(Base):
    __tablename__ = "chatbot_message"  # ← 기존 테이블명 유지

    id = Column(Integer, primary_key=True, index=True)
    # 게스트 허용 → user_id nullable
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # 프런트 공유/조회용 식별자
    message_id = Column(String(64), unique=True, nullable=False, index=True)

    question  = Column(Text, nullable=False)
    answer    = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ User.chatbot_messages (복수)와 정확히 매칭
    user = relationship("User", back_populates="chatbot_messages")
