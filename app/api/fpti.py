# app/api/fpti.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.api.deps import get_current_user_optional
from app.schemas.fpti import FptiCreate, FptiUpdate, FptiOut
from app.services import fpti_service

router = APIRouter(tags=["fpti"])

@router.post("/posts", response_model=FptiOut)
def create_fpti(
    payload: FptiCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional),
):
    row = fpti_service.create(db, current_user, payload)
    return row

@router.get("/select/{post_id}", response_model=FptiOut)
def get_fpti(
    post_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional),
):
    row = fpti_service.get_for_view(db, current_user, post_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found or no permission")
    return row

@router.put("/update/{post_id}", response_model=FptiOut)
def update_fpti(
    post_id: str,
    payload: FptiUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional),
):
    row = fpti_service.update(db, current_user, post_id, payload)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found or no permission")
    return row
