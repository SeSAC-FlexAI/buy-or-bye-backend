from fastapi import APIRouter
from . import user, auth, account, fpti

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(fpti.router,    prefix="/fpti",    tags=["fpti"])