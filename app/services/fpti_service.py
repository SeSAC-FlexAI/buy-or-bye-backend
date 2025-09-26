# app/services/fpti_service.py
from sqlalchemy.orm import Session
from typing import Optional
from app.models.fpti import FPTI
from app.models.user import User
from app.repositories import fpti_repo
from app.schemas.fpti import FptiCreate, FptiUpdate

def create(db: Session, current_user: Optional[User], payload: FptiCreate) -> FPTI:
    user_id = current_user.id if current_user else None
    return fpti_repo.create(db, user_id, payload)

def get_for_view(db: Session, current_user: Optional[User], post_id: str) -> Optional[FPTI]:
    row = fpti_repo.get_by_post_id(db, post_id)
    if not row:
        return None
    # 로그인 사용자인데 남의 데이터면? → 게스트 데이터(user_id is None)는 모두 열람 허용
    if row.user_id and current_user and row.user_id != current_user.id:
        # 소유자 다르면 막을지 허용할지 정책 선택 (여기선 막음)
        return None
    return row

def update(db: Session, current_user: Optional[User], post_id: str, payload: FptiUpdate) -> Optional[FPTI]:
    row = fpti_repo.get_by_post_id(db, post_id)
    if not row:
        return None
    # 수정 권한: (1) 본인 소유 or (2) 게스트 데이터
    if row.user_id and (not current_user or row.user_id != current_user.id):
        return None
    return fpti_repo.update_by_post_id(db, post_id, payload)
