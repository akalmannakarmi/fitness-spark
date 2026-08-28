from pymongo import AsyncMongoClient

from config import DATABASE_NAME, MONGO_URL

client = AsyncMongoClient(MONGO_URL)
database = client[DATABASE_NAME]

recipes_collection = database["recipes"]
meal_plans_collection = database["meal_plans"]
