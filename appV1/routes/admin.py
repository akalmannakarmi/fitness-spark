from fastapi import APIRouter,Depends
from ..schemas import SuccessResponse,RecipesOut,RecipeOut,RecipeCreate,RecipeUpdate,RecipeFilter
from ..schemas import MealPlansOut,MealPlanOut,MealPlanCreate,MealPlanUpdate,MealPlanFilter
from ..crud import db_get_recipes,db_get_recipe,db_create_recipe,db_update_recipe,db_delete_recipe
from ..crud import db_get_meal_plans,db_get_meal_plan,db_create_meal_plan,db_update_meal_plan,db_delete_meal_plan
from auth.wraper import User,admin_user
from stats.wraper import update_stats
from config import Models,Actions

router = APIRouter()

@router.get("/get/recipes",response_model=RecipesOut)
@update_stats(Models.Recipe,Actions.Read)
async def get_recipes(
    filters: RecipeFilter = Depends(),
    _: User = Depends(admin_user),
):
    recipes, total = await db_get_recipes(filters)

    return {
        "recipes": recipes,
        "page": filters.page,
        "limit": filters.limit,
        "total": total,
        "pages": (total + filters.limit - 1) // filters.limit
    }

@router.get("/get/recipe/{id}", response_model=RecipeOut)
@update_stats(Models.Recipe,Actions.Read)
async def get_recipe(id,_:User=Depends(admin_user)):
    return await db_get_recipe(id)

@router.post("/create/recipe", response_model=SuccessResponse)
@update_stats(Models.Recipe,Actions.Create)
async def create_recipe(form:RecipeCreate, _:User=Depends(admin_user)):
    recipe_id = await db_create_recipe(form)
    return {"status": "Success", "message": "Created Recipe Successfully!", "data":{"recipe_id":str(recipe_id)}}

@router.patch("/update/recipe/{id}", response_model=SuccessResponse)
@update_stats(Models.Recipe,Actions.Update)
async def update_recipe(id:str,form:RecipeUpdate, _:User=Depends(admin_user)):
    recipe_id = await db_update_recipe(id,form)
    return {"status": "Success", "message": "Updated Recipe Successfully!", "data":{"recipe_id":str(recipe_id)}}

@router.delete("/delete/recipe/{id}", response_model=SuccessResponse)
@update_stats(Models.Recipe,Actions.Delete)
async def delete_recipe(id:str, _:User=Depends(admin_user)):
    recipe_id = await db_delete_recipe(id)
    return {"status": "Success", "message": "Deleted Recipe Successfully!", "data":{"recipe_id":str(recipe_id)}}


@router.get("/get/meal_plans",response_model=MealPlansOut)
@update_stats(Models.Plans,Actions.Read)
async def get_meal_plans(user: User = Depends(admin_user), filters: MealPlanFilter = Depends()):
    meal_plans, total = await db_get_meal_plans(filters)
    return {
        "meal_plans": meal_plans,
        "total": total,
        "page": filters.page,
        "limit": filters.limit,
        "pages": (total + filters.limit - 1) // filters.limit
    }

@router.get("/get/meal_plan/{id}", response_model=MealPlanOut)
@update_stats(Models.Plans,Actions.Read)
async def get_meal_pan(id, _:User=Depends(admin_user)):
    return await db_get_meal_plan(id)

@router.post("/create/meal_plan", response_model=SuccessResponse)
@update_stats(Models.Plans,Actions.Create)
async def create_meal_plan(form:MealPlanCreate, user:User=Depends(admin_user)):
    meal_plan_id = await db_create_meal_plan(user._id,form)
    return {"status": "Success", "message": "Created Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}

@router.patch("/update/meal_plan/{id}", response_model=SuccessResponse)
@update_stats(Models.Plans,Actions.Update)
async def update_meal_plan(id:str,form:MealPlanUpdate, _:User=Depends(admin_user)):
    meal_plan_id = await db_update_meal_plan(id,form)
    return {"status": "Success", "message": "Updated Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}

@router.delete("/delete/meal_plan/{id}", response_model=SuccessResponse)
@update_stats(Models.Plans,Actions.Delete)
async def delete_meal_plan(id:str, _:User=Depends(admin_user)):
    meal_plan_id = await db_delete_meal_plan(id)
    return {"status": "Success", "message": "Deleted Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}