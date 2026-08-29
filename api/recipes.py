from typing import Any

from fastapi import APIRouter, Depends

from config import Actions, Models
from crud.recipes import db_get_recipe, db_get_recipes, db_list_recipes
from crud.stats import update_stats
from deps import get_current_user
from schemas.common import MongoObjectId, num_pages
from schemas.recipe import RecipeFilter, RecipeListOut, RecipeOut, RecipesOut
from schemas.user import User

router = APIRouter()


@router.get("/list/recipes", response_model=RecipeListOut)
@update_stats(Models.Recipe, Actions.Read)
async def list_recipes(_: User = Depends(get_current_user)) -> dict[str, Any]:
    recipes = await db_list_recipes()
    return {"recipes": recipes}


@router.get("/get/recipes", response_model=RecipesOut)
@update_stats(Models.Recipe, Actions.Read)
async def get_recipes(
    filters: RecipeFilter = Depends(),
    _: User = Depends(get_current_user),
) -> dict[str, Any]:
    recipes, total = await db_get_recipes(filters)

    return {
        "recipes": recipes,
        "page": filters.page,
        "limit": filters.limit,
        "total": total,
        "pages": num_pages(total, filters.limit),
    }


@router.get("/get/recipe/{recipe_id}", response_model=RecipeOut)
@update_stats(Models.Recipe, Actions.Read)
async def get_recipe(
    recipe_id: MongoObjectId, _: User = Depends(get_current_user)
) -> dict[str, Any]:
    return await db_get_recipe(recipe_id)
