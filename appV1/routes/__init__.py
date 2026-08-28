from fastapi import APIRouter

from .admin import router as admin_router
from .meal_plans import router as meal_plan_router
from .recipe import router as recipe_router

router = APIRouter()

router.include_router(admin_router, tags=["Admin"], prefix="/admin")
router.include_router(recipe_router, tags=["Recipe"], prefix="/recipe")
router.include_router(meal_plan_router, tags=["Meal"], prefix="/meal_plan")
