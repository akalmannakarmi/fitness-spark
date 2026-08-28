import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import asyncio
import time
import uuid
from datetime import UTC, datetime, timedelta

import httpx
import pytest

from config import AUTH_PREFIX, BASE_URL


@pytest.mark.asyncio
async def test_simple_get_user():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"
        password = "password"

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        access_token = data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 200
        data = response.json()

        assert "username" in data
        assert username == data["username"]
        assert "email" in data
        assert email == data["email"]

        response = await client.get("/users/me", params={"token": access_token})

        assert response.status_code == 200
        data = response.json()

        assert "username" in data
        assert username == data["username"]
        assert "email" in data
        assert email == data["email"]


@pytest.mark.asyncio
async def test_expired_token():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"
        password = "password"
        expires_at = (datetime.now(UTC) - timedelta(seconds=1)).timestamp()

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": email,
                "password": password,
                "expires_at": expires_at,
            },
        )

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        access_token = data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/users/me", headers=headers)

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_missing_token():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        response = await client.get("/users/me")

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_stress_test():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:

        async def signup_and_get_user():
            username = str(uuid.uuid4())
            email = f"{username}@test.com"
            password = "password"

            signup_response = await client.post(
                "/signup",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                },
            )

            assert signup_response.status_code == 200
            signup_data = signup_response.json()

            assert "access_token" in signup_data
            access_token = signup_data["access_token"]

            headers = {"Authorization": f"Bearer {access_token}"}

            get_user_response = await client.get("/users/me", headers=headers)

            assert get_user_response.status_code == 200
            get_user_data = get_user_response.json()

            assert "username" in get_user_data
            assert username == get_user_data["username"]
            assert "email" in get_user_data
            assert email == get_user_data["email"]

        # Create a list of tasks to run in parallel
        tasks = [signup_and_get_user() for _ in range(10)]

        start_time = time.time()

        # Run all tasks in parallel
        await asyncio.gather(*tasks)

        end_time = time.time()
        print(f"[Completed in {end_time - start_time:.2f} secs.]", end=" ")
