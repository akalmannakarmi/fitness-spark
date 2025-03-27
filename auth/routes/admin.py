from fastapi import APIRouter, Depends, Request
from ..schemas import AdminUserCreate, UserUpdate, UserOut, UsersOut, SuccessResponse
from ..crud import create_user_full, get_users, get_user, update_user, delete_user
from ..wraper import admin_user
from ..models import User
from stats.wraper import update_stats,Models,Actions

router = APIRouter()

@router.post("/create/user", response_model=SuccessResponse)
@update_stats(Models.User,Actions.Create)
async def create(form:AdminUserCreate,_:User=Depends(admin_user)):
    user_id = await create_user_full(form)
    return {"status": "Success", "message": "Created User Successfully!", "data":{"user_id":str(user_id)}}


@router.get("/get/users/", response_model=UsersOut)
@update_stats(Models.User,Actions.Read)
async def get_all(_:User=Depends(admin_user)):
    users = await get_users()
    return {"users":users}

@router.get("/get/user/{id}", response_model=UserOut)
@update_stats(Models.User,Actions.Read)
async def get(id:str, _:User=Depends(admin_user)):
    user:User = await get_user(id)
    return {"_id":str(user._id),"username":user.username,"email":user.email}


@router.put("/update/user/{id}", response_model=SuccessResponse)
@update_stats(Models.User,Actions.Update)
async def update(id:str, form:UserUpdate, _:User=Depends(admin_user)):
    user_id = await update_user(id,form)
    return {"status": "Success", "message": "Updated User Successfully!", "data":{"user_id":str(user_id)}}


@router.delete("/delete/user/{id}", response_model=SuccessResponse)
@update_stats(Models.User,Actions.Delete)
async def delete(id:str,_:User=Depends(admin_user)):
    await delete_user(id)
    return {"status":"Success", "message": "Deleted User Successfully!", "data":{"user_id":str(id)}}
