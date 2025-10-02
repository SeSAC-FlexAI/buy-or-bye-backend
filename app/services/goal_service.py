# app/services/goal_service.py
from sqlalchemy.orm import Session
from typing import Optional, List
from app.repositories import goal_repo
from app.schemas.goal import GoalCreate, GoalUpdate

def list_goals(db: Session, user_id: int, **filters):
    return goal_repo.list_goals(db, user_id, **filters)

def upsert(db: Session, user_id: int, payload: GoalCreate | GoalUpdate):
    return goal_repo.upsert(db, user_id, payload)

def delete(db: Session, user_id: int, **key) -> bool:
    return goal_repo.delete_one(db, user_id, **key)
