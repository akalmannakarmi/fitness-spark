from pydantic import BaseModel,Field,field_serializer
from typing import Any,Optional,List
from bson import ObjectId

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    expires_at: Optional[float] = None

class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str
    groups: List[str]

class UserOut(BaseModel):
    id: Any = Field(alias="_id")
    username: str
    email: str
    groups: List[str]

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)

class UsersOut(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    users: List[UserOut]

class LoginRequest(BaseModel):
    username: str
    password: str
    expires_at: Optional[float] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: float
    admin: bool

class SuccessResponse(BaseModel):
    status: str
    message: str
    data: dict

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    groups: Optional[List[str]] = None

class UserShort(BaseModel):
    id: Any = Field(alias="_id")
    username: str

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)

class UsersListOut(BaseModel):
    users: List[UserShort]
