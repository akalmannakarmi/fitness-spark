from typing import TYPE_CHECKING

from fastapi import HTTPException, Request

from .crud import get_user
from .utils import get_token, verify_token

if TYPE_CHECKING:
    from .models import User


async def auth_user(request: Request, token: str | None = None):
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


async def admin_user(request: Request, token: str | None = None):
    user: User = await auth_user(request, token)
    if "admin" in user.groups:
        return user
    raise HTTPException(status_code=403, detail="Admin only!")
