from .schemas import RecipeCreate,RecipeUpdate,MealPlanCreate,MealPlanUpdate
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

async def db_get_recipes() -> str:
    result = recipes_collection.find({})
    return await result.to_list()

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

async def db_get_meal_plans() -> list:
    result = meal_plans_collection.find({})
    return await result.to_list()

async def db_get_meal_plan(id:str) -> str:
    result = await meal_plans_collection.find_one({"_id":ObjectId(id)})
    if not result:
        raise CustomAPIException(status_code=404, error="Not Found", message="Meal Plan not found")
    return result


async def db_get_public_meal_plans() -> list:
    result = meal_plans_collection.find({"private":False})
    return await result.to_list()

async def db_get_user_meal_plans(user_id:ObjectId) -> list:
    result = meal_plans_collection.find({"user":user_id})
    return await result.to_list()

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