from typing import Any

import pytest
from httpx import AsyncClient

RECIPE_PAYLOAD: dict[str, Any] = {
    "image": "https://example.com/recipe.jpg",
    "title": "Test Recipe",
    "readyInMinutes": 10,
    "servings": 2,
    "vegetarian": True,
    "vegan": False,
    "glutenFree": True,
    "dairyFree": False,
    "cheap": True,
    "nutrients": [{"name": "Calories", "amount": 100, "unit": "kcal"}],
    "ingredients": [{"name": "flour", "amount": 1, "unit": "cup"}],
    "steps": ["Mix", "Bake"],
}


async def create_recipe(client: AsyncClient, headers: dict[str, str]) -> str:
    resp = await client.post(
        "/api/v1/admin/create/recipe", headers=headers, json=RECIPE_PAYLOAD
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    return str(body["data"]["recipe_id"])


@pytest.mark.asyncio
async def test_list_recipes_requires_auth(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    await create_recipe(client, admin_headers)
    resp = await client.get("/api/v1/recipe/list/recipes", headers=admin_headers)
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert len(body["recipes"]) == 1
    assert body["recipes"][0]["title"] == "Test Recipe"


@pytest.mark.asyncio
async def test_list_recipes_requires_auth_401(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/recipe/list/recipes")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_recipes_filters(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    await create_recipe(client, admin_headers)
    resp = await client.get(
        "/api/v1/recipe/get/recipes",
        headers=admin_headers,
        params={"search": "test", "cheap": "true"},
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["total"] == 1
    assert body["recipes"][0]["title"] == "Test Recipe"


@pytest.mark.asyncio
async def test_get_recipe_by_id(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    recipe_id = await create_recipe(client, admin_headers)
    resp = await client.get(
        f"/api/v1/recipe/get/recipe/{recipe_id}", headers=admin_headers
    )
    assert resp.status_code == 200
    body: dict[str, Any] = resp.json()
    assert body["title"] == "Test Recipe"
    assert body["cheap"] is True


@pytest.mark.asyncio
async def test_get_recipe_not_found(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    from bson import ObjectId

    resp = await client.get(
        f"/api/v1/recipe/get/recipe/{ObjectId()}", headers=admin_headers
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_recipe(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    recipe_id = await create_recipe(client, admin_headers)
    resp = await client.patch(
        f"/api/v1/admin/update/recipe/{recipe_id}",
        headers=admin_headers,
        json={"title": "Updated Title"},
    )
    assert resp.status_code == 200

    get = await client.get(
        f"/api/v1/recipe/get/recipe/{recipe_id}", headers=admin_headers
    )
    assert get.json()["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_recipe(
    client: AsyncClient, admin_headers: dict[str, str]
) -> None:
    recipe_id = await create_recipe(client, admin_headers)
    resp = await client.delete(
        f"/api/v1/admin/delete/recipe/{recipe_id}", headers=admin_headers
    )
    assert resp.status_code == 200

    get = await client.get(
        f"/api/v1/recipe/get/recipe/{recipe_id}", headers=admin_headers
    )
    assert get.status_code == 404


@pytest.mark.asyncio
async def test_recipe_admin_forbidden_for_regular_user(
    client: AsyncClient, user_headers: dict[str, str]
) -> None:
    resp = await client.post(
        "/api/v1/admin/create/recipe", headers=user_headers, json=RECIPE_PAYLOAD
    )
    assert resp.status_code == 403
