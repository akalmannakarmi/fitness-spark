from typing import Any

from fastapi import APIRouter, Depends, Query

from config import Actions, Models
from crud.stats import update_stats
from crud.users import (
    create_user_full,
    db_list_users,
    delete_user,
    get_user,
    get_users,
    update_user,
)
from deps import require_admin
from schemas.common import MongoObjectId, SuccessResponse, num_pages
from schemas.user import (
    AdminUserCreate,
    User,
    UserOut,
    UsersListOut,
    UsersOut,
    UserUpdate,
)

router = APIRouter()


@router.post("/create/user", response_model=SuccessResponse)
@update_stats(Models.User, Actions.Create)
async def create(
    form: AdminUserCreate, _: User = Depends(require_admin)
) -> dict[str, Any]:
    user_id = await create_user_full(form)
    return {
        "status": "Success",
        "message": "Created User Successfully!",
        "data": {"user_id": str(user_id)},
    }


@router.get("/list/users/", response_model=UsersListOut)
@update_stats(Models.User, Actions.Read)
async def list_users(_: User = Depends(require_admin)) -> dict[str, Any]:
    users = await db_list_users()
    return {"users": users}


@router.get("/get/users/", response_model=UsersOut)
@update_stats(Models.User, Actions.Read)
async def get_all(
    search: str = "",
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    _: User = Depends(require_admin),
) -> dict[str, Any]:
    users, total = await get_users(search=search, page=page, limit=limit)
    return {
        "users": users,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": num_pages(total, limit),
    }


@router.get("/get/user/{user_id}", response_model=UserOut)
@update_stats(Models.User, Actions.Read)
async def get(
    user_id: MongoObjectId, _: User = Depends(require_admin)
) -> dict[str, Any]:
    user: User = await get_user(user_id)
    return {
        "_id": user.id,
        "username": user.username,
        "email": user.email,
        "groups": user.groups,
    }


@router.put("/update/user/{user_id}", response_model=SuccessResponse)
@update_stats(Models.User, Actions.Update)
async def update(
    user_id: MongoObjectId, form: UserUpdate, _: User = Depends(require_admin)
) -> dict[str, Any]:
    await update_user(user_id, form)
    return {
        "status": "Success",
        "message": "Updated User Successfully!",
        "data": {"user_id": user_id},
    }


@router.delete("/delete/user/{user_id}", response_model=SuccessResponse)
@update_stats(Models.User, Actions.Delete)
async def delete(
    user_id: MongoObjectId, _: User = Depends(require_admin)
) -> dict[str, Any]:
    await delete_user(user_id)
    return {
        "status": "Success",
        "message": "Deleted User Successfully!",
        "data": {"user_id": user_id},
    }
