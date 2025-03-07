from fastapi import Request, HTTPException
from .utils import verify_token
from .crud import get_user
from .models import User

async def auth_user(request:Request,token:str=None):
    authorization: str = request.headers.get("Authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    token = authorization.removeprefix("Bearer ").strip()

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
    
