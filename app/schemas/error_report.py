from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ErrorReportCreate(BaseModel):
    user_id: int        # 요청자가 명시적으로 전달 (원하면 인증으로 대체 가능)
    message: str

class ErrorReportOut(BaseModel):
    id: int
    user_id: int
    message: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
