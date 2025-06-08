from fastapi import APIRouter
from .users_router import router as users_router
from .auth_router import router as auth_router
from .jobs_router import router as jobs_router
from .home_route import router as home_router


router = APIRouter()

router.include_router(home_router)
router.include_router(users_router, prefix="/user", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(jobs_router, prefix="/job", tags=["job"])
