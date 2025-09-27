from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.models.fpa import FPA
from app.schemas.fpa import FpaCreate
from app.repositories import fpa_repo

def create(db: Session, current_user: User, payload: FpaCreate) -> FPA:
    # 순자산 계산은 repo에서 처리하지만, 여기서도 비즈니스 검증 가능
    return fpa_repo.create(db, current_user.id, payload)

def get_by_id_owned(db: Session, current_user: User, _id: int) -> Optional[FPA]:
    row = fpa_repo.get_by_id(db, _id)
    if not row:
        return None
    if row.user_id != current_user.id:
        return None
    return row

def delete_owned(db: Session, current_user: User, _id: int) -> bool:
    row = get_by_id_owned(db, current_user, _id)
    if not row:
        return False
    fpa_repo.delete(db, row)
    return True
