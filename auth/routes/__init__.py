from fastapi import APIRouter

from .auth import router as authRouter
from .admin import router as adminRouter

router = APIRouter()
router.include_router(authRouter)
router.include_router(adminRouter,prefix="/admin")
