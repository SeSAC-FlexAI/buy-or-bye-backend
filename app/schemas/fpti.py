# app/schemas/fpti.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class FptiBase(BaseModel):
    title: Optional[str] = None
    answers: Optional[Any] = None   # dict/list/str 허용
    result: Optional[Any] = None

class FptiCreate(FptiBase):
    pass  # 게스트도 가능하니 필수 필드 없음

class FptiUpdate(BaseModel):
    title: Optional[str] = None
    answers: Optional[Any] = None
    result: Optional[Any] = None

class FptiOut(FptiBase):
    id: int
    post_id: str
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
