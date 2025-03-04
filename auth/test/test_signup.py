import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import httpx
import pytest
from config import BASE_URL,AUTH_PREFIX
import uuid


@pytest.mark.asyncio
async def test_Simple_signup():
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


@pytest.mark.asyncio
async def test_User_Already_Exists():
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

        response = await client.post("/signup",json={
            "username":username,
            "email":email,
            "password":password,
        })

        assert response.status_code == 400


@pytest.mark.asyncio
async def test_Missing_Username():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"
        password = f"password"

        response = await client.post("/signup",json={
            "email":email,
            "password":password,
        })

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_Missing_Email():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"
        password = f"password"

        response = await client.post("/signup",json={
            "username":username,
            "password":password,
        })

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_Missing_Password():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"
        password = f"password"

        response = await client.post("/signup",json={
            "username":username,
            "email":email,
        })

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_Missing_Fields():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"
        password = f"password"

        response = await client.post("/signup")

        assert response.status_code == 422