# app/models/goal.py
from sqlalchemy import (
    Column, Integer, ForeignKey, String, Enum, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class GoalType(str, enum.Enum):
    ASSET = "ASSET"
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class Period(str, enum.Enum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

class Goal(Base):
    __tablename__ = "goals"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "goal_type", "period", "year", "month", "category",
            name="uq_goals_user_scope"
        ),
        CheckConstraint("year >= 1900 AND year <= 2100", name="ck_goals_year_range"),
        CheckConstraint("(month IS NULL) OR (month BETWEEN 1 AND 12)", name="ck_goals_month_range"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    goal_type = Column(Enum(GoalType), nullable=False)
    period = Column(Enum(Period), nullable=False)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=True)      # YEARLY일 때는 None

    category = Column(String(50), nullable=True)  # 세부 카테고리 목표 (없으면 전체)

    target_amount = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="goals")
