from fastapi import APIRouter, Depends, HTTPException, status

from config import Actions, Models
from stats.wraper import update_stats

from ..crud import authenticate_user, create_user
from ..models import User
from ..schemas import LoginRequest, Token, UserCreate, UserOut
from ..utils import create_access_token
from ..wraper import auth_user

router = APIRouter()


@router.post("/signup", response_model=Token)
@update_stats(Models.User, Actions.Create)
async def signup(user: UserCreate):
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
async def login(request: LoginRequest):
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token, expires_at = create_access_token(user._id, request.expires_at)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": expires_at,
        "admin": "admin" in user.groups,
    }


@router.get("/users/me", response_model=UserOut)
@update_stats(Models.User, Actions.Read)
async def read_users_me(user: User = Depends(auth_user)):
    return {
        "_id": user._id,
        "username": user.username,
        "email": user.email,
        "groups": user.groups,
    }
