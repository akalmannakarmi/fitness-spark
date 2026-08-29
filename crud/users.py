import re
from typing import Any

from bson import ObjectId

from database import users_collection
from exceptions import CustomAPIException
from schemas.user import AdminUserCreate, User, UserCreate, UserUpdate
from security import hash_password, verify_password


async def create_user(user: UserCreate) -> str:
    exists = await users_collection.find_one({"username": user.username})
    if exists:
        raise CustomAPIException(
            400, "User Exists", "User with the provided username already exists!"
        )

    result = await users_collection.insert_one(
        {
            "username": user.username,
            "email": user.email,
            "password": hash_password(user.password),
            "groups": ["user"],
        }
    )
    return str(result.inserted_id)


async def authenticate_user(username: str, password: str) -> User:
    user = await users_collection.find_one({"username": username})

    if user and verify_password(password, user.get("password", "")):
        return User(**user)
    raise CustomAPIException(
        401, "Invalid Credentials", "User does not exists or invalid password!"
    )


async def create_user_full(user: AdminUserCreate) -> str:
    exists = await users_collection.find_one({"username": user.username})
    if exists:
        raise CustomAPIException(
            400, "User Exists", "User with the provided username already exists!"
        )

    result = await users_collection.insert_one(
        {
            "username": user.username,
            "email": user.email,
            "password": hash_password(user.password),
            "groups": user.groups,
        }
    )
    return str(result.inserted_id)


async def get_user(user_id: str) -> User:
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise CustomAPIException(
            404, "User Not Found", "User with the provided Id not found!"
        )
    return User(**user)


async def get_users(
    search: str = "", page: int = 1, limit: int = 10
) -> tuple[list[dict[str, Any]], int]:
    query: dict[str, Any] = {}
    if search:
        query["username"] = {"$regex": re.escape(search), "$options": "i"}

    total = await users_collection.count_documents(query)

    cursor = users_collection.find(query).skip((page - 1) * limit).limit(limit)

    users = await cursor.to_list(length=limit)
    return users, total


async def update_user(user_id: str, form: UserUpdate) -> str:
    update: dict[str, Any] = {}
    if form.username:
        update["username"] = form.username
    if form.email:
        update["email"] = form.email
    if form.password:
        update["password"] = hash_password(form.password)
    if form.groups:
        update["groups"] = form.groups
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update}
    )
    if result.matched_count == 0:
        raise CustomAPIException(
            404, "User Not Found", "User with the provided Id not found!"
        )
    return user_id


async def delete_user(user_id: str) -> None:
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise CustomAPIException(
            404, "User Not Found", "User with the provided Id not found!"
        )


async def db_list_users() -> list[dict[str, Any]]:
    cursor = users_collection.find({}, {"_id": 1, "username": 1})
    result = await cursor.to_list()
    return result
