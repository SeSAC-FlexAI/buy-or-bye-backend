from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

class UserEmailOut(BaseModel):
    user_id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class PasswordChangeIn(BaseModel):
    current_password: str = Field(min_length=6, max_length=256)
    new_password: str = Field(min_length=8, max_length=256)

class EmailCheckOut(BaseModel):
    email: EmailStr
    available: bool  # True면 가입 가능(중복 없음)
