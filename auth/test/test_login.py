import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import uuid

import httpx
import pytest

from config import AUTH_PREFIX, BASE_URL


@pytest.mark.asyncio
async def test_simple_login():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": "test1@gmail.com",
                "password": "password",
            },
        )

        response = await client.post(
            "/login", json={"username": username, "password": "password"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data


@pytest.mark.asyncio
async def test_invalid_login():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": "test1@gmail.com",
                "password": "password",
            },
        )

        response = await client.post(
            "/login", json={"username": username, "password": "wrongpassword"}
        )

        assert response.status_code == 401

        response = await client.post(
            "/login", json={"username": "wrongusername", "password": "password"}
        )

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_missing_username():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": "test1@gmail.com",
                "password": "password",
            },
        )

        response = await client.post("/login", json={"password": "password"})

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_password():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": "test1@gmail.com",
                "password": "password",
            },
        )

        response = await client.post("/login", json={"username": username})

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_fields():
    async with httpx.AsyncClient(base_url=f"{BASE_URL}{AUTH_PREFIX}") as client:
        username = str(uuid.uuid4())

        response = await client.post(
            "/signup",
            json={
                "username": username,
                "email": "test1@gmail.com",
                "password": "password",
            },
        )

        response = await client.post("/login")

        assert response.status_code == 422
