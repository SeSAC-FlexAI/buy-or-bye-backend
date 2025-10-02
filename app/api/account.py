# app/api/account.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.account import AccountCreate, AccountFormOut, AccountUpdate, AccountOut
from app.services import account_service
from app.repositories import account_repo

router = APIRouter()


@router.post("", response_model=AccountFormOut, status_code=status.HTTP_201_CREATED)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    가계부 행 생성(대시보드 스냅샷 자동 반영).
    편집폼 형태로 반환.
    """
    return account_service.create(db, user.id, payload)


@router.get("/{account_id}/form", response_model=AccountFormOut)
def get_account_form(
    account_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    편집폼 전용 단건 조회(양수/음수 → 수입/지출로 변환하여 amount는 절대값으로 반환)
    """
    form = account_service.get_form(db, user.id, account_id)
    if not form:
        raise HTTPException(status_code=404, detail="Account not found")
    return form


@router.put("/{account_id}", response_model=AccountFormOut)
def update_account(
    account_id: int,
    payload: AccountUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    가계부 수정(이전 델타 역적용 → 신규 델타 적용).
    편집폼 형태로 반환.
    """
    form = account_service.update(db, user.id, account_id, payload)
    if not form:
        raise HTTPException(status_code=404, detail="Account not found")
    return form


@router.delete("/{account_id}", status_code=status.HTTP_200_OK)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    가계부 삭제(삭제 전 델타 역적용).
    JSON을 원하면 {"success": True} 반환.
    """
    ok = account_service.delete(db, user.id, account_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"success": True}


# (선택) 월별 리스트: 대출 제외 없이 모두 반환
@router.get("/month", response_model=List[AccountOut])
def list_month(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    월별 가계부 목록 (대출 포함, 정렬: 날짜/ID 오름차순)
    """
    return account_repo.list_month(db, user.id, year, month)
