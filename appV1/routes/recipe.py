from fastapi import APIRouter,Depends
from ..schemas import RecipesOut,RecipeOut
from ..crud import db_get_recipes,db_get_recipe
from auth.wraper import User,auth_user

router = APIRouter()

@router.get("/get/recipes",response_model=RecipesOut)
async def get_recipes(_:User=Depends(auth_user)):
    recipes = await db_get_recipes()
    return {"recipes":recipes}

@router.get("/get/recipe/{id}",response_model=RecipeOut)
async def get_recipe(id,_:User=Depends(auth_user)):
    return await db_get_recipe(id)