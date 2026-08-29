import re
from typing import Any

from bson import ObjectId

from database import meal_plans_collection
from exceptions import CustomAPIException
from schemas.meal_plan import MealPlanCreate, MealPlanFilter, MealPlanUpdate


async def db_create_meal_plan(user_id: ObjectId, meal_plan: MealPlanCreate) -> str:
    data = meal_plan.model_dump()
    data["user"] = user_id
    result = await meal_plans_collection.insert_one(data)
    return str(result.inserted_id)


def build_meal_plan_query(
    filters: MealPlanFilter, user_id: ObjectId | None = None, public_only: bool = False
) -> dict[str, Any]:
    query: dict[str, Any] = {}

    if filters.recipe_ids:
        query["dailyPlans.recipes"] = {"$in": filters.recipe_ids}

    if filters.search:
        escaped = re.escape(filters.search)
        query["$or"] = [
            {"title": {"$regex": escaped, "$options": "i"}},
            {"description": {"$regex": escaped, "$options": "i"}},
        ]

    if user_id is not None:
        query["user"] = user_id

    if public_only:
        query["private"] = False

    return query


async def db_get_meal_plans(
    filters: MealPlanFilter,
    user_id: ObjectId | None = None,
    public_only: bool = False,
) -> tuple[list[dict[str, Any]], int]:
    query = build_meal_plan_query(filters, user_id=user_id, public_only=public_only)

    total = await meal_plans_collection.count_documents(query)
    cursor = meal_plans_collection.find(query).skip(filters.skip).limit(filters.limit)
    meal_plans = await cursor.to_list(length=filters.limit)
    return meal_plans, total


async def db_get_meal_plan(
    meal_plan_id: str, user_id: ObjectId | None = None
) -> dict[str, Any]:
    query: dict[str, Any] = {"_id": ObjectId(meal_plan_id)}
    if user_id is not None:
        query["user"] = user_id

    result: dict[str, Any] | None = await meal_plans_collection.find_one(query)
    if not result:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return result


async def db_update_meal_plan(
    meal_plan_id: str, meal_plan: MealPlanUpdate, user_id: ObjectId | None = None
) -> str:
    update_data = {k: v for k, v in meal_plan.model_dump().items() if v is not None}

    if not update_data:
        raise CustomAPIException(
            status_code=400, error="No Field", message="No valid fields to update"
        )

    query: dict[str, Any] = {"_id": ObjectId(meal_plan_id)}
    if user_id is not None:
        query["user"] = user_id

    result = await meal_plans_collection.update_one(query, {"$set": update_data})

    if result.matched_count == 0:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return meal_plan_id


async def db_delete_meal_plan(
    meal_plan_id: str, user_id: ObjectId | None = None
) -> str:
    query: dict[str, Any] = {"_id": ObjectId(meal_plan_id)}
    if user_id is not None:
        query["user"] = user_id

    result = await meal_plans_collection.delete_one(query)

    if result.deleted_count == 0:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return meal_plan_id
