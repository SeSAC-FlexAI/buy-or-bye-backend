# app/services/account_posting_rules.py
from dataclasses import dataclass

@dataclass
class PostingDelta:
    deposits_cash_delta: int = 0
    real_estate_delta: int = 0
    other_assets_delta: int = 0
    loans_delta: int = 0
    income_delta: int = 0
    expense_delta: int = 0

def calc_posting_delta(*, io_type: str, category: str, method: str | None, amount: float) -> PostingDelta:
    d = PostingDelta()
    amt = int(abs(amount))
    mtd = (method or "").upper()

    # 1) 카드대금 출금: 자산만 감소 (지출합계 X)
    if category == "카드 대금 출금":
        d.deposits_cash_delta -= amt
        return d

    # 2) 투자(부동산/금융 등): io_type으로 매수/매도 해석 (세부 파생 제외)
    if category == "투자(부동산, 금융 등)":
        if io_type == "expense":   # 매수
            d.deposits_cash_delta -= amt
            d.other_assets_delta  += amt
        else:                      # income = 매도
            d.deposits_cash_delta += amt
            d.other_assets_delta  -= amt
        return d

    # 3) 대출: 이자/이율 계산 없이 흐름만 반영
    if category == "대출":
        if io_type == "income":    # 대출 실행(입금)
            d.deposits_cash_delta += amt
            d.loans_delta         += amt
            d.income_delta        += amt    # ✅ 수입 합계에 포함
        else:                      # expense = 원금 상환(출금)
            d.deposits_cash_delta -= amt
            d.loans_delta         -= amt
            d.expense_delta       += amt    # ✅ 지출 합계에 포함
        return d

    # 4) 일반 수입/지출
    if io_type == "income":
        d.income_delta       += amt
        d.deposits_cash_delta += amt
        return d

    if io_type == "expense":
        d.expense_delta      += amt
        if mtd != "카드":                 # 카드 지출은 자산 즉시 감소 없음
            d.deposits_cash_delta -= amt
        return d

    return d
