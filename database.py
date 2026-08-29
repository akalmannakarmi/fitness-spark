from typing import Any

from pymongo import AsyncMongoClient

from config import DATABASE_NAME, MONGO_URL

client: AsyncMongoClient[dict[str, Any]] = AsyncMongoClient(MONGO_URL)
database = client[DATABASE_NAME]

users_collection = database["users"]
recipes_collection = database["recipes"]
meal_plans_collection = database["meal_plans"]
stats_collection = database["statistics"]
