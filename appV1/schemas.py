from datetime import datetime
from typing import Any

from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer


class SuccessResponse(BaseModel):
    status: str
    message: str
    data: dict[str, Any]


class Recipe(BaseModel):
    id: Any = Field(alias="_id")
    image: str
    title: str
    readyInMinutes: int
    servings: int
    vegetarian: bool
    vegan: bool
    glutenFree: bool
    dairyFree: bool
    cheep: bool

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)


class RecipesOut(BaseModel):
    recipes: list[Recipe]
    page: int
    limit: int
    total: int
    pages: int


class Nutrient(BaseModel):
    name: str
    amount: float
    unit: str


class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str


class RecipeOut(BaseModel):
    id: Any = Field(alias="_id")
    image: str
    title: str
    readyInMinutes: int
    servings: int
    vegetarian: bool
    vegan: bool
    glutenFree: bool
    dairyFree: bool
    cheep: bool
    nutrients: list[Nutrient]
    ingredients: list[Ingredient]
    steps: list[str]

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)


class RecipeCreate(BaseModel):
    image: str
    title: str
    readyInMinutes: int
    servings: int
    vegetarian: bool
    vegan: bool
    glutenFree: bool
    dairyFree: bool
    cheep: bool
    nutrients: list[Nutrient]
    ingredients: list[Ingredient]
    steps: list[str]


class RecipeUpdate(BaseModel):
    image: str | None = None
    title: str | None = None
    readyInMinutes: int | None = None
    servings: int | None = None
    vegetarian: bool | None = None
    vegan: bool | None = None
    glutenFree: bool | None = None
    dairyFree: bool | None = None
    cheep: bool | None = None
    nutrients: list[Nutrient] | None = None
    ingredients: list[Ingredient] | None = None
    steps: list[str] | None = None


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


class RecipeFilter(BaseModel):
    search: str | None = None
    vegetarian: bool | None = None
    vegan: bool | None = None
    glutenFree: bool | None = None
    dairyFree: bool | None = None
    cheep: bool | None = None
    min_readyInMinutes: int | None = None
    max_readyInMinutes: int | None = None
    include_ingredients: list[str] | None = None
    exclude_ingredients: list[str] | None = None
    nutrients: dict[str, Any] | None = None

    page: int = 1
    limit: int = 10

    @property
    def skip(self):
        return (self.page - 1) * self.limit


class MealPlanFilter(BaseModel):
    search: str | None = None
    recipe_ids: list[str] | None = None
    page: int = 1
    limit: int = 10

    @property
    def skip(self):
        return (self.page - 1) * self.limit


class RecipeShort(BaseModel):
    id: Any = Field(alias="_id")
    title: str

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)


class RecipeListOut(BaseModel):
    recipes: list[RecipeShort]


class MealPlanShort(BaseModel):
    id: Any = Field(alias="_id")
    title: str

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)


class MealPlanListOut(BaseModel):
    mealPlans: list[MealPlanShort]
