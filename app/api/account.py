from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.init_db import get_db
from app.schemas.account import AccountCreate, AccountUpdate, AccountOut
from app.services import account_service
from app.api.deps import get_current_user  # 로그인 필요시

router = APIRouter()

@router.post("/", response_model=AccountOut)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),  # ✅ 쿼리 파라미터 대신 Depends
):
    return account_service.create_account(db, current_user.id, payload)

@router.get("/", response_model=List[AccountOut])
def read_accounts(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return account_service.get_accounts(db, user.id)

@router.get("/{account_id}", response_model=AccountOut)
def read_account(account_id: int, db: Session = Depends(get_db)):
    account = account_service.get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, data: AccountUpdate, db: Session = Depends(get_db)):
    updated = account_service.update_account(db, account_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated

@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    ok = account_service.delete_account(db, account_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"detail": "Account deleted successfully"}
