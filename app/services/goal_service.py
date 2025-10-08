from sqlalchemy.orm import Session
from app.repositories.goal_repo import GoalRepository
from app.schemas.goal import GoalCreate, GoalUpdate

def list_scope(db: Session, user_id: int, goal_type: str, period: str, year: int, month: int | None):
    return GoalRepository(db).list_scope(user_id, goal_type, period, year, month)

def upsert_goal(db: Session, user_id: int, payload: GoalCreate):
    return GoalRepository(db).upsert(user_id, payload)

def update_goal_amount(db: Session, goal_id: int, payload: GoalUpdate):
    return GoalRepository(db).update_amount(goal_id, payload)

def delete_goal(db: Session, user_id: int, goal_type: str, period: str, year: int, month: int | None, category: str | None) -> bool:
    return GoalRepository(db).delete_one(user_id, goal_type, period, year, month, category)
