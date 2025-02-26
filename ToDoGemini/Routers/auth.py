from fastapi import APIRouter
from .auth import router as auth_router

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/get_user")
async def get_user():
    return "Hello World!"