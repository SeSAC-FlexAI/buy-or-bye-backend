from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.init_db import get_db
from app.api.deps import get_current_user
from app.schemas.account import AccountCreate, AccountOut, AccountFormOut, AccountUpdate
from app.repositories import account_repo
from app.services import account_service

router = APIRouter(tags=["account"])

# 생성
@router.post("", response_model=AccountOut)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    row = account_repo.create_account(db, user.id, payload)
    return row

# 월 목록(달력/일별 리스트)
@router.get("/month", response_model=List[AccountOut])
def list_month(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return account_repo.list_month(db, user.id, year, month)

# 편집 폼 조회 (연필 아이콘 클릭 시)
@router.get("/{account_id}", response_model=AccountFormOut)
def get_account_for_edit(
    account_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    res = account_service.get_form(db, user.id, account_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return res

# 수정 저장
@router.put("/{account_id}", response_model=AccountFormOut)
def update_account(
    account_id: int,
    payload: AccountUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    try:
        res = account_service.update(db, user.id, account_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return res
