from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

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
    access_token, expires_at = create_access_token(user_id, user.expires_at)
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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token, expires_at = create_access_token(user.id, request.expires_at)
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
