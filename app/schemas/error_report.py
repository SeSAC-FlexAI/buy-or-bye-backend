from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ErrorReportCreate(BaseModel):
    user_id: int = Field(..., description="오류를 보고한 사용자 ID")
    message: str = Field(..., description="오류 상세 메시지/스택")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "message": "[Account] KeyError: 'amount' at /api/account"
            }
        }
    )

class ErrorReportOut(BaseModel):
    id: int
    user_id: int
    message: str
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 12,
                "user_id": 1,
                "message": "[Account] KeyError: 'amount' at /api/account",
                "created_at": "2025-10-02T08:30:00Z"
            }
        }
    )
