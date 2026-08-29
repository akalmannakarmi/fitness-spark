from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from config import Actions, Models
from crud.stats import db_get_model, db_get_models, update_stats
from deps import require_admin
from schemas.stats import ModelOut, ModelsOut
from schemas.user import User

router = APIRouter()


@router.get("/models", response_model=ModelsOut)
@update_stats(Models.Stats, Actions.Read)
async def get_models(_: User = Depends(require_admin)) -> dict[str, Any]:
    models = await db_get_models()
    return {"models": models}


@router.get("/model/{model_id}", response_model=ModelOut)
@update_stats(Models.Stats, Actions.Read)
async def get_model(model_id: str, _: User = Depends(require_admin)) -> dict[str, Any]:
    model = await db_get_model(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model Not Found")
    return model
