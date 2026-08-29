from typing import Any

import pytest
from httpx import AsyncClient

from crud.users import delete_user
from tests.conftest import auth_headers, create_user


@pytest.mark.asyncio
async def test_signup_success(client: AsyncClient) -> None:
    resp = await client.post(
        "/auth/signup",
        json={"username": "alice", "email": "alice@example.com", "password": "s3cret"},
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["token_type"] == "bearer"
    assert body["admin"] is False
    assert body["access_token"]
    assert body["expires_at"] > 0


@pytest.mark.asyncio
async def test_signup_duplicate_username(client: AsyncClient) -> None:
    payload = {"username": "alice", "email": "alice@example.com", "password": "s3cret"}
    first = await client.post("/auth/signup", json=payload)
    assert first.status_code == 200

    resp = await client.post("/auth/signup", json=payload)
    assert resp.status_code == 400
    body: dict[str, Any] = resp.json()
    assert body["error"] == "User Exists"


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    await create_user("bob", password="hunter2")
    resp = await client.post(
        "/auth/login", json={"username": "bob", "password": "hunter2"}
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["token_type"] == "bearer"
    assert body["admin"] is False
    assert body["access_token"]


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    await create_user("bob", password="hunter2")
    resp = await client.post(
        "/auth/login", json={"username": "bob", "password": "wrong"}
    )
    assert resp.status_code == 401
    body: dict[str, Any] = resp.json()
    assert body["error"] == "Invalid Credentials"


@pytest.mark.asyncio
async def test_login_unknown_user(client: AsyncClient) -> None:
    resp = await client.post(
        "/auth/login", json={"username": "ghost", "password": "whatever"}
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_with_token(client: AsyncClient) -> None:
    user_id = await create_user("carol")
    headers = auth_headers(user_id)
    resp = await client.get("/auth/users/me", headers=headers)
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["username"] == "carol"
    assert body["email"] == "carol@example.com"
    assert body["groups"] == ["user"]


@pytest.mark.asyncio
async def test_me_without_token(client: AsyncClient) -> None:
    resp = await client.get("/auth/users/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_invalid_token(client: AsyncClient) -> None:
    resp = await client.get(
        "/auth/users/me", headers={"Authorization": "Bearer not-a-real-token"}
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_deleted_user_returns_401(client: AsyncClient) -> None:
    user_id = await create_user("dave")
    headers = auth_headers(user_id)

    await delete_user(user_id)
    resp = await client.get("/auth/users/me", headers=headers)
    assert resp.status_code == 401
