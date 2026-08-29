from typing import Any

from fastapi import APIRouter, Depends

from config import Actions, Models
from crud.stats import update_stats
from crud.users import authenticate_user, create_user
from deps import get_current_user
from schemas.user import LoginRequest, Token, User, UserCreate, UserOut
from security import create_access_token

router = APIRouter()


@router.post("/signup", response_model=Token)
@update_stats(Models.User, Actions.Create)
async def signup(user: UserCreate) -> dict[str, Any]:
    user_id = await create_user(user)
    access_token, expires_at = create_access_token(user_id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": expires_at,
        "admin": False,
    }


@router.post("/login", response_model=Token)
@update_stats(Models.User, Actions.Read)
async def login(request: LoginRequest) -> dict[str, Any]:
    user = await authenticate_user(request.username, request.password)
    access_token, expires_at = create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": expires_at,
        "admin": "admin" in user.groups,
    }


@router.get("/users/me", response_model=UserOut)
@update_stats(Models.User, Actions.Read)
async def read_users_me(user: User = Depends(get_current_user)) -> dict[str, Any]:
    return {
        "_id": user.id,
        "username": user.username,
        "email": user.email,
        "groups": user.groups,
    }
