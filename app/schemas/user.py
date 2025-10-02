from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="로그인 이메일(아이디)")
    nickname: str = Field(..., description="표시 이름")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "nickname": "관리자"
            }
        }
    )

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="비밀번호 (최소 8자)")
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "nickname": "관리자",
                "password": "admin1234"
            }
        }
    )

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "admin@example.com",
                "nickname": "관리자"
            }
        }
    )
