from fastapi import APIRouter

router = APIRouter()

@router.get("/add")
def add():
    return {"detail":"work in progress"}