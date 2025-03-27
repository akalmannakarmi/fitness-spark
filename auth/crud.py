from os.path import exists
from .schemas import AdminUserCreate, UserCreate,UserUpdate
from .utils import hash_password, verify_password
from .database import users_collection
from .models import User
from bson import ObjectId
from utils.exception import CustomAPIException

async def create_user(user: UserCreate) -> str:
    exists = await users_collection.find_one({"username":user.username})
    if exists:
        raise CustomAPIException(400,"User Exists", "User with the provided username already exists!")

    result = await users_collection.insert_one({
        "username":user.username,
        "email":user.email,
        "password":hash_password(user.password),
        "groups":["user"]
    })
    return str(result.inserted_id)

async def authenticate_user(username: str, password: str)->User:
    user = await users_collection.find_one({"username":username})

    if user and verify_password(password,user.get("password")):
        return User(**user)
    raise CustomAPIException(401,"Invalid Credentials","User does not exists or invalid password!")

async def create_user_full(user: AdminUserCreate) -> str:
    exists = await users_collection.find_one({"username":user.username})
    if exists:
        raise CustomAPIException(400, "User Exists", "User with the provided username already exists!")

    result = await users_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "groups": user.groups,
    })
    return str(result.inserted_id)


async def get_user(user_id:str) -> User:
    user = await users_collection.find_one({"_id":ObjectId(user_id)})
    if not user:
        raise CustomAPIException(404,"User Not Found","User with the provided Id not found!")
    return User(**user)

async def get_users():
    users_cursor = users_collection.find({})
    return await users_cursor.to_list()

async def update_user(id:str,form:UserUpdate) -> str:
    update = {}
    if form.username:
        update["username"] = form.username
    if form.email:
        update["email"] = form.email
    if form.password:
        update["password"] = form.password
    if form.groups:
        update["groups"] = form.groups
    
    result = await users_collection.update_one({"_id":ObjectId(id)},update)
    return result.upserted_id

async def delete_user(id:str) -> None:
    await users_collection.delete_one({"_id":ObjectId(id)})
