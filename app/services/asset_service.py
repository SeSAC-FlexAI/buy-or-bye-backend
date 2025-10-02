# app/services/asset_service.py
from sqlalchemy.orm import Session
from app.repositories import asset_repo
from app.schemas.asset import AssetCreate, AssetUpdate

# ----- /me용 -----
def get_my_asset(db: Session, user_id: int):
    return asset_repo.get_by_user_id(db, user_id)

def upsert_my_asset(db: Session, user_id: int, payload: AssetCreate | AssetUpdate):
    return asset_repo.upsert_for_user(db, user_id, payload)

def delete_my_asset(db: Session, user_id: int) -> bool:
    return asset_repo.delete_by_user(db, user_id)

# # ----- (선택) 기존 id 기반을 계속 노출한다면: 소유권 보강 -----
# def get_asset_by_id(db: Session, user_id: int, asset_id: int):
#     return asset_repo.get_asset_by_id_for_user(db, user_id, asset_id)

# def update_asset(db: Session, user_id: int, asset_id: int, data: AssetUpdate):
#     return asset_repo.update_asset_by_id_for_user(db, user_id, asset_id, data)

# def delete_asset(db: Session, user_id: int, asset_id: int) -> bool:
#     return asset_repo.delete_asset_by_id_for_user(db, user_id, asset_id)
