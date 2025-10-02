# app/api/goal.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.init_db import get_db
from app.api.deps import get_current_user
from app.schemas.goal import GoalCreate, GoalUpdate, GoalOut
from app.services import goal_service

router = APIRouter()

@router.get("/me", response_model=List[GoalOut])
def get_my_goals(
    goal_type: Optional[str] = Query(None),
    period: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return goal_service.list_goals(
        db, user.id,
        goal_type=goal_type, period=period, year=year, month=month, category=category
    )

@router.post("/me", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def create_or_update_goal_for_me(
    payload: GoalCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return goal_service.upsert(db, user.id, payload)

@router.put("/me", response_model=GoalOut)
def update_goal_for_me(
    payload: GoalUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return goal_service.upsert(db, user.id, payload)

@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_goal_for_me(
    goal_type: str = Query(...),
    period: str = Query(...),
    year: int = Query(...),
    month: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    ok = goal_service.delete(db, user.id,
        goal_type=goal_type, period=period, year=year, month=month, category=category
    )
    if not ok:
        raise HTTPException(status_code=404, detail="goal not found")
    return {"success": True}
