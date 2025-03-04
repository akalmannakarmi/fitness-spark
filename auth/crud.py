from .schemas import UserCreate
from .utils import hash_password, verify_password
from .database import users_collection
from .models import User
from bson import ObjectId

async def create_user(user: UserCreate) -> str:
    exists = await users_collection.find_one({"username":user.username})
    if exists:
        raise ValueError("User already exists")

    result = await users_collection.insert_one({
        "username":user.username,
        "email":user.email,
        "password":hash_password(user.password),
    })
    return str(result.inserted_id)

async def authenticate_user(username: str, password: str)->User:
    user = await users_collection.find_one({"username":username})

    if user and verify_password(password,user.get("password")):
        return User(**user)
    return None

async def get_user(user_id:ObjectId) -> User:
    user = await users_collection.find_one({"_id":user_id})
    if not user:
        raise LookupError("User with the provided Id not found")
    return User(**user)
