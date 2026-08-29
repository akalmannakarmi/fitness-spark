from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator


class SuccessResponse(BaseModel):
    status: str
    message: str
    data: dict[str, Any]


class Paginated[T](BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    items: list[T]


def _validate_object_id(value: Any) -> str:
    if not ObjectId.is_valid(str(value)):
        raise ValueError("Invalid ObjectId")
    return str(value)


MongoObjectId = Annotated[str, BeforeValidator(_validate_object_id)]


def num_pages(total: int, limit: int) -> int:
    return (total + limit - 1) // limit
