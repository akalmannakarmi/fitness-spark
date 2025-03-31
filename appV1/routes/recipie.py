from fastapi import APIRouter

router = APIRouter()

@router.post("/get/recipes")
async def get_recipes():
    pass

@router.post("/get/recipe/{id}")
async def get_recipe(id):
    pass