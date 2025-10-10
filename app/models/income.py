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

    # ←↓↓ 기본값과 NOT NULL을 명시 (server_default는 마이그레이션 시에만 반영됨)
    total_income = Column(Integer, nullable=False, server_default="0")
    salary = Column(Integer, nullable=False, server_default="0")
    investment_income = Column(Integer, nullable=False, server_default="0")
    side_income = Column(Integer, nullable=False, server_default="0")
    pin_money = Column(Integer, nullable=False, server_default="0")
    loans = Column(Integer, nullable=False, server_default="0")

    user = relationship("User", back_populates="incomes")  # ✅ User.incomes 와 교차 일치
