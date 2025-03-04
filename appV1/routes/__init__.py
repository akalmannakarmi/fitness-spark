from fastapi import APIRouter

from .user import router as userRouter
from .recipie import router as recipeRouter

router = APIRouter()

router.include_router(userRouter,tags=["User"],prefix="/user")
router.include_router(recipeRouter,tags=["Recipe"],prefix="/recipe")