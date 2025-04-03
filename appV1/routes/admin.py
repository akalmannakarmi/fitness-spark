from fastapi import APIRouter,Depends
from ..schemas import SuccessResponse,RecipesOut,RecipeOut,RecipeCreate,RecipeUpdate
from ..schemas import MealPlansOut,MealPlanOut,MealPlanCreate,MealPlanUpdate
from ..crud import db_get_recipes,db_get_recipe,db_create_recipe,db_update_recipe,db_delete_recipe
from ..crud import db_get_meal_plans,db_get_meal_plan,db_create_meal_plan,db_update_meal_plan,db_delete_meal_plan
from auth.wraper import User,admin_user

router = APIRouter()

@router.get("/get/recipes",response_model=RecipesOut)
async def get_recipes(_:User=Depends(admin_user)):
    recipes = await db_get_recipes()
    return {"recipes":recipes}

@router.get("/get/recipe/{id}", response_model=RecipeOut)
async def get_recipe(id,_:User=Depends(admin_user)):
    return await db_get_recipe(id)

@router.post("/create/recipe", response_model=SuccessResponse)
async def create_recipe(form:RecipeCreate, _:User=Depends(admin_user)):
    recipe_id = await db_create_recipe(form)
    return {"status": "Success", "message": "Created Recipe Successfully!", "data":{"recipe_id":str(recipe_id)}}

@router.patch("/update/recipe/{id}", response_model=SuccessResponse)
async def update_recipe(id:str,form:RecipeUpdate, _:User=Depends(admin_user)):
    recipe_id = await db_update_recipe(id,form)
    return {"status": "Success", "message": "Updated Recipe Successfully!", "data":{"recipe_id":str(recipe_id)}}

@router.delete("/delete/recipe/{id}", response_model=SuccessResponse)
async def delete_recipe(id:str, _:User=Depends(admin_user)):
    recipe_id = await db_delete_recipe(id)
    return {"status": "Success", "message": "Deleted Recipe Successfully!", "data":{"recipe_id":str(recipe_id)}}


@router.get("/get/meal_plans",response_model=MealPlansOut)
async def get_meal_plans(_:User=Depends(admin_user)):
    meal_plans = await db_get_meal_plans()
    return {"meal_plans":meal_plans}

@router.get("/get/meal_plan/{id}", response_model=MealPlanOut)
async def get_meal_pan(id, _:User=Depends(admin_user)):
    return await db_get_meal_plan(id)

@router.post("/create/meal_plan", response_model=SuccessResponse)
async def create_meal_plan(form:MealPlanCreate, user:User=Depends(admin_user)):
    meal_plan_id = await db_create_meal_plan(str(user._id),form)
    return {"status": "Success", "message": "Created Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}

@router.patch("/update/meal_plan/{id}", response_model=SuccessResponse)
async def update_meal_plan(id:str,form:MealPlanUpdate, _:User=Depends(admin_user)):
    meal_plan_id = await db_update_meal_plan(id,form)
    return {"status": "Success", "message": "Updated Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}

@router.delete("/delete/meal_plan/{id}", response_model=SuccessResponse)
async def delete_meal_plan(id:str, _:User=Depends(admin_user)):
    meal_plan_id = await db_delete_meal_plan(id)
    return {"status": "Success", "message": "Deleted Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}