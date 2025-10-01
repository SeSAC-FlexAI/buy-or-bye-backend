from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class FSDSetting(Base):
    __tablename__ = "fsd_setting"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    goal_name = Column(String(100), nullable=True)
    target_amount = Column(Float, nullable=True)   # 목표 금액
    target_date = Column(Date, nullable=True)      # 목표 달성일
    monthly_saving = Column(Float, nullable=True)  # 월 저축 목표

    user = relationship("User", back_populates="fsd_setting")
