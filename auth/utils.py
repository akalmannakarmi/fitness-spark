from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException, Request

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(user_id, expires_at: float | None = None) -> tuple[str, float]:
    if not expires_at:
        expires_at = (
            datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        ).timestamp()

    to_encode = {"user_id": str(user_id), "expires_at": expires_at}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expires_at


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Could not validate token"
        ) from None

    if "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token: missing user_id.")
    if "expires_at" not in payload:
        raise HTTPException(
            status_code=401, detail="Invalid token: missing expiry date."
        )
    if payload["expires_at"] < datetime.now(UTC).timestamp():
        raise HTTPException(status_code=401, detail="Token has expired!")

    return payload["user_id"]  # type: ignore[no-any-return]


def get_token(request: Request) -> str | None:
    if "token" in request.query_params:
        return request.query_params.get("token")

    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    return authorization.removeprefix("Bearer ").strip()
