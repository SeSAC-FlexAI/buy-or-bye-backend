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


def _apply_delta(db: Session, user_id: int, d: PostingDelta,tx_date: Date) -> None:
    """
    룰엔진에서 계산된 델타를 자산/수입/지출 스냅샷에 반영.
    - 자산: deposits_cash / real_estate / other_assets / loans / total_assets
    - 수입 합계, 지출 합계 누적 (단건 스냅샷 기준)
    """
    # 1) 자산 스냅샷
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
    # upsert_for_user가 Pydantic 모델을 기대하더라도 아래 trick으로 dict 주입 가능
    asset_repo.upsert_for_user(
        db, user_id,
        type("Obj", (object,), {"dict": lambda s, exclude_unset=True: aset_payload})()
    )

    # 2) 수입/지출 합계 누적
    if d.income_delta:
        inc = income_repo.get_by_user_id(db, user_id) or income_repo.upsert_for_user(db, user_id, data={"date": tx_date})
        income_repo.upsert_for_user(
            db, user_id,
            type("Obj", (object,), {"dict": lambda s, exclude_unset=True: {
                "total_income": (getattr(inc, "total_income", 0) or 0) + d.income_delta
            }})()
        )
    if d.expense_delta:
        exp = expense_repo.get_by_user_id(db, user_id) or expense_repo.upsert_for_user(db, user_id, data={"date": tx_date})
        expense_repo.upsert_for_user(
            db, user_id,
            type("Obj", (object,), {"dict": lambda s, exclude_unset=True: {
                "total_expense": (getattr(exp, "total_expense", 0) or 0) + d.expense_delta
            }})()
        )


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
    """
    가계부 생성:
    1) 레포에 저장(수입=+, 지출=- 부호 규칙 유지)
    2) 룰 엔진 델타 계산 → 스냅샷 반영
    3) 편집폼 형태로 반환
    """
    # 1) 저장
    row = account_repo.create_account(db, user_id, payload)

    # 2) 델타 적용
    d = calc_posting_delta(
        io_type=payload.io_type,
        category=payload.category,
        method=payload.method or "",
        amount=payload.amount
    )
    
    tx_date = payload.date

    _apply_delta(db, user_id, d, tx_date)

    # 3) 편집폼 반환
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
    """
    가계부 수정:
    - 기존 값 델타를 역적용 → 스냅샷 되돌림
    - 새 값 저장 → 새 델타 적용
    """
    row = account_repo.get_by_id(db, user_id, account_id)
    if not row:
        return None

    # 현재 io_type은 DB 부호로 판단
    current_io: IoType = _io_type_from_amount(row.amount)
    io_type: IoType = payload.io_type or current_io

    # 카테고리 검증(선제적 가드)
    if payload.category:
        if io_type == "income" and payload.category not in INCOME_CATEGORIES:
            raise ValueError("수입 카테고리 허용값이 아닙니다.")
        if io_type == "expense" and payload.category not in EXPENSE_CATEGORIES:
            raise ValueError("지출 카테고리 허용값이 아닙니다.")

    # 1) 이전 델타 역적용
    d_prev = calc_posting_delta(
        io_type=current_io,
        category=row.category,
        method=row.method or "",
        amount=abs(row.amount),
    )
    # 역적용(부호 반전)
    for k, v in d_prev.__dict__.items():
        setattr(d_prev, k, -v)

    tx_date = payload.date

    _apply_delta(db, user_id, d_prev, tx_date)

    # 2) 업데이트 (부호 규칙 적용)
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

    # 3) 신규 델타 적용
    d_new = calc_posting_delta(
        io_type=io_type,
        category=row.category,
        method=row.method or "",
        amount=abs(row.amount),
    )
    _apply_delta(db, user_id, d_new, tx_date)

    return get_form(db, user_id, row.id)


def delete(db: Session, user_id: int, account_id: int) -> bool:
    """
    가계부 삭제:
    - 삭제 전, 기존 값 델타를 역적용하여 스냅샷 되돌림
    """
    row = account_repo.get_by_id(db, user_id, account_id)
    if not row:
        return False

    prev_io: IoType = _io_type_from_amount(row.amount)
    d_prev = calc_posting_delta(
        io_type=prev_io,
        category=row.category,
        method=row.method or "",
        amount=abs(row.amount),
    )
    for k, v in d_prev.__dict__.items():
        setattr(d_prev, k, -v)

    tx_date = date.today()    
    _apply_delta(db, user_id, d_prev, tx_date)

    return account_repo.delete_by_id(db, user_id, account_id)
