from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..schemas import ModelsOut,ModelOut
from ..crud import db_get_models,db_get_model
from ..wraper import update_stats,Models,Actions
from auth.wraper import admin_user,User
from bson import ObjectId

router = APIRouter()


@router.get("/models/", response_model=ModelsOut)
@update_stats(Models.Stats,Actions.Read)
async def get_models(user:User=Depends(admin_user)):
    models = await db_get_models()
    return {"models":models}


@router.get("/model/{model_id}", response_model=ModelOut)
@update_stats(Models.Stats,Actions.Read)
async def get_model(model_id:str,user:User=Depends(admin_user)):
    model = await db_get_model(model_id)
    if model is None:
        raise HTTPException(status_code=404,detail="Model Not Found")
    return model
