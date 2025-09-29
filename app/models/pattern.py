from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class PatternSetting(Base):
    """
    사용자별 소비패턴 설정:
    - monthly_budget: 월 예산(선택)
    - rules_json: {"스타벅스": "카페", "GS25": "편의점", "지하철": "교통"} 같은 키워드→카테고리 매핑
    """
    __tablename__ = "pattern_setting"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)

    monthly_budget = Column(Float, nullable=True)
    rules_json = Column(Text, nullable=True)

    user = relationship("User", back_populates="pattern_setting")
