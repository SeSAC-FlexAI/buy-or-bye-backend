from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class ErrorReport(Base):
    __tablename__ = "error_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),  # 하드 딜리트 연쇄 삭제
        nullable=False,
        index=True,
    )
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ 반대편과 정확히 매칭 — backref 쓰지 말고 back_populates로
    user = relationship("User", back_populates="error_reports")
