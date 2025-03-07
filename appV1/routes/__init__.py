from fastapi import APIRouter

from .recipie import router as recipeRouter

router = APIRouter()

router.include_router(recipeRouter,tags=["Recipe"],prefix="/recipe")