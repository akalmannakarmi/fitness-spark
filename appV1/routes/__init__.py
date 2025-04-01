from fastapi import APIRouter

from .recipe import router as recipeRouter
from .meal_plans import router as mealPlanRouter
from .admin import router as adminRouter

router = APIRouter()

router.include_router(adminRouter,tags=["Admin"],prefix="/admin")
router.include_router(recipeRouter,tags=["Recipe"],prefix="/recipe")
router.include_router(mealPlanRouter,tags=["Meal"],prefix="/meal_plan")