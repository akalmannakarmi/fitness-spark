from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]

recipes_collection = database["recipes"]
meal_plans_collection = database["meal_plans"]
