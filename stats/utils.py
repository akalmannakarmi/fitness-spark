from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException,Request
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from bson import ObjectId
from typing import Tuple

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id,expires_at:float=None) -> Tuple[str,float]:
    if not expires_at:
        expires_at = (datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()

    to_encode = {"user_id":str(user_id),"expires_at": expires_at}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt,expires_at

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")
    
    if "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token: missing user_id.")
    if "expires_at" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token: missing expiry date.")
    if payload["expires_at"] < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=401, detail="Token has expired!")

    return ObjectId(payload["user_id"])

