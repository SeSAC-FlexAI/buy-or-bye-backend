from sqlalchemy.orm import Session
from app.models.account import AccountBook
from app.schemas.account import AccountCreate, AccountUpdate

def create_account(db: Session, user_id: int, data: AccountCreate):
    account = AccountBook(user_id=user_id, **data.dict())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_accounts(db: Session, user_id: int):
    return db.query(AccountBook).filter(AccountBook.user_id == user_id).all()

def get_account_by_id(db: Session, account_id: int):
    return db.query(AccountBook).filter(AccountBook.id == account_id).first()

def update_account(db: Session, account: AccountBook, data: AccountUpdate):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account

def delete_account(db: Session, account: AccountBook):
    db.delete(account)
    db.commit()
