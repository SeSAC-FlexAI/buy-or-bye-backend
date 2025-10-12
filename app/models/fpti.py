# app/models/fpti.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.db.base import Base

class FPTI(Base):
    __tablename__ = "fpti"

    id = Column(Integer, primary_key=True, index=True)
    # ★ 추가: 외부 공유/조회용 식별자
    post_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid4()))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    # 화면에 저장하는 필드들(네가 원하는 구조 유지)
    title = Column(String(255), nullable=True)
    type_code = Column(String(16), nullable=True)
    type_alias = Column(String(255), nullable=True)
    type_name_en = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    who_text = Column(String(255), nullable=True)
    when_text = Column(String(255), nullable=True)
    what_text = Column(String(255), nullable=True)
    how_text = Column(String(255), nullable=True)

    # 점수/원시결과
    scores = Column(JSON, nullable=True)   # {"who_score":..., ...}
    answers = Column(Text, nullable=True)  # 프론트 설명 문자열 저장
    result = Column(JSON, nullable=True)   # 전체 결과 JSON(옵션)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="fpti_list")
