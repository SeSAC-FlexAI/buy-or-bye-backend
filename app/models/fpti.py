# app/models/fpti.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class FPTI(Base):
    __tablename__ = "fpti"

    id = Column(Integer, primary_key=True, index=True)
    # 게스트 허용 → user_id nullable
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    # 프런트 공유/조회용 키 (UUID 문자열 권장)
    post_id = Column(String(64), unique=True, nullable=False, index=True)

    title = Column(String(100), nullable=True)
    # 설문 응답/중간계산/최종결과를 저장할 수 있게 JSON string(Text)
    answers_json = Column(Text, nullable=True)
    result_json = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="fpti_list")