from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate

class GoalRepository:
    def __init__(self, db: Session):
        self.db = db

    def _match_month(self, month):
        # SQLAlchemy에서 None 비교를 위해 is_ / == 분기
        if month is None:
            return Goal.month.is_(None)
        return Goal.month == month

    def _match_category(self, category):
        if category is None:
            return Goal.category.is_(None)
        return Goal.category == category

    def get_one(self, user_id: int, goal_type: str, period: str, year: int, month: int | None, category: str | None) -> Goal | None:
        stmt = (
            select(Goal)
            .where(
                Goal.user_id == user_id,
                Goal.goal_type == goal_type,
                Goal.period == period,
                Goal.year == year,
                self._match_month(month),
                self._match_category(category),
            )
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_scope(self, user_id: int, goal_type: str, period: str, year: int, month: int | None) -> list[Goal]:
        stmt = (
            select(Goal)
            .where(
                Goal.user_id == user_id,
                Goal.goal_type == goal_type,
                Goal.period == period,
                Goal.year == year,
                self._match_month(month),
            )
            .order_by(Goal.category.is_(None), Goal.category.asc())  # None이 마지막으로 가게 조정
        )
        return list(self.db.execute(stmt).scalars().all())

    def upsert(self, user_id: int, payload: GoalCreate) -> Goal:
        row = self.get_one(
            user_id=user_id,
            goal_type=payload.goal_type,
            period=payload.period,
            year=payload.year,
            month=payload.month,
            category=payload.category,
        )
        if row:
            row.target_amount = payload.target_amount
            self.db.add(row)
        else:
            row = Goal(
                user_id=user_id,
                goal_type=payload.goal_type,
                period=payload.period,
                year=payload.year,
                month=payload.month,
                category=payload.category,
                target_amount=payload.target_amount,
            )
            self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update_amount(self, goal_id: int, payload: GoalUpdate) -> Goal | None:
        row = self.db.get(Goal, goal_id)
        if not row:
            return None
        if payload.target_amount is not None:
            row.target_amount = payload.target_amount
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def delete_one(self, user_id: int, goal_type: str, period: str, year: int, month: int | None, category: str | None) -> bool:
        row = self.get_one(user_id, goal_type, period, year, month, category)
        if not row:
            return False
        self.db.delete(row)
        self.db.commit()
        return True
