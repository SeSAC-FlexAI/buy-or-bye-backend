# app/services/account_service.py
from typing import Optional
from sqlalchemy.orm import Session

from app.repositories import account_repo
from app.schemas.account import AccountFormOut, AccountUpdate, AccountCreate, IoType
from app.common.account_constants import INCOME_CATEGORIES, EXPENSE_CATEGORIES
from app.services.account_posting_rules import calc_posting_delta, PostingDelta

# 자산/수입/지출 "스냅샷" 업데이트용 레포 (프로젝트 내 실제 이름과 동일해야 합니다)
from app.repositories import asset_repo, income_repo, expense_repo
from datetime import date as Date


def _io_type_from_amount(amount_signed: float) -> IoType:
    """금액 부호로 io_type(income|expense) 판별"""
    return "income" if amount_signed >= 0 else "expense"


def _apply_delta(
    db: Session,
    user_id: int,
    d: PostingDelta,
    tx_date: Date,
    *,
    io_type: Optional[IoType] = None,
    category: Optional[str] = None,
) -> None:
    """
    룰엔진 델타를 자산/수입/지출 스냅샷에 반영.
    - 자산: deposits_cash / real_estate / other_assets / loans / total_assets
    - 수입/지출: '카테고리별 컬럼'을 갱신하고, 합계(total_*)는 자동 재계산
    """

    # 1) 자산 스냅샷 (그대로 유지)
    asset = asset_repo.get_by_user_id(db, user_id) or asset_repo.upsert_for_user(db, user_id, data={"date": tx_date})
    aset_payload = {
        "deposits_cash": (getattr(asset, "deposits_cash", 0) or 0) + d.deposits_cash_delta,
        "real_estate":   (getattr(asset, "real_estate",   0) or 0) + d.real_estate_delta,
        "other_assets":  (getattr(asset, "other_assets",  0) or 0) + d.other_assets_delta,
        "loans":         (getattr(asset, "loans",         0) or 0) + d.loans_delta,
    }
    aset_payload["total_assets"] = (
        aset_payload["deposits_cash"]
        + aset_payload["real_estate"]
        + aset_payload["other_assets"]
        - aset_payload["loans"]
    )
    asset_repo.upsert_for_user(
        db, user_id,
        type("Obj", (object,), {"dict": lambda s, exclude_unset=True: aset_payload})()
    )

    # 2) 수입/지출 스냅샷 - ✅ 합계만 더하지 말고, 카테고리 컬럼을 갱신하도록 변경
    if io_type == "income" and d.income_delta:
        # 예: "월급" -> incomes.salary += amount  (그리고 total_income은 자동 재계산)
        income_repo.apply_delta(db, user_id, tx_date, category or "", float(d.income_delta))

    if io_type == "expense" and d.expense_delta:
        # 예: "식비" -> expenses.food += amount  (그리고 total_expense는 자동 재계산)
        expense_repo.apply_delta(db, user_id, tx_date, category or "", float(d.expense_delta))

    # repo의 apply_delta()는 커밋하지 않으므로 여기서 한번에 커밋
    db.commit()


def get_form(db: Session, user_id: int, account_id: int) -> Optional[AccountFormOut]:
    """편집폼 전용 조회(양수=수입, 음수=지출로 변환해 amount 절대값 반환)"""
    row = account_repo.get_by_id(db, user_id, account_id)
    if not row:
        return None
    io_type = _io_type_from_amount(row.amount)
    return AccountFormOut(
        id=row.id,
        io_type=io_type,
        amount=abs(row.amount),
        category=row.category,
        date=row.date,
        description=row.description,
        method=row.method,
    )


def create(db: Session, user_id: int, payload: AccountCreate) -> AccountFormOut:
    row = account_repo.create_account(db, user_id, payload)

    d = calc_posting_delta(
        io_type=payload.io_type,
        category=payload.category,
        method=payload.method or "",
        amount=payload.amount,
    )
    tx_date = payload.date

    # ✅ io_type / category를 함께 전달
    _apply_delta(db, user_id, d, tx_date, io_type=payload.io_type, category=payload.category)

    return AccountFormOut(
        id=row.id,
        io_type=payload.io_type,
        amount=payload.amount,
        category=row.category,
        date=row.date,
        description=row.description,
        method=row.method,
    )

def update(db: Session, user_id: int, account_id: int, payload: AccountUpdate) -> Optional[AccountFormOut]:
    row = account_repo.get_by_id(db, user_id, account_id)
    if not row:
        return None

    current_io: IoType = _io_type_from_amount(row.amount)
    io_type: IoType = payload.io_type or current_io

    if payload.category:
        if io_type == "income" and payload.category not in INCOME_CATEGORIES:
            raise ValueError("수입 카테고리 허용값이 아닙니다.")
        if io_type == "expense" and payload.category not in EXPENSE_CATEGORIES:
            raise ValueError("지출 카테고리 허용값이 아닙니다.")

    # 1) 이전값 역적용
    d_prev = calc_posting_delta(
        io_type=current_io,
        category=row.category,
        method=row.method or "",
        amount=abs(row.amount),
    )
    for k, v in d_prev.__dict__.items():
        setattr(d_prev, k, -v)

    tx_date = payload.date or row.date
    _apply_delta(db, user_id, d_prev, tx_date, io_type=current_io, category=row.category)

    # 2) DB 업데이트 (부호 규칙 적용)
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

    # 3) 신규값 적용
    d_new = calc_posting_delta(
        io_type=io_type,
        category=row.category,
        method=row.method or "",
        amount=abs(row.amount),
    )
    _apply_delta(db, user_id, d_new, row.date, io_type=io_type, category=row.category)

    return get_form(db, user_id, row.id)
    

def _negate_delta(d):
    d.income_delta *= -1
    d.expense_delta *= -1
    d.deposits_cash_delta *= -1
    d.other_assets_delta *= -1
    d.real_estate_delta *=-1
    d.loans_delta *=-1
    return d


def delete(db: Session, user_id: int, account_id: int) -> bool:
    row = account_repo.get_by_id(db, user_id, account_id)
    if not row or row.user_id != user_id:
        return False

    # DB에는 amount가 수입은 +, 지출은 - 로 저장되어 있다고 가정
    io_type = "income" if row.amount > 0 else "expense"
    amt = abs(row.amount)
    category = row.category
    method = row.method
    tx_date = row.date

    # 생성 시 계산했던 것과 동일한 델타 계산 후 '역적용'
    d = calc_posting_delta(io_type=io_type, category=category, amount=amt, method=method)
    d.category = category  # (bump_by_category에서 카테고리 참고)

    _apply_delta(db, user_id, _negate_delta(d), tx_date, io_type=io_type, category=category)

    # 마지막에 거래 삭제
    return account_repo.delete_by_id(db, user_id, account_id)