from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.api.deps import get_current_user
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import register_user
from app.repositories.user_repo import UserRepository
from app.schemas.user_extra import UserEmailOut, PasswordChangeIn, EmailCheckOut
from app.services import user_service

router = APIRouter()

@router.post("/", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, payload)
    return user

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return UserRepository(db).list()

@router.get("/get_mail/{user_id}", response_model=UserEmailOut)
def get_mail(
    user_id: int,
    db: Session = Depends(get_db),
    _current = Depends(get_current_user),   # 인증 필요(본인/관리자 정책은 여기서 확장 가능)    
    ):
    res = user_service.get_email_by_user_id(db, user_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # 본인만 조회하게 하려면:
    # if _current.id != user_id: raise HTTPException(status_code=403, detail="Forbidden")
    return res

@router.put("/alter_pwd")
def alter_pwd(
    payload: PasswordChangeIn,
    db: Session = Depends(get_db),
    current = Depends(get_current_user),    # 반드시 로그인 필요
    ):
    ok = user_service.change_password(db, current.id, payload)
    if not ok:
        # 어디서 실패했는지 자세히 주고 싶으면 메시지 분기 가능
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password change failed")
    return {"success": True}

@router.get("/check", response_model=EmailCheckOut)
def check_email(
    email: str = Query(..., description="가입하려는 이메일"),
    db: Session = Depends(get_db),
    ):
    # 인증 불필요 – 회원가입 전 중복 체크 용도
    email_norm = email.strip().lower()
    return user_service.check_email_available(db, email_norm)
