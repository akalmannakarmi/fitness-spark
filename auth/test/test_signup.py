import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import uuid

import httpx
import pytest

from config import AUTH_PREFIX, BASE_URL


@pytest.mark.asyncio
async def test_simple_signup():
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


@pytest.mark.asyncio
async def test_user_already_exists():
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

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == 400


@pytest.mark.asyncio
async def test_missing_username():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"
        password = "password"

        response = await client.post(
            "/signup",
            json={
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_email():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        password = "password"

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "password": password,
            },
        )

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_password():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())
        email = f"{username}@test.com"

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": email,
            },
        )

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_fields():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        response = await client.post("/signup")

        assert response.status_code == 422
