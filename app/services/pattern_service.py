from collections import defaultdict
from datetime import date
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session

from app.repositories import pattern_repo
from app.schemas.pattern import PatternOut, CategoryAgg, DayPoint, PatternSettingIn, PatternSettingOut

def _apply_rules(category: str, description: str | None, rules: Dict[str, str] | None) -> str:
    """
    description에 규칙 키워드가 포함되면 해당 카테고리로 재분류.
    규칙이 없거나 매칭 안 되면 원래 category 반환.
    """
    if not rules or not description:
        return category
    desc = description.lower()
    for kw, mapped in rules.items():
        if not kw:
            continue
        if kw.lower() in desc:
            return mapped
    return category

def get_pattern(db: Session, user_id: int, year: int, month: int, top: int = 5) -> PatternOut:
    setting = pattern_repo.get_setting(db, user_id)
    rules = None if not setting else pattern_repo._from_json_str(setting.rules_json)

    rows = pattern_repo.get_month_rows(db, user_id, year, month)

    # 집계 컨테이너
    income_total = 0.0
    expense_total = 0.0
    cat_sum: Dict[str, float] = defaultdict(float)  # 지출 집계는 양수(절대값)로
    daily: Dict[date, Tuple[float, float]] = defaultdict(lambda: (0.0, 0.0))  # d -> (inc, exp)

    for d, cat, desc, amt in rows:
        cat2 = _apply_rules(cat or "기타", desc, rules)
        if amt >= 0:
            income_total += float(amt)
            inc, exp = daily[d]
            daily[d] = (inc + float(amt), exp)
        else:
            a = abs(float(amt))
            expense_total += a
            cat_sum[cat2] += a
            inc, exp = daily[d]
            daily[d] = (inc, exp + a)

    # 카테고리 비율 계산 (지출 합계 기준)
    categories = []
    for c, a in sorted(cat_sum.items(), key=lambda x: x[1], reverse=True):
        ratio = (a / expense_total) if expense_total > 0 else 0.0
        categories.append(CategoryAgg(category=c, amount=round(a, 2), ratio=round(ratio, 6)))

    top_categories = categories[:top]

    daily_series = [
        DayPoint(d=k, income=round(v[0], 2), expense=round(v[1], 2))
        for k, v in sorted(daily.items(), key=lambda x: x[0])
    ]

    return PatternOut(
        year=year,
        month=month,
        income_total=round(income_total, 2),
        expense_total=round(expense_total, 2),
        top_categories=top_categories,
        categories=categories,
        daily_series=daily_series,
        monthly_budget=setting.monthly_budget if setting else None,
    )

def save_setting(db: Session, user_id: int, payload: PatternSettingIn) -> PatternSettingOut:
    rules = payload.rules if payload.rules else None
    row = pattern_repo.upsert_setting(db, user_id, payload.monthly_budget, rules)
    return PatternSettingOut.model_validate(row)
