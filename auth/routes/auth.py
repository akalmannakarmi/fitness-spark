from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..schemas import UserCreate, LoginRequest, Token, UserOut
from ..crud import create_user, authenticate_user
from ..utils import create_access_token
from ..wraper import auth_user
from ..models import User
from stats.wraper import update_stats,Models,Actions

router = APIRouter()

@router.post("/signup", response_model=Token)
@update_stats(Models.User,Actions.Create)
async def signup(user: UserCreate):
    try:
        user_id = await create_user(user)
        access_token,expires_at = create_access_token(user_id,user.expires_at)
        return {"access_token": access_token, "token_type": "bearer", "expires_at":expires_at}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=Token)
@update_stats(Models.User,Actions.Read)
async def login(request: LoginRequest):
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token,expires_at = create_access_token(user._id,request.expires_at)
    return {"access_token": access_token, "token_type": "bearer", "expires_at":expires_at}

@router.get("/users/me", response_model=UserOut)
@update_stats(Models.User,Actions.Read)
async def read_users_me(user:User=Depends(auth_user)):
    return {"username":user.username,"email":user.email}
