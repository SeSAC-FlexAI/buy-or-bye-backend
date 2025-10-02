# app/models/income.py
from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Income(Base):
    __tablename__ = "incomes"  # ✅ 복수형으로 변경

    __table_args__ = (UniqueConstraint("user_id", name="uq_incomes_user"),)  # ✅ 유저당 1건 보장

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)

    total_income = Column(Integer, nullable=False)
    salary = Column(Integer, default=0)
    investment_income = Column(Integer, default=0)
    side_income = Column(Integer, default=0)

    user = relationship("User", back_populates="incomes")  # ✅ User.incomes 와 교차 일치
