# app/schemas/account.py
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, Literal
from datetime import date as Date
from app.common.account_constants import INCOME_CATEGORIES, EXPENSE_CATEGORIES

IoType = Literal["income", "expense"]  # 수입/지출

# ----------------------------
# 생성용 (폼 → 서버)
# ----------------------------
class AccountCreate(BaseModel):
    io_type: IoType = Field(
        ...,
        description="수입/지출 유형 (income=수입, expense=지출)"
    )
    amount: float = Field(
        gt=0,
        description="금액(양수). 수입/지출 부호 처리는 서버에서 수행"
    )
    category: str = Field(
        ...,
        description="카테고리 (수입: 월급/이자/기타 등, 지출: 식비/교통/주거 등)"
    )
    date: Date = Field(
        ...,
        description="거래 일자 (YYYY-MM-DD)"
    )
    description: Optional[str] = Field(
        None,
        description="메모(선택)"
    )
    method: Optional[str] = Field(
        None,
        description="결제수단 (예: '카드', '현금')"
    )

    # ✅ Swagger Request body 기본 예시
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "io_type": "income",
                "amount": 1500000,
                "category": "월급",
                "date": "2025-10-02",
                "description": "10월 급여",
                "method": "현금"
            }
        }
    )

    @field_validator("category")
    @classmethod
    def validate_category(cls, v, info):
        io_type = info.data.get("io_type")
        if io_type == "income" and v not in INCOME_CATEGORIES:
            raise ValueError(f"수입 카테고리 허용값이 아닙니다: {v}")
        if io_type == "expense" and v not in EXPENSE_CATEGORIES:
            raise ValueError(f"지출 카테고리 허용값이 아닙니다: {v}")
        return v


# ----------------------------
# 목록/상세 응답 (DB 부호 유지)
# ----------------------------
class AccountOut(BaseModel):
    id: int
    user_id: int
    amount: float        # DB: 수입(+), 지출(-)
    category: str
    date: Date
    description: Optional[str] = None
    method: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 321,
                "user_id": 1,
                "amount": -35000,
                "category": "식비",
                "date": "2025-10-02",
                "description": "점심",
                "method": "카드"
            }
        }
    )


# ----------------------------
# 편집 폼 조회 응답 (양수 금액 + io_type)
# ----------------------------
class AccountFormOut(BaseModel):
    id: int
    io_type: IoType
    amount: float        # 양수
    category: str
    date: Date
    description: Optional[str] = None
    method: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 321,
                "io_type": "expense",
                "amount": 35000,
                "category": "식비",
                "date": "2025-10-02",
                "description": "점심",
                "method": "카드"
            }
        }
    )


# ----------------------------
# 수정용 (부분 수정 허용)
# ----------------------------
class AccountUpdate(BaseModel):
    io_type: IoType | None = Field(
        default=None,
        description="수정 시에만 전달 (income|expense)"
    )
    amount: float | None = Field(
        default=None, gt=0,
        description="양수. 없으면 금액 변경 안 함"
    )
    category: str | None = Field(
        default=None, description="없으면 카테고리 변경 안 함"
    )
    date: Date | None = Field(
        default=None, description="없으면 일자 변경 안 함 (YYYY-MM-DD)"
    )
    description: str | None = Field(
        default=None, description="없으면 메모 변경 안 함"
    )
    method: str | None = Field(
        default=None, description="없으면 결제수단 변경 안 함 (예: '카드', '현금')"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "io_type": "expense",
                "amount": 42000,
                "category": "교통",
                "date": "2025-10-03",
                "description": "택시",
                "method": "현금"
            }
        }
    )

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
