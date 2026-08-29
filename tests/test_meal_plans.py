from typing import Any

import pytest
from httpx import AsyncClient

from tests.conftest import auth_headers, create_user

ONE_DAY = "2026-01-01T12:00:00"


def meal_plan_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": "Weekly Plan",
        "description": "A weekly meal plan",
        "summary": "Balanced",
        "private": False,
        "dailyPlans": [
            {
                "day": ONE_DAY,
                "recipes": {"breakfast": "recipe_1"},
                "summary": "Day one",
            }
        ],
    }
    payload.update(overrides)
    return payload


async def create_meal_plan(
    client: AsyncClient, headers: dict[str, str], **overrides: Any
) -> str:
    resp = await client.post(
        "/api/v1/meal_plan/create/meal_plan",
        headers=headers,
        json=meal_plan_payload(**overrides),
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    return str(body["data"]["meal_plan_id"])


@pytest.mark.asyncio
async def test_create_and_get_my_meal_plan(
    client: AsyncClient, user_headers: dict[str, str]
) -> None:
    plan_id = await create_meal_plan(client, user_headers)

    resp = await client.get(
        f"/api/v1/meal_plan/get/meal_plan/{plan_id}", headers=user_headers
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["title"] == "Weekly Plan"


@pytest.mark.asyncio
async def test_get_my_meal_plans(
    client: AsyncClient, user_headers: dict[str, str]
) -> None:
    await create_meal_plan(client, user_headers)
    resp = await client.get("/api/v1/meal_plan/get/my/meal_plans", headers=user_headers)
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["total"] == 1
    assert body["meal_plans"][0]["title"] == "Weekly Plan"


@pytest.mark.asyncio
async def test_public_meal_plans_list(
    client: AsyncClient, user_headers: dict[str, str]
) -> None:
    await create_meal_plan(client, user_headers)
    resp = await client.get("/api/v1/meal_plan/get/meal_plans")
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["total"] == 1


@pytest.mark.asyncio
async def test_meal_plan_scoped_to_owner(
    client: AsyncClient, user_headers: dict[str, str]
) -> None:
    plan_id = await create_meal_plan(client, user_headers)

    other_user_id = await create_user("otheruser")
    resp = await client.get(
        f"/api/v1/meal_plan/get/meal_plan/{plan_id}",
        headers=auth_headers(other_user_id),
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_meal_plan(
    client: AsyncClient, user_headers: dict[str, str]
) -> None:
    plan_id = await create_meal_plan(client, user_headers)
    resp = await client.patch(
        f"/api/v1/meal_plan/update/meal_plan/{plan_id}",
        headers=user_headers,
        json={"title": "Renamed Plan"},
    )
    assert resp.status_code == 200

    get = await client.get(
        f"/api/v1/meal_plan/get/meal_plan/{plan_id}", headers=user_headers
    )
    assert get.json()["title"] == "Renamed Plan"


@pytest.mark.asyncio
async def test_delete_meal_plan(
    client: AsyncClient, user_headers: dict[str, str]
) -> None:
    plan_id = await create_meal_plan(client, user_headers)
    resp = await client.delete(
        f"/api/v1/meal_plan/delete/meal_plan/{plan_id}", headers=user_headers
    )
    assert resp.status_code == 200

    get = await client.get(
        f"/api/v1/meal_plan/get/meal_plan/{plan_id}", headers=user_headers
    )
    assert get.status_code == 404


@pytest.mark.asyncio
async def test_created_meal_plan_requires_auth(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/meal_plan/create/meal_plan", json=meal_plan_payload()
    )
    assert resp.status_code == 401
