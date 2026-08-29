from fastapi import HTTPException, Request

from crud.users import get_user
from schemas.user import User
from security import get_token, verify_token


async def get_current_user(request: Request, token: str | None = None) -> User:
    if token is None:
        token = get_token(request)
        if token is None:
            raise HTTPException(status_code=401, detail="Invalid or missing token")

    try:
        user_id = verify_token(token)
        user: User = await get_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Failed to authenticate. Exception: {e}"
        ) from None


async def require_admin(request: Request, token: str | None = None) -> User:
    user: User = await get_current_user(request, token)
    if "admin" in user.groups:
        return user
    raise HTTPException(status_code=403, detail="Admin only!")
