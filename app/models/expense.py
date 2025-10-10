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

    total_expense = Column(Integer, nullable=False, server_default="0")
    food = Column(Integer, nullable=False, server_default="0")
    shopping = Column(Integer, nullable=False, server_default="0")
    transportation = Column(Integer, nullable=False, server_default="0")
    housing_maintenance = Column(Integer, nullable=False, server_default="0")
    culture_leisure = Column(Integer, nullable=False, server_default="0")
    household_goods = Column(Integer, nullable=False, server_default="0")  # 기존 cosmetics → household_goods
    other = Column(Integer, nullable=False, server_default="0")

    loans = Column(Integer, nullable=False, server_default="0")
    investment_expense = Column(Integer, nullable=False, server_default="0")
    card_payment_withdrawal = Column(Integer, nullable=False, server_default="0")

    user = relationship("User", back_populates="expenses")  # ✅ User.expenses와 교차 일치
    