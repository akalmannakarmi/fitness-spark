from fastapi import APIRouter

router = APIRouter()

@router.post("/get/meal_plans")
async def get_meal_plans():
    pass

@router.post("/get/meal_plan/{id}")
async def get_meal_plan(id:str):
    pass

@router.post("/create/meal_plan")
async def create_meal_plan(form):
    pass

@router.post("/update/meal_plan/{id}")
async def update_meal_plan(id,form):
    pass

@router.post("/delete/meal_plan/{id}")
async def delete_meal_plan(id):
    pass

@router.post("/set_public/meal_plan/{id}")
async def set_public_meal_plan(id):
    pass

@router.post("/set_private/meal_plan/{id}")
async def set_private_meal_plan(id):
    pass