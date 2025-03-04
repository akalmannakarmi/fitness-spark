from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..schemas import UserCreate, LoginRequest, Token, UserOut
from ..crud import create_user, authenticate_user
from ..utils import create_access_token
from ..wraper import authenticated_user
from ..models import User

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    try:
        user_id = await create_user(user)
        access_token,expires_at = create_access_token(user_id,user.expires_at)
        return {"access_token": access_token, "token_type": "bearer", "expires_at":expires_at}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token,expires_at = create_access_token(user._id,request.expires_at)
    return {"access_token": access_token, "token_type": "bearer", "expires_at":expires_at}

@router.get("/users/me", response_model=UserOut)
async def read_users_me(request:Request):
    user: User= await authenticated_user(request)
    return {"username":user.username,"email":user.email}
