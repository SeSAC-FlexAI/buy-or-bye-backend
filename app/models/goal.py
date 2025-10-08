from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    goal_type = Column(String(16), nullable=False)   # ASSET / INCOME / EXPENSE
    period    = Column(String(16), nullable=False)   # MONTHLY / YEARLY
    year      = Column(Integer, nullable=False)
    month     = Column(Integer, nullable=True)       # YEARLY면 NULL
    category  = Column(String(64), nullable=True)    # ASSET이면 보통 NULL

    target_amount = Column(Integer, nullable=False)

    # User 모델에 goals 관계가 있다고 가정 (back_populates="goals")
    user = relationship("User", back_populates="goals")

    # 사용자 + 유형 + 기간 + 연/월 + 카테고리 = 유니크
    __table_args__ = (
        UniqueConstraint(
            "user_id", "goal_type", "period", "year", "month", "category",
            name="uq_goals_user_scope"
        ),
    )
