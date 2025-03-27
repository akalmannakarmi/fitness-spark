import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import httpx
import pytest
import uuid
import time
import asyncio

from config import BASE_URL,AUTH_PREFIX

@pytest.mark.asyncio
async def test_Simple_Get_Users():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        response = await client.post("/login",json={
            "username":"admin",
            "password":"admin",
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        access_token = data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get("/admin/get/users/",headers=headers)

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_unauthorized():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"
        password = f"password"

        response = await client.post("/signup",json={
            "username":username,
            "email":email,
            "password":password,
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        access_token = data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.get("/admin/get/users/",headers=headers)

        assert response.status_code == 403

@pytest.mark.asyncio
async def test_Stress_Test():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        response = await client.post("/login",json={
            "username":"admin",
            "password":"admin",
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        access_token = data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}

        async def create_user_and_login(headers):
            response = await client.get("/admin/get/users/",headers=headers)

            assert response.status_code == 200

        # Create a list of tasks to run in parallel
        tasks = [create_user_and_login(headers) for _ in range(10)]

        start_time = time.time()

        # Run all tasks in parallel
        await asyncio.gather(*tasks)

        end_time = time.time()
        print(f"[Completed in {end_time - start_time:.2f} secs.]",end=" ")

