from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.api.deps import get_current_user
from app.schemas.fpa import FpaCreate, FpaOut
from app.services import fpa_service

router = APIRouter(tags=["fpa"])

@router.post("", response_model=FpaOut)  # POST /api/fpa
def create_fpa(
    payload: FpaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    row = fpa_service.create(db, current_user, payload)
    # detail_json → detail 로 직렬화해 반환하려면 Pydantic 모델로 매핑될 때 커버됨(스키마 필드명 detail)
    return row

@router.get("/{fpa_id}", response_model=FpaOut)  # GET /api/fpa/{id}
def get_fpa(
    fpa_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    row = fpa_service.get_by_id_owned(db, current_user, fpa_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return row

@router.delete("/{fpa_id}")  # DELETE /api/fpa/{id}
def delete_fpa(
    fpa_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    ok = fpa_service.delete_owned(db, current_user, fpa_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return {"detail": "ok"}
