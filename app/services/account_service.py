from typing import Optional
from sqlalchemy.orm import Session
from app.repositories import account_repo
from app.schemas.account import AccountFormOut, AccountUpdate, IoType
from app.common.account_constants import INCOME_CATEGORIES, EXPENSE_CATEGORIES

def _io_type_from_amount(amount_signed: float) -> IoType:
    return "income" if amount_signed >= 0 else "expense"

def get_form(db: Session, user_id: int, account_id: int) -> Optional[AccountFormOut]:
    row = account_repo.get_by_id(db, user_id, account_id)
    if not row:
        return None
    io_type = _io_type_from_amount(row.amount)
    return AccountFormOut(
        id=row.id,
        io_type=io_type,
        amount=abs(float(row.amount)),
        category=row.category,
        date=row.date,
        description=row.description,
        method=row.method,
    )

def update(db: Session, user_id: int, account_id: int, payload: AccountUpdate) -> Optional[AccountFormOut]:
    row = account_repo.get_by_id(db, user_id, account_id)
    if not row:
        return None

    current_io = _io_type_from_amount(row.amount)
    io_type = payload.io_type or current_io

    # 카테고리 검증(validator 보완)
    if payload.category:
        if io_type == "income" and payload.category not in INCOME_CATEGORIES:
            raise ValueError("수입 카테고리 허용값이 아닙니다.")
        if io_type == "expense" and payload.category not in EXPENSE_CATEGORIES:
            raise ValueError("지출 카테고리 허용값이 아닙니다.")

    amount_signed = None
    if payload.amount is not None:
        amount_signed = payload.amount if io_type == "income" else -payload.amount

    row = account_repo.update_account(
        db,
        row,
        amount_signed=amount_signed,
        category=payload.category,
        date=payload.date,
        description=payload.description,
        method=payload.method,
    )
    return get_form(db, user_id, row.id)
