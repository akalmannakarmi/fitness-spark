from typing import Any

import pytest
from httpx import AsyncClient

from tests.conftest import create_user


async def create_admin_user(client: AsyncClient, headers: dict[str, str]) -> str:
    resp = await client.post(
        "/auth/admin/create/user",
        headers=headers,
        json={
            "username": "managed",
            "email": "managed@example.com",
            "password": "pw123",
            "groups": ["user"],
        },
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    return str(body["data"]["user_id"])


@pytest.mark.asyncio
async def test_create_user_success(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    user_id = await create_admin_user(client, admin_headers)
    assert user_id


@pytest.mark.asyncio
async def test_create_user_duplicate_username(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    await create_admin_user(client, admin_headers)
    resp = await client.post(
        "/auth/admin/create/user",
        headers=admin_headers,
        json={
            "username": "managed",
            "email": "other@example.com",
            "password": "pw123",
            "groups": ["user"],
        },
    )
    assert resp.status_code == 400
    body: dict[str, Any] = resp.json()
    assert body["error"] == "User Exists"


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient, admin_headers: dict[str, str]) -> None:
    resp = await client.get("/auth/admin/list/users/", headers=admin_headers)
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert isinstance(body["users"], list)


@pytest.mark.asyncio
async def test_get_users_search_pagination(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    await create_user("findme", groups=["user"])
    resp = await client.get(
        "/auth/admin/get/users/",
        headers=admin_headers,
        params={"search": "find", "page": 1, "limit": 10},
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["total"] == 1
    assert body["pages"] == 1
    assert any(u["username"] == "findme" for u in body["users"])


@pytest.mark.asyncio
async def test_get_user_by_id(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    user_id = await create_user("target")
    resp = await client.get(f"/auth/admin/get/user/{user_id}", headers=admin_headers)
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["username"] == "target"


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, admin_headers: dict[str, str]) -> None:
    user_id = await create_user("updatable")
    resp = await client.put(
        f"/auth/admin/update/user/{user_id}",
        headers=admin_headers,
        json={"username": "renamed"},
    )
    assert resp.status_code == 200

    get = await client.get(f"/auth/admin/get/user/{user_id}", headers=admin_headers)
    assert get.json()["username"] == "renamed"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, admin_headers: dict[str, str]) -> None:
    user_id = await create_user("deletable")
    resp = await client.delete(
        f"/auth/admin/delete/user/{user_id}", headers=admin_headers
    )
    assert resp.status_code == 200

    get = await client.get(f"/auth/admin/get/user/{user_id}", headers=admin_headers)
    assert get.status_code == 404


@pytest.mark.asyncio
async def test_missing_user_returns_404(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    from bson import ObjectId

    missing_id = str(ObjectId())
    resp = await client.get(f"/auth/admin/get/user/{missing_id}", headers=admin_headers)
    assert resp.status_code == 404

    update = await client.put(
        f"/auth/admin/update/user/{missing_id}",
        headers=admin_headers,
        json={"email": "x@example.com"},
    )
    assert update.status_code == 404

    delete = await client.delete(
        f"/auth/admin/delete/user/{missing_id}", headers=admin_headers
    )
    assert delete.status_code == 404


@pytest.mark.asyncio
async def test_invalid_object_id_returns_404(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    resp = await client.get(
        "/auth/admin/get/user/not-an-objectid", headers=admin_headers
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_requires_admin_token(client: AsyncClient) -> None:
    resp = await client.get("/auth/admin/list/users/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_forbidden_for_regular_user(
    client: AsyncClient, user_headers: dict[str, str]
) -> None:
    resp = await client.get("/auth/admin/list/users/", headers=user_headers)
    assert resp.status_code == 403
