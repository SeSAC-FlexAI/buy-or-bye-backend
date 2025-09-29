from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from app.repositories import fsd_repo
from app.schemas.fsd import FsdHomeOut, FsdSettingIn, FsdSettingOut, CategorySummary, FpaBrief

def get_home(db: Session, user_id: int, year: Optional[int], month: Optional[int]) -> FsdHomeOut:
    today = date.today()
    year = year or today.year
    month = month or today.month

    income, expense = fsd_repo.get_month_income_expense(db, user_id, year, month)
    top = fsd_repo.get_top_categories(db, user_id, year, month, limit=5)
    snap_date, net_worth = fsd_repo.get_latest_fpa(db, user_id)
    setting = fsd_repo.get_setting(db, user_id)

    # 목표 달성률: 누적 월저축 추정(단순화) = monthly_saving * 경과개월 / target_amount
    progress = None
    if setting and setting.target_amount and setting.monthly_saving:
        # 간단 추정: 목표 시작 시점 가정치가 없으므로, 목표일까지 남은개월/경과개월로 계산하고 싶으면 추가 모델 필요
        # 여기선 현재 잔여 필요금액 대비 월저축으로 달성률 근사치 제공
        if net_worth is not None:
            # 예: net_worth가 목표금액에 얼마나 근접했는지 비율
            progress = max(0.0, min(1.0, float(net_worth) / float(setting.target_amount)))

    return FsdHomeOut(
        year=year,
        month=month,
        income_total=income,
        expense_total=expense,
        balance=income - expense,
        top_categories=[CategorySummary(category=c, amount=a) for c, a in top],
        latest_fpa=FpaBrief(snapshot_date=snap_date, net_worth=net_worth),
        goal_progress=progress,
        setting=FsdSettingOut.model_validate(setting) if setting else None,
    )

def upsert_setting(db: Session, user_id: int, payload: FsdSettingIn) -> FsdSettingOut:
    data = payload.model_dump(exclude_unset=True)
    row = fsd_repo.upsert_setting(db, user_id, data)
    return FsdSettingOut.model_validate(row)
