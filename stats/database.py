from pymongo import AsyncMongoClient
from config import MONGO_URL, DATABASE_NAME

client = AsyncMongoClient(MONGO_URL)
database = client[DATABASE_NAME]

stats_collection = database["statistics"]
