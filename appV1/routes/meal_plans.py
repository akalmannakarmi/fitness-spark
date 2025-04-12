from fastapi import APIRouter,Depends
from ..crud import db_get_public_meal_plans,db_get_user_meal_plans,db_get_user_meal_plan,db_create_meal_plan,db_update_user_meal_plan,db_delete_user_meal_plan
from ..schemas import SuccessResponse,MealPlansOut,MealPlanOut,MealPlanCreate,MealPlanUpdate
from auth.wraper import User,auth_user
from stats.wraper import update_stats
from config import Models, Actions

router = APIRouter()

@router.get("/get/meal_plans",response_model=MealPlansOut)
@update_stats(Models.Plans,Actions.Read)
async def get_meal_plans(_:User=Depends(auth_user)):
    meal_plans = await db_get_public_meal_plans()
    return {"meal_plans":meal_plans}

@router.get("/get/my/meal_plans",response_model=MealPlansOut)
@update_stats(Models.Plans,Actions.Read)
async def get_user_meal_plans(user:User=Depends(auth_user)):
    meal_plans = await db_get_user_meal_plans(user._id)
    return {"meal_plans":meal_plans}

@router.get("/get/meal_plan/{id}", response_model=MealPlanOut)
@update_stats(Models.Plans,Actions.Read)
async def get_meal_plan(id:str,user:User=Depends(auth_user)):
    return await db_get_user_meal_plan(id,user._id)

@router.post("/create/meal_plan", response_model=SuccessResponse)
@update_stats(Models.Plans,Actions.Create)
async def create_meal_plan(form:MealPlanCreate, user:User=Depends(auth_user)):
    meal_plan_id = await db_create_meal_plan(user._id,form)
    return {"status": "Success", "message": "Created Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}

@router.patch("/update/meal_plan/{id}", response_model=SuccessResponse)
@update_stats(Models.Plans,Actions.Update)
async def update_meal_plan(id:str,form:MealPlanUpdate,user:User=Depends(auth_user)):
    meal_plan_id = await db_update_user_meal_plan(id,user._id,form)
    return {"status": "Success", "message": "Updated Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}

@router.delete("/delete/meal_plan/{id}")
@update_stats(Models.Plans,Actions.Delete)
async def delete_meal_plan(id:str,user:User=Depends(auth_user)):
    meal_plan_id = await db_delete_user_meal_plan(id,user._id)
    return {"status": "Success", "message": "Deleted Meal Plan Successfully!", "data":{"meal_plan_id":str(meal_plan_id)}}
