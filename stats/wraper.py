import asyncio
import functools
import time

from fastapi import HTTPException

from config import Actions, Models

from .crud import db_update_stats


def update_stats(model: Models, action: Actions):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            status_code = 500
            try:
                result = await func(*args, **kwargs)
                status_code = 200
            except HTTPException as e:
                status_code = e.status_code
                raise e
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
