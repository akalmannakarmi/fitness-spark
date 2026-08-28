from fastapi import APIRouter, Depends, HTTPException

from auth.wraper import admin_user
from config import Actions, Models

from ..crud import db_get_model, db_get_models
from ..schemas import ModelOut, ModelsOut
from ..wraper import update_stats

router = APIRouter()


@router.get("/models", response_model=ModelsOut)
@update_stats(Models.Stats, Actions.Read)
async def get_models(_=Depends(admin_user)):
    models = await db_get_models()
    return {"models": models}


@router.get("/model/{model_id}", response_model=ModelOut)
@update_stats(Models.Stats, Actions.Read)
async def get_model(model_id: str, _=Depends(admin_user)):
    model = await db_get_model(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model Not Found")
    return model
