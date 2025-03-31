from .schemas import RecipeCreate,RecipeUpdate
from .database import recipes_collection,meal_plans_collection
from .models import Recipe,MealPlan
from bson import ObjectId
from utils.exception import CustomAPIException


async def create_recipe(recipe: RecipeCreate) -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)

async def update_recipe(recipe: RecipeUpdate) -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)

async def delete_recipe(id: str) -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)

async def get_recipes() -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)

async def get_recipe(id:str) -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)


async def create_meal_plan(recipe: RecipeCreate) -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)

async def update_meal_plan(recipe: RecipeUpdate) -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)

async def delete_meal_plan(id: str) -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)

async def get_meal_plans() -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)

async def get_meal_plan(id:str) -> str:
    result = await recipes_collection.insert_one({})
    return str(result.inserted_id)