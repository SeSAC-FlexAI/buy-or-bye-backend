from fastapi import APIRouter
from . import users, auth, budgets

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
