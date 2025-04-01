from fastapi import APIRouter
from ..schemas import RecipesOut,RecipeOut
from ..crud import db_get_recipes,db_get_recipe

router = APIRouter()

@router.get("/get/recipes",response_model=RecipesOut)
async def get_recipes():
    recipes = await db_get_recipes()
    return {"recipes":recipes}

@router.get("/get/recipe/{id}",response_model=RecipeOut)
async def get_recipe(id):
    return await db_get_recipe(id)