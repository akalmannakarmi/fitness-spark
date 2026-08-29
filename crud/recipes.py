from typing import Any

from bson import ObjectId

from database import recipes_collection
from exceptions import CustomAPIException
from schemas.recipe import RecipeCreate, RecipeFilter, RecipeUpdate


async def db_list_recipes() -> list[dict[str, Any]]:
    cursor = recipes_collection.find({}, {"_id": 1, "title": 1})
    result = await cursor.to_list()
    return result


async def db_create_recipe(recipe: RecipeCreate) -> str:
    result = await recipes_collection.insert_one(recipe.model_dump())
    return str(result.inserted_id)


async def db_update_recipe(recipe_id: str, recipe: RecipeUpdate) -> str:
    update_data = {k: v for k, v in recipe.model_dump().items() if v is not None}

    if not update_data:
        raise CustomAPIException(
            status_code=400, error="No Field", message="No valid fields to update"
        )

    result = await recipes_collection.update_one(
        {"_id": ObjectId(recipe_id)}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Recipe not found"
        )
    return recipe_id


async def db_delete_recipe(recipe_id: str) -> str:
    result = await recipes_collection.delete_one({"_id": ObjectId(recipe_id)})

    if result.deleted_count == 0:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Recipe not found"
        )
    return recipe_id


async def db_get_recipes(filters: RecipeFilter) -> tuple[list[dict[str, Any]], int]:
    query: dict[str, Any] = {}

    # Text search
    if filters.search:
        query["$or"] = [
            {"title": {"$regex": filters.search, "$options": "i"}},
            {"description": {"$regex": filters.search, "$options": "i"}},
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
                        **({"$gte": bounds["min"]} if "min" in bounds else {}),
                        **({"$lte": bounds["max"]} if "max" in bounds else {}),
                    }
                }
            }
            query.update(nutrient_filter)

    # Fetch results
    total = await recipes_collection.count_documents(query)

    cursor = recipes_collection.find(query).skip(filters.skip).limit(filters.limit)

    recipes = await cursor.to_list(length=filters.limit)
    return recipes, total


async def db_get_recipe(recipe_id: str) -> dict[str, Any]:
    result: dict[str, Any] | None = await recipes_collection.find_one(
        {"_id": ObjectId(recipe_id)}
    )
    if not result:
        raise CustomAPIException(
            status_code=404, error="Not Found", message="Recipe not found"
        )
    return result
