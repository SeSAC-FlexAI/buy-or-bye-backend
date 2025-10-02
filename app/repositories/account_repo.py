from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, literal
from app.models.account import AccountBook
from app.schemas.account import AccountCreate

# 생성: 수입=+, 지출=-
def create_account(db: Session, user_id: int, payload: AccountCreate) -> AccountBook:
    signed_amount = payload.amount if payload.io_type == "income" else -payload.amount
    row = AccountBook(
        user_id=user_id,
        date=payload.date,
        category=payload.category,
        description=payload.description,
        amount=signed_amount,
        method=payload.method,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

# 월 목록 (대출 제외)
def list_month(db: Session, user_id: int, year: int, month: int) -> List[AccountBook]:
    return (
        db.query(AccountBook)
        .filter(
            AccountBook.user_id == user_id,
            func.strftime('%Y', AccountBook.date) == literal(f"{year:04d}"),
            func.strftime('%m', AccountBook.date) == literal(f"{month:02d}"),
        )
        .order_by(AccountBook.date.asc(), AccountBook.id.asc())
        .all()
    )

# 단건 조회 (소유권 체크)
def get_by_id(db: Session, user_id: int, account_id: int) -> Optional[AccountBook]:
    return (
        db.query(AccountBook)
        .filter(AccountBook.id == account_id, AccountBook.user_id == user_id)
        .first()
    )

# 수정 (부분 업데이트)
def update_account(
    db: Session,
    row: AccountBook,
    *,
    amount_signed: Optional[float] = None,
    category: Optional[str] = None,
    date=None,
    description: Optional[str] = None,
    method: Optional[str] = None,
) -> AccountBook:
    if amount_signed is not None:
        row.amount = amount_signed
    if category is not None:
        row.category = category
    if date is not None:
        row.date = date
    if description is not None:
        row.description = description
    if method is not None:
        row.method = method
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

#삭제 
def delete_by_id(db: Session, user_id: int, account_id: int) -> bool:
    row = (
        db.query(AccountBook)
        .filter(AccountBook.id == account_id, AccountBook.user_id == user_id)
        .first()
    )
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True
