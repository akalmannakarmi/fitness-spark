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


async def db_update_meal_plan(meal_plan_id: str, meal_plan: MealPlanUpdate) -> str:
    update_data = {k: v for k, v in meal_plan.model_dump().items() if v is not None}

    if not update_data:
        raise CustomAPIException(
            status_code=400, error="No Field", message="No valid fields to update"
        )

    result = await meal_plans_collection.update_one(
        {"_id": ObjectId(meal_plan_id)}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return meal_plan_id


async def db_delete_meal_plan(meal_plan_id: str) -> str:
    result = await meal_plans_collection.delete_one({"_id": ObjectId(meal_plan_id)})

    if result.deleted_count == 0:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return meal_plan_id


async def db_get_meal_plan(meal_plan_id: str) -> dict[str, Any]:
    result: dict[str, Any] | None = await meal_plans_collection.find_one(
        {"_id": ObjectId(meal_plan_id)}
    )
    if not result:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return result


def build_meal_plan_query(filters: MealPlanFilter) -> dict[str, Any]:
    query: dict[str, Any] = {}

    if filters.recipe_ids:
        query["dailyPlans.recipes"] = {"$in": filters.recipe_ids}

    if filters.search:
        query["$or"] = [
            {"title": {"$regex": filters.search, "$options": "i"}},
            {"description": {"$regex": filters.search, "$options": "i"}},
        ]

    return query


async def db_get_public_meal_plans(
    filters: MealPlanFilter,
) -> tuple[list[dict[str, Any]], int]:
    query = build_meal_plan_query(filters)
    query["private"] = False

    total = await meal_plans_collection.count_documents(query)
    cursor = meal_plans_collection.find(query).skip(filters.skip).limit(filters.limit)
    meal_plans = await cursor.to_list(length=filters.limit)
    return meal_plans, total


async def db_get_user_meal_plans(
    user_id: ObjectId, filters: MealPlanFilter
) -> tuple[list[dict[str, Any]], int]:
    query = build_meal_plan_query(filters)
    query["user"] = user_id

    total = await meal_plans_collection.count_documents(query)
    cursor = meal_plans_collection.find(query).skip(filters.skip).limit(filters.limit)
    meal_plans = await cursor.to_list(length=filters.limit)
    return meal_plans, total


async def db_get_meal_plans(
    filters: MealPlanFilter,
) -> tuple[list[dict[str, Any]], int]:
    query = build_meal_plan_query(filters)

    total = await meal_plans_collection.count_documents(query)
    cursor = meal_plans_collection.find(query).skip(filters.skip).limit(filters.limit)
    meal_plans = await cursor.to_list(length=filters.limit)
    return meal_plans, total


async def db_get_user_meal_plan(meal_plan_id: str, user_id: ObjectId) -> dict[str, Any]:
    result: dict[str, Any] | None = await meal_plans_collection.find_one(
        {"_id": ObjectId(meal_plan_id), "user": user_id}
    )
    if not result:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return result


async def db_update_user_meal_plan(
    meal_plan_id: str, user_id: ObjectId, meal_plan: MealPlanUpdate
) -> str:
    update_data = {k: v for k, v in meal_plan.model_dump().items() if v is not None}

    if not update_data:
        raise CustomAPIException(
            status_code=400, error="No Field", message="No valid fields to update"
        )

    result = await meal_plans_collection.update_one(
        {"_id": ObjectId(meal_plan_id), "user": user_id}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return meal_plan_id


async def db_delete_user_meal_plan(meal_plan_id: str, user_id: ObjectId) -> str:
    result = await meal_plans_collection.delete_one(
        {"_id": ObjectId(meal_plan_id), "user": user_id}
    )

    if result.deleted_count == 0:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Meal Plan not found"
        )
    return meal_plan_id
