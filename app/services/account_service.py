# app/services/account_service.py
from sqlalchemy.orm import Session
from app.repositories import account_repo
from app.schemas.account import AccountCreate, AccountUpdate

def create_account(db: Session, user_id: int, payload: AccountCreate):
    return account_repo.create_account(db, user_id, payload)

def get_accounts(db: Session, user_id: int):
    return account_repo.get_accounts(db, user_id)

def get_account_by_id(db: Session, account_id: int):
    return account_repo.get_account_by_id(db, account_id)

def update_account(db: Session, account_id: int, data: AccountUpdate):
    account = account_repo.get_account_by_id(db, account_id)
    if not account:
        return None
    return account_repo.update_account(db, account, data)

def delete_account(db: Session, account_id: int):
    account = account_repo.get_account_by_id(db, account_id)
    if not account:
        return None
    account_repo.delete_account(db, account)
    return True
