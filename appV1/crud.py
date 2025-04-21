from .schemas import RecipeCreate,RecipeUpdate,MealPlanCreate,MealPlanUpdate,RecipeFilter,MealPlanFilter
from .database import recipes_collection,meal_plans_collection
from bson import ObjectId
from utils.exception import CustomAPIException


async def db_create_recipe(recipe: RecipeCreate) -> str:
    result = await recipes_collection.insert_one(recipe.model_dump())
    return str(result.inserted_id)

async def db_update_recipe(id:str,recipe: RecipeUpdate) -> str:
    update_data = {k: v for k, v in recipe.model_dump().items() if v is not None}

    if not update_data:
        raise CustomAPIException(status_code=400, error="No Field", message="No valid fields to update")

    result = await recipes_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise CustomAPIException(status_code=404, error="Not Found", message="Recipe not found")
    return id

async def db_delete_recipe(id: str) -> str:
    result = await recipes_collection.delete_one({"_id":ObjectId(id)})

    if result.deleted_count == 0:
        raise CustomAPIException(status_code=404, error="Not Found", message="Recipe not found")
    return id

async def db_get_recipes(filters: RecipeFilter):
    query = {}

    # Text search
    if filters.search:
        query["$or"] = [
            {"title": {"$regex": filters.search, "$options": "i"}},
            {"description": {"$regex": filters.search, "$options": "i"}}
        ]

    # Boolean filters
    for field in ["vegetarian", "vegan", "glutenFree", "dairyFree", "cheep"]:
        val = getattr(filters, field)
        if val is not None:
            query[field] = val

    # Time range
    if filters.min_readyInMinutes or filters.max_readyInMinutes:
        query["readyInMinutes"] = {}
        if filters.min_readyInMinutes:
            query["readyInMinutes"]["$gte"] = filters.min_readyInMinutes
        if filters.max_readyInMinutes:
            query["readyInMinutes"]["$lte"] = filters.max_readyInMinutes

    # Ingredient filters
    if filters.include_ingredients:
        query["ingredients.name"] = {"$in": filters.include_ingredients}
    if filters.exclude_ingredients:
        query["ingredients.name"] = {"$nin": filters.exclude_ingredients}

    # Nutrient filters
    if filters.nutrients:
        for name, bounds in filters.nutrients.items():
            nutrient_filter = {
                "nutrients": {
                    "$elemMatch": {
                        "name": name,
                        **({ "$gte": bounds["min"] } if "min" in bounds else {}),
                        **({ "$lte": bounds["max"] } if "max" in bounds else {})
                    }
                }
            }
            query.update(nutrient_filter)

    # Fetch results
    total = await recipes_collection.count_documents(query)

    cursor = (
        recipes_collection
        .find(query)
        .skip(filters.skip)
        .limit(filters.limit)
    )

    recipes = await cursor.to_list(length=filters.limit)
    return recipes, total

async def db_get_recipe(id:str) -> str:
    result = await recipes_collection.find_one({"_id":ObjectId(id)})
    if not result:
        raise CustomAPIException(status_code=404, error="Not Found", message="Recipe not found")
    return result



async def db_create_meal_plan(user_id:ObjectId,meal_plan: MealPlanCreate) -> str:
    meal_plan = meal_plan.model_dump()
    meal_plan["user"] = user_id
    result = await meal_plans_collection.insert_one(meal_plan)
    return str(result.inserted_id)

async def db_update_meal_plan(id:str,meal_plan: MealPlanUpdate) -> str:
    update_data = {k: v for k, v in meal_plan.model_dump().items() if v is not None}

    if not update_data:
        raise CustomAPIException(status_code=400, error="No Field", message="No valid fields to update")

    result = await meal_plans_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise CustomAPIException(status_code=404, error="Not Found", message="Meal Plan not found")
    return id

async def db_delete_meal_plan(id: str) -> str:
    result = await meal_plans_collection.delete_one({"_id":ObjectId(id)})

    if result.deleted_count == 0:
        raise CustomAPIException(status_code=404, error="Not Found", message="Meal Plan not found")
    return id

async def db_get_meal_plan(id:str) -> str:
    result = await meal_plans_collection.find_one({"_id":ObjectId(id)})
    if not result:
        raise CustomAPIException(status_code=404, error="Not Found", message="Meal Plan not found")
    return result


def build_meal_plan_query(filters: MealPlanFilter):
    query = {}

    if filters.recipe_ids:
        query["dailyPlans.recipes"] = {"$in": filters.recipe_ids}

    if filters.search:
        query["$or"] = [
            {"title": {"$regex": filters.search, "$options": "i"}},
            {"description": {"$regex": filters.search, "$options": "i"}},
        ]

    return query

async def db_get_public_meal_plans(filters: MealPlanFilter):
    query = build_meal_plan_query(filters)
    query["private"] = False

    total = await meal_plans_collection.count_documents(query)
    cursor = (
        meal_plans_collection
        .find(query)
        .skip(filters.skip)
        .limit(filters.limit)
    )
    meal_plans = await cursor.to_list(length=filters.limit)
    return meal_plans, total


async def db_get_user_meal_plans(user_id: ObjectId, filters: MealPlanFilter):
    query = build_meal_plan_query(filters)
    query["user"] = user_id

    total = await meal_plans_collection.count_documents(query)
    cursor = (
        meal_plans_collection
        .find(query)
        .skip(filters.skip)
        .limit(filters.limit)
    )
    meal_plans = await cursor.to_list(length=filters.limit)
    return meal_plans, total


async def db_get_meal_plans(filters: MealPlanFilter):
    query = build_meal_plan_query(filters)

    total = await meal_plans_collection.count_documents(query)
    cursor = (
        meal_plans_collection
        .find(query)
        .skip(filters.skip)
        .limit(filters.limit)
    )
    meal_plans = await cursor.to_list(length=filters.limit)
    return meal_plans, total


async def db_get_user_meal_plan(id:str,user_id:ObjectId) -> str:
    result = await meal_plans_collection.find_one({"_id":ObjectId(id),"user":user_id})
    if not result:
        raise CustomAPIException(status_code=404, error="Not Found", message="Meal Plan not found")
    return result

async def db_update_user_meal_plan(id:str,user_id:ObjectId,meal_plan: MealPlanUpdate) -> str:
    update_data = {k: v for k, v in meal_plan.model_dump().items() if v is not None}

    if not update_data:
        raise CustomAPIException(status_code=400, error="No Field", message="No valid fields to update")

    result = await meal_plans_collection.update_one({"_id": ObjectId(id),"user":user_id}, {"$set": update_data})

    if result.matched_count == 0:
        raise CustomAPIException(status_code=404, error="Not Found", message="Meal Plan not found")
    return id

async def db_delete_user_meal_plan(id: str,user_id:ObjectId) -> str:
    result = await meal_plans_collection.delete_one({"_id":ObjectId(id),"user":user_id})

    if result.deleted_count == 0:
        raise CustomAPIException(status_code=404, error="Not Found", message="Meal Plan not found")
    return id