# ✅ 이미 "대출"이 수입/지출 모두에 존재하면 OK, 없으면 추가
INCOME_CATEGORIES = {
    "salary", "pin_money", "investment_income", "side_income",
    "loans",          # ← 대출 실행(입금)으로 사용
}

EXPENSE_CATEGORIES = {
    "food", "shopping", "transportation", "household_maintenance", "culture_leisure",
    "household_goods", "card_payment_withdrawal", "investment_expense", "other",
    "loans",          # ← 대출 원금 상환(출금)으로 사용
}

PAYMENT_METHODS = {"card", "cash"}