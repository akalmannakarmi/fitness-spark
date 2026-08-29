from typing import Any

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_serializer


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str
    groups: list[str]


class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ObjectId = Field(alias="_id")
    username: str
    email: str
    password: str
    groups: list[str]


class UserOut(BaseModel):
    id: Any = Field(alias="_id")
    username: str
    email: str
    groups: list[str]

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)


class UsersOut(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    users: list[UserOut]


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: float
    admin: bool


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    groups: list[str] | None = None


class UserShort(BaseModel):
    id: Any = Field(alias="_id")
    username: str

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)


class UsersListOut(BaseModel):
    users: list[UserShort]
