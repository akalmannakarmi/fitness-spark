from pymongo import AsyncMongoClient
from config import MONGO_URL, DATABASE_NAME

client = AsyncMongoClient(MONGO_URL)
database = client[DATABASE_NAME]

recipes_collection = database["recipes"]
meal_plans_collection = database["meal_plans"]
