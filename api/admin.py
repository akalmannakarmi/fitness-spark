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
from crud.recipes import (
    db_create_recipe,
    db_delete_recipe,
    db_get_recipe,
    db_get_recipes,
    db_update_recipe,
)
from crud.stats import update_stats
from deps import require_admin
from schemas.common import MongoObjectId, SuccessResponse, num_pages
from schemas.meal_plan import (
    MealPlanCreate,
    MealPlanFilter,
    MealPlanOut,
    MealPlansOut,
    MealPlanUpdate,
)
from schemas.recipe import (
    RecipeCreate,
    RecipeFilter,
    RecipeOut,
    RecipesOut,
    RecipeUpdate,
)
from schemas.user import User

router = APIRouter()


@router.get("/get/recipes", response_model=RecipesOut)
@update_stats(Models.Recipe, Actions.Read)
async def get_recipes(
    filters: RecipeFilter = Depends(),
    _: User = Depends(require_admin),
) -> dict[str, Any]:
    recipes, total = await db_get_recipes(filters)

    return {
        "recipes": recipes,
        "page": filters.page,
        "limit": filters.limit,
        "total": total,
        "pages": num_pages(total, filters.limit),
    }


@router.get("/get/recipe/{recipe_id}", response_model=RecipeOut)
@update_stats(Models.Recipe, Actions.Read)
async def get_recipe(
    recipe_id: MongoObjectId, _: User = Depends(require_admin)
) -> dict[str, Any]:
    return await db_get_recipe(recipe_id)


@router.post("/create/recipe", response_model=SuccessResponse)
@update_stats(Models.Recipe, Actions.Create)
async def create_recipe(
    form: RecipeCreate, _: User = Depends(require_admin)
) -> dict[str, Any]:
    recipe_id = await db_create_recipe(form)
    return {
        "status": "Success",
        "message": "Created Recipe Successfully!",
        "data": {"recipe_id": str(recipe_id)},
    }


@router.patch("/update/recipe/{recipe_id}", response_model=SuccessResponse)
@update_stats(Models.Recipe, Actions.Update)
async def update_recipe(
    recipe_id: MongoObjectId, form: RecipeUpdate, _: User = Depends(require_admin)
) -> dict[str, Any]:
    updated_id = await db_update_recipe(recipe_id, form)
    return {
        "status": "Success",
        "message": "Updated Recipe Successfully!",
        "data": {"recipe_id": str(updated_id)},
    }


@router.delete("/delete/recipe/{recipe_id}", response_model=SuccessResponse)
@update_stats(Models.Recipe, Actions.Delete)
async def delete_recipe(
    recipe_id: MongoObjectId, _: User = Depends(require_admin)
) -> dict[str, Any]:
    deleted_id = await db_delete_recipe(recipe_id)
    return {
        "status": "Success",
        "message": "Deleted Recipe Successfully!",
        "data": {"recipe_id": str(deleted_id)},
    }


@router.get("/get/meal_plans", response_model=MealPlansOut)
@update_stats(Models.Plans, Actions.Read)
async def get_meal_plans(
    _: User = Depends(require_admin), filters: MealPlanFilter = Depends()
) -> dict[str, Any]:
    meal_plans, total = await db_get_meal_plans(filters)
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
    meal_plan_id: MongoObjectId, _: User = Depends(require_admin)
) -> dict[str, Any]:
    return await db_get_meal_plan(meal_plan_id)


@router.post("/create/meal_plan", response_model=SuccessResponse)
@update_stats(Models.Plans, Actions.Create)
async def create_meal_plan(
    form: MealPlanCreate, user: User = Depends(require_admin)
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
    meal_plan_id: MongoObjectId, form: MealPlanUpdate, _: User = Depends(require_admin)
) -> dict[str, Any]:
    updated_id = await db_update_meal_plan(meal_plan_id, form)
    return {
        "status": "Success",
        "message": "Updated Meal Plan Successfully!",
        "data": {"meal_plan_id": str(updated_id)},
    }


@router.delete("/delete/meal_plan/{meal_plan_id}", response_model=SuccessResponse)
@update_stats(Models.Plans, Actions.Delete)
async def delete_meal_plan(
    meal_plan_id: MongoObjectId, _: User = Depends(require_admin)
) -> dict[str, Any]:
    deleted_id = await db_delete_meal_plan(meal_plan_id)
    return {
        "status": "Success",
        "message": "Deleted Meal Plan Successfully!",
        "data": {"meal_plan_id": str(deleted_id)},
    }
