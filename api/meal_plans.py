from typing import Any

from fastapi import APIRouter, Depends

from config import Actions, Models
from crud.meal_plans import (
    db_create_meal_plan,
    db_delete_meal_plan,
    db_get_meal_plan,
    db_get_meal_plans,
    db_update_meal_plan,
)
from crud.stats import update_stats
from deps import get_current_user
from schemas.common import MongoObjectId, SuccessResponse, num_pages
from schemas.meal_plan import (
    MealPlanCreate,
    MealPlanFilter,
    MealPlanOut,
    MealPlansOut,
    MealPlanUpdate,
)
from schemas.user import User

router = APIRouter()


@router.get("/get/meal_plans", response_model=MealPlansOut)
async def get_meal_plans(filters: MealPlanFilter = Depends()) -> dict[str, Any]:
    meal_plans, total = await db_get_meal_plans(filters, public_only=True)
    return {
        "meal_plans": meal_plans,
        "total": total,
        "page": filters.page,
        "limit": filters.limit,
        "pages": num_pages(total, filters.limit),
    }


@router.get("/get/my/meal_plans", response_model=MealPlansOut)
async def get_user_meal_plans(
    user: User = Depends(get_current_user), filters: MealPlanFilter = Depends()
) -> dict[str, Any]:
    meal_plans, total = await db_get_meal_plans(filters, user_id=user.id)
    return {
        "meal_plans": meal_plans,
        "total": total,
        "page": filters.page,
        "limit": filters.limit,
        "pages": num_pages(total, filters.limit),
    }


@router.get("/get/meal_plan/{meal_plan_id}", response_model=MealPlanOut)
@update_stats(Models.Plans, Actions.Read)
async def get_meal_plan(
    meal_plan_id: MongoObjectId, user: User = Depends(get_current_user)
) -> dict[str, Any]:
    return await db_get_meal_plan(meal_plan_id, user.id)


@router.post("/create/meal_plan", response_model=SuccessResponse)
@update_stats(Models.Plans, Actions.Create)
async def create_meal_plan(
    form: MealPlanCreate, user: User = Depends(get_current_user)
) -> dict[str, Any]:
    meal_plan_id = await db_create_meal_plan(user.id, form)
    return {
        "status": "Success",
        "message": "Created Meal Plan Successfully!",
        "data": {"meal_plan_id": str(meal_plan_id)},
    }


@router.patch("/update/meal_plan/{meal_plan_id}", response_model=SuccessResponse)
@update_stats(Models.Plans, Actions.Update)
async def update_meal_plan(
    meal_plan_id: MongoObjectId,
    form: MealPlanUpdate,
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    await db_update_meal_plan(meal_plan_id, form, user.id)
    return {
        "status": "Success",
        "message": "Updated Meal Plan Successfully!",
        "data": {"meal_plan_id": meal_plan_id},
    }


@router.delete("/delete/meal_plan/{meal_plan_id}", response_model=SuccessResponse)
@update_stats(Models.Plans, Actions.Delete)
async def delete_meal_plan(
    meal_plan_id: MongoObjectId, user: User = Depends(get_current_user)
) -> dict[str, Any]:
    await db_delete_meal_plan(meal_plan_id, user.id)
    return {
        "status": "Success",
        "message": "Deleted Meal Plan Successfully!",
        "data": {"meal_plan_id": meal_plan_id},
    }
