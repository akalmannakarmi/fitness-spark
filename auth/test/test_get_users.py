import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import asyncio
import time
import uuid

import httpx
import pytest

from config import AUTH_PREFIX, BASE_URL


@pytest.mark.asyncio
async def test_simple_get_users():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        response = await client.post(
            "/login",
            json={
                "username": "admin",
                "password": "admin",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        access_token = data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get("/admin/get/users/", headers=headers)

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_unauthorized():
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

        response = await client.get("/admin/get/users/", headers=headers)

        assert response.status_code == 403


@pytest.mark.asyncio
async def test_stress_test():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        response = await client.post(
            "/login",
            json={
                "username": "admin",
                "password": "admin",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        access_token = data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}

        async def create_user_and_login(headers):
            response = await client.get("/admin/get/users/", headers=headers)

            assert response.status_code == 200

        # Create a list of tasks to run in parallel
        tasks = [create_user_and_login(headers) for _ in range(10)]

        start_time = time.time()

        # Run all tasks in parallel
        await asyncio.gather(*tasks)

        end_time = time.time()
        print(f"[Completed in {end_time - start_time:.2f} secs.]", end=" ")
