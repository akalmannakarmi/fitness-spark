from pymongo import AsyncMongoClient

from config import DATABASE_NAME, MONGO_URL

client = AsyncMongoClient(MONGO_URL)
database = client[DATABASE_NAME]

users_collection = database["users"]
