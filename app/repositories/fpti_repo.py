# app/repositories/fpti_repo.py
import json
import uuid
from sqlalchemy.orm import Session
from typing import Optional
from app.models.fpti import FPTI
from app.schemas.fpti import FptiCreate, FptiUpdate

def _to_json_str(v):
    if v is None:
        return None
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False)

def create(db: Session, user_id: Optional[int], payload: FptiCreate) -> FPTI:
    post_id = uuid.uuid4().hex  # 32자리
    row = FPTI(
        user_id=user_id,
        post_id=post_id,
        title=payload.title,
        answers_json=_to_json_str(payload.answers),
        result_json=_to_json_str(payload.result),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def get_by_post_id(db: Session, post_id: str) -> Optional[FPTI]:
    return db.query(FPTI).filter(FPTI.post_id == post_id).first()

def update_by_post_id(db: Session, post_id: str, payload: FptiUpdate) -> Optional[FPTI]:
    row = get_by_post_id(db, post_id)
    if not row:
        return None
    if payload.title is not None:
        row.title = payload.title
    if payload.answers is not None:
        row.answers_json = _to_json_str(payload.answers)
    if payload.result is not None:
        row.result_json = _to_json_str(payload.result)
    db.commit()
    db.refresh(row)
    return row
