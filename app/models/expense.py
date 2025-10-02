# app/models/expense.py
from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Expense(Base):
    __tablename__ = "expenses"  # ✅ 복수형

    __table_args__ = (UniqueConstraint("user_id", name="uq_expenses_user"),)  # ✅ 유저당 1건 보장

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)

    total_expense = Column(Integer, nullable=False)
    food = Column(Integer, default=0)
    shopping = Column(Integer, default=0)
    transportation = Column(Integer, default=0)
    housing_maintenance = Column(Integer, default=0)
    culture_leisure = Column(Integer, default=0)
    household_goods = Column(Integer, default=0)  # 기존 cosmetics → household_goods
    other = Column(Integer, default=0)

    user = relationship("User", back_populates="expenses")  # ✅ User.expenses와 교차 일치
    