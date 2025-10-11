# ✅ 이미 "대출"이 수입/지출 모두에 존재하면 OK, 없으면 추가
# INCOME_CATEGORIES = {
#     "salary", "pin_money", "investment_income", "side_income",
#     "loans",          # ← 대출 실행(입금)으로 사용
# }

# 1차 수정 매핑 10.11 
# CATEGORY_TO_FIELD = {
#     "월급": "salary",
#     "투자수익": "investment_income",
#     "부가수익": "side_income",
#     "용돈": "pin_money",
#     "대출": "loans",  # 유입(대출금 유입)을 수입에 적는 정책이라면 유지, 아니면 제거
# }

INCOME_CATEGORIES = {
    "월급", "용돈", "투자", "부가수익",
    "대출",          # ← 대출 실행(입금)으로 사용
}

# EXPENSE_CATEGORIES = {
#     "food", "shopping", "transportation", "household_maintenance", "culture_leisure",
#     "household_goods", "card_payment_withdrawal", "investment_expense", "other",
#     "loans",          # ← 대출 원금 상환(출금)으로 사용
# }

# 1차 수정 매핑 10.11
# CATEGORY_TO_FIELD = { 
#     "식비": "food",
#     "쇼핑": "shopping",
#     "교통/차량": "transportation",
#     "집/관리비": "household_maintenance",
#     "문화/여가": "culture_leisure",
#     "생활용품": "household_goods",  # (구 cosmetic → household_goods 로 바꿨다고 하셨음)
#     "카드대금": "card_payment_withdrawal",
#     "투자수익": "investment_expense",
#     "기타": "other",
#     "대출": "loans",     
# }

EXPENSE_CATEGORIES = {
    "식비", "쇼핑", "교통/차량", "집/관리비", "문화/여가",
    "생활용품", "카드대금", "투자수익", "기타",
    "대출",          # ← 대출 원금 상환(출금)으로 사용
}

PAYMENT_METHODS = {"card", "cash"}