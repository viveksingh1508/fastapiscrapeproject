from fastapi import APIRouter
from .users_router import router as users_router
from .auth_router import router as auth_router


router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
