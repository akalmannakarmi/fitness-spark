from fastapi import APIRouter

from .admin import router as admin_router
from .meal_plans import router as meal_plan_router
from .recipes import router as recipe_router

v1_router = APIRouter()

v1_router.include_router(admin_router, tags=["Admin"], prefix="/admin")
v1_router.include_router(recipe_router, tags=["Recipe"], prefix="/recipe")
v1_router.include_router(meal_plan_router, tags=["Meal"], prefix="/meal_plan")
