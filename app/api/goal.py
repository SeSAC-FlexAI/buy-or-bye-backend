from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Literal

from app.api.deps import get_db, get_current_user
from app.schemas.goal import GoalCreate, GoalUpdate, GoalOut
from app.services import goal_service
from app.models.user import User

router = APIRouter(prefix="/api/goal", tags=["goal"])

GoalType = Literal["ASSET", "INCOME", "EXPENSE"]
Period = Literal["MONTHLY", "YEARLY"]

@router.get("/me", response_model=list[GoalOut], summary="(대시보드) 스코프별 목표 리스트")
def list_my_goals(
    goal_type: GoalType = Query(..., description="ASSET/INCOME/EXPENSE"),
    period: Period = Query(..., description="MONTHLY/YEARLY"),
    year: int = Query(..., description="연도"),
    month: Optional[int] = Query(None, description="월( MONTHLY일 때 필수 / YEARLY일 때 None )"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return goal_service.list_scope(db, current_user.id, goal_type, period, year, month)

@router.post("/me", response_model=GoalOut, summary="목표 업서트(동일 스코프가 있으면 금액 갱신)")
def upsert_my_goal(
    payload: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return goal_service.upsert_goal(db, current_user.id, payload)

@router.put("/{goal_id}", response_model=GoalOut, summary="목표 금액 수정(단일)")
def update_my_goal_amount(
    goal_id: int,
    payload: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = goal_service.update_goal_amount(db, goal_id, payload)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return row

@router.delete("/me", summary="목표 삭제(정확한 스코프 지정)")
def delete_my_goal(
    goal_type: GoalType = Query(..., description="ASSET/INCOME/EXPENSE"),
    period: Period = Query(..., description="MONTHLY/YEARLY"),
    year: int = Query(..., description="연도"),
    month: Optional[int] = Query(None, description="월"),
    category: Optional[str] = Query(None, description="카테고리(ASSET이면 None)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = goal_service.delete_goal(db, current_user.id, goal_type, period, year, month, category)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return {"success": True}
