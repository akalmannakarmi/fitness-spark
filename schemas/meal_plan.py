from datetime import datetime
from typing import Any

from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer


class MealPlan(BaseModel):
    id: Any = Field(alias="_id")
    user: Any
    title: str
    description: str
    summary: str
    private: bool

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)

    @field_serializer("user")
    def serialize_objectid_user(self, value: ObjectId) -> str:
        return str(value)


class MealPlansOut(BaseModel):
    meal_plans: list[MealPlan]
    page: int
    limit: int
    total: int
    pages: int


class DailyPlan(BaseModel):
    day: datetime
    recipes: dict[str, str]
    summary: str


class MealPlanOut(BaseModel):
    id: Any = Field(alias="_id")
    user: Any
    title: str
    description: str
    dailyPlans: list[DailyPlan]
    summary: str
    private: bool

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)

    @field_serializer("user")
    def serialize_objectid_user(self, value: ObjectId) -> str:
        return str(value)


class MealPlanCreate(BaseModel):
    title: str
    description: str
    dailyPlans: list[DailyPlan]
    summary: str
    private: bool


class MealPlanUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    dailyPlans: list[DailyPlan] | None = None
    summary: str | None = None
    private: bool | None = None


class MealPlanFilter(BaseModel):
    search: str | None = None
    recipe_ids: list[str] | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.limit
