from .database import stats_collection,database
from config import Models, Actions
from bson import ObjectId


async def db_update_stats(model: Models, action: Actions, status_code: int, now: int, start_time: float, end_time: float):
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")
    await stats_collection.update_one(
        {"model": model},
        {
            "$inc": {
                f"logs.{now}.{action}": 1,
                f"logs.{now}.{action}_time": elapsed_time,
                f"logs.{now}.status_codes.{status_code}": 1,
            }
        },
        upsert=True,
    )

async def db_get_models():
    cursor = stats_collection.find({}, {"_id": 1, "model": 1})
    results = []
    async for document in cursor:
        count = await database[document["model"]].count_documents(filter={})
        results.append({"_id":str(document["_id"]),"model":document["model"],"count":count})
    return results

async def db_get_model(id:str):
    model = await stats_collection.find_one({"_id":ObjectId(id)})
    model["count"] = await database[model["model"]].count_documents({})
    return model

