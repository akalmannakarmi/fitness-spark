import os
from collections.abc import AsyncIterator

os.environ["MONGO_URL"] = "mongodb://127.0.0.1:27017"
os.environ["DATABASE_NAME"] = "fitness_spark_test"
os.environ["SECRET_KEY"] = "test-secret-key-that-is-far-longer-than-thirty-two-bytes"

import pytest_asyncio  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402


async def create_user(
    username: str, password: str = "password", groups: list[str] | None = None
) -> str:
    from database import users_collection
    from security import hash_password

    result = await users_collection.insert_one(
        {
            "username": username,
            "email": f"{username}@example.com",
            "password": hash_password(password),
            "groups": groups or ["user"],
        }
    )
    return str(result.inserted_id)


def auth_headers(user_id: str) -> dict[str, str]:
    from security import create_access_token

    token, _ = create_access_token(user_id)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(autouse=True, loop_scope="session")
async def clean_db() -> AsyncIterator[None]:
    from database import (
        meal_plans_collection,
        recipes_collection,
        stats_collection,
        users_collection,
    )

    collections = [
        users_collection,
        recipes_collection,
        meal_plans_collection,
        stats_collection,
    ]
    for collection in collections:
        await collection.drop()
    yield
    for collection in collections:
        await collection.drop()


@pytest_asyncio.fixture(loop_scope="session")
async def client() -> AsyncIterator[AsyncClient]:
    from app import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c


@pytest_asyncio.fixture(loop_scope="session")
async def admin_headers() -> dict[str, str]:
    user_id = await create_user("admin", "adminpass", ["admin"])
    return auth_headers(user_id)


@pytest_asyncio.fixture(loop_scope="session")
async def user_headers() -> dict[str, str]:
    user_id = await create_user("regularuser")
    return auth_headers(user_id)
