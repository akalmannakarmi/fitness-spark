from typing import Any

from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer


class ModelsOut(BaseModel):
    models: list[dict[str, str | int]]


class ModelOut(BaseModel):
    id: Any = Field(alias="_id")
    model: str
    count: int
    logs: dict[str, dict[str, dict[str, float]]]

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)
