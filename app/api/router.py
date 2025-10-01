from fastapi import APIRouter
from . import user, auth, account, asset, fpti, fpa, fsd, pattern, chatbot, error_report

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(asset.router, prefix="/assets", tags=["Assets"])
api_router.include_router(fpti.router,    prefix="/fpti",    tags=["fpti"])
api_router.include_router(fpa.router,     prefix="/fpa",     tags=["fpa"])
api_router.include_router(fsd.router,     prefix="/fsd",     tags=["fsd"])
api_router.include_router(pattern.router, prefix="/pattern", tags=["pattern"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(error_report.router, prefix="/error-report", tags=["error-report"])