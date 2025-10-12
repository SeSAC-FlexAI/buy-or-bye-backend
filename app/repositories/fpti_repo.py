# app/repositories/fpti_repo.py
from typing import Optional
from sqlalchemy.orm import Session
from uuid import uuid4
from app.models.fpti import FPTI
from app.schemas.fpti import FptiCreate

class FptiRepo:
    def get_by_post_id(self, db: Session, user_id: int, post_id: str) -> Optional[FPTI]:
        return (
            db.query(FPTI)
            .filter(FPTI.user_id == user_id, FPTI.post_id == post_id)
            .first()
        )

    # ★ 로그인 사용자 기준 단건 조회 (가장 최근 1건)
    def get_by_user_id(self, db: Session, user_id: int) -> Optional[FPTI]:
        return (
            db.query(FPTI)
            .filter(FPTI.user_id == user_id)
            .order_by(FPTI.id.desc())
            .first()
        )

    # ★ 사용자 기준 업서트
    def upsert_by_user(self, db: Session, user_id: int, payload: FptiCreate) -> FPTI:
        row = self.get_by_user_id(db, user_id)

        if row is None:
            row = FPTI(
                post_id=str(uuid4()),
                user_id=user_id,
                title=payload.title,
                result=payload.result,  # serializer가 합쳐준 dict
                type_code=payload.type_code,
                type_alias=payload.type_alias,
                type_name_en=payload.type_name_en,
                summary=payload.summary,
                who_text=payload.who_text,
                when_text=payload.when_text,
                what_text=payload.what_text,
                how_text=payload.how_text,
            )
            db.add(row)
        else:
            row.title = payload.title
            row.result = payload.result
            row.type_code = payload.type_code
            row.type_alias = payload.type_alias
            row.type_name_en = payload.type_name_en
            row.summary = payload.summary
            row.who_text = payload.who_text
            row.when_text = payload.when_text
            row.what_text = payload.what_text
            row.how_text = payload.how_text

        db.commit()
        db.refresh(row)
        return row

fpti_repo = FptiRepo()
