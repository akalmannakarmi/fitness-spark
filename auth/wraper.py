from fastapi import Request, HTTPException
from .utils import verify_token,get_token
from .crud import get_user
from .models import User

async def auth_user(request:Request,token:str=None):
    if token is None:
        token = get_token(request)

    try:
        user_id = verify_token(token)
        user:User = await get_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to authenticate. Exception: {e}")


async def admin_user(request:Request,token:str=None):
    user:User = await auth_user(request,token)
    if "admin" in user.groups:
        return user
    raise HTTPException(status_code=401, detail=f"Admin only!")
    
