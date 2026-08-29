import asyncio
import functools
import time
from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeVar

from bson import ObjectId
from fastapi import HTTPException

from config import Actions, Models
from database import database, stats_collection

P = ParamSpec("P")
R = TypeVar("R")


def update_stats(
    model: Models, action: Actions
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    def decorator(
        func: Callable[P, Awaitable[R]],
    ) -> Callable[P, Awaitable[R]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.perf_counter()
            status_code = 500
            try:
                result = await func(*args, **kwargs)
            except HTTPException as e:
                status_code = e.status_code
                raise
            finally:
                end_time = time.perf_counter()
                now = int(time.time() // 60)
                asyncio.create_task(
                    db_update_stats(
                        model, action, status_code, now, start_time, end_time
                    )
                )
            return result

        return wrapper

    return decorator


async def db_update_stats(
    model: Models,
    action: Actions,
    status_code: int,
    now: int,
    start_time: float,
    end_time: float,
) -> None:
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


async def db_get_models() -> list[dict[str, Any]]:
    cursor = stats_collection.find({}, {"_id": 1, "model": 1})
    results: list[dict[str, Any]] = []
    async for document in cursor:
        count = await database[document["model"]].count_documents(filter={})
        results.append(
            {"_id": str(document["_id"]), "model": document["model"], "count": count}
        )
    return results


async def db_get_model(model_id: str) -> dict[str, Any] | None:
    model: dict[str, Any] | None = await stats_collection.find_one(
        {"_id": ObjectId(model_id)}
    )
    if model is None:
        return None
    model["count"] = await database[model["model"]].count_documents({})
    return model
