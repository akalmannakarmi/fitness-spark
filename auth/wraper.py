from fastapi import Request, HTTPException
from .utils import verify_token
from .crud import get_user

async def authenticated_user(request:Request):
    authorization: str = request.headers.get("Authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    token = authorization.removeprefix("Bearer ").strip()

    try:
        user_id = verify_token(token)
        user = await get_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to authenticate. Exception: {e}")
