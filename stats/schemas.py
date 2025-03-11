from pydantic import BaseModel,field_serializer,Field
from typing import Optional,List,Tuple,Dict,Any
from bson import ObjectId

class ModelsOut(BaseModel):
    models: List[Tuple[str,str]]

    @field_serializer("models")
    def serialize_objectid(self, value):
        return [(str(obj_id), name) for obj_id, name in value]

class ModelOut(BaseModel):
    id: Any = Field(alias="_id")
    model: str
    logs: Dict[str, Dict[str, Dict[str, float]]]

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)