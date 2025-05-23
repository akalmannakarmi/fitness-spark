from fastapi import APIRouter,Depends
from ..schemas import RecipesOut,RecipeOut,RecipeFilter,RecipeListOut
from ..crud import db_get_recipes,db_get_recipe,db_list_recipes
from auth.wraper import User,auth_user
from stats.wraper import update_stats
from config import Models, Actions

router = APIRouter()

@router.get("/list/recipes", response_model=RecipeListOut)
@update_stats(Models.Recipe, Actions.Read)
async def list_recipes(_: User = Depends(auth_user)):
    recipes = await db_list_recipes()
    return {"recipes": recipes}


@router.get("/get/recipes",response_model=RecipesOut)
@update_stats(Models.Recipe, Actions.Read)
async def get_recipes(
    filters: RecipeFilter = Depends(),
    _: User = Depends(auth_user),
):
    recipes, total = await db_get_recipes(filters)

    return {
        "recipes": recipes,
        "page": filters.page,
        "limit": filters.limit,
        "total": total,
        "pages": (total + filters.limit - 1) // filters.limit
    }

@router.get("/get/recipe/{id}",response_model=RecipeOut)
@update_stats(Models.Recipe,Actions.Read)
async def get_recipe(id,_:User=Depends(auth_user)):
    return await db_get_recipe(id)