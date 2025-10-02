from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, Literal
from datetime import date as Date
from app.common.account_constants import INCOME_CATEGORIES, EXPENSE_CATEGORIES

IoType = Literal["income", "expense"]  # 수입/지출

# 생성용 (폼 → 서버)
class AccountCreate(BaseModel):
    io_type: IoType
    amount: float = Field(gt=0)        # 입력은 항상 양수
    category: str
    date: Date
    description: Optional[str] = None
    method: Optional[str] = Field(None, description="결제수단 (예: '카드' / '현금')")


    @field_validator("category")
    @classmethod
    def validate_category(cls, v, info):
        io_type = info.data.get("io_type")
        if io_type == "income" and v not in INCOME_CATEGORIES:
            raise ValueError(f"수입 카테고리 허용값이 아닙니다: {v}")
        if io_type == "expense" and v not in EXPENSE_CATEGORIES:
            raise ValueError(f"지출 카테고리 허용값이 아닙니다: {v}")
        return v

# 목록/상세 응답 (DB 부호 유지)
class AccountOut(BaseModel):
    id: int
    user_id: int
    amount: float       # DB: 수입(+), 지출(-)
    category: str
    date: Date
    description: Optional[str] = None
    method: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# 편집 폼 조회 응답 (폼에 넣기 쉬움: 양수 금액 + io_type)
class AccountFormOut(BaseModel):
    id: int
    io_type: IoType
    amount: float       # 양수
    category: str
    date: Date
    description: Optional[str] = None
    method: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# 수정용 (부분 수정 허용)
class AccountUpdate(BaseModel):
    io_type: IoType | None = None
    amount: float | None = Field(default=None, gt=0)  # 양수, 없으면 수정 안 함
    category: str | None = None
    date: Date | None = None                          # <-- 중요: Optional date
    description: str | None = None
    method: str | None = None

    @field_validator("category")
    @classmethod
    def validate_category(cls, v, info):
        if v is None:
            return v
        io_type = info.data.get("io_type")
        if io_type == "income" and v not in INCOME_CATEGORIES:
            raise ValueError(f"수입 카테고리 허용값이 아닙니다: {v}")
        if io_type == "expense" and v not in EXPENSE_CATEGORIES:
            raise ValueError(f"지출 카테고리 허용값이 아닙니다: {v}")
        return v
