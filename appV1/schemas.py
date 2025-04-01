from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId
from typing import Any,List,Dict
from datetime import date,time


class SuccessResponse(BaseModel):
    status: str
    message: str
    data: dict


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
    recipes: List[Recipe]


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
    nutrients: List[Nutrient]
    ingredients: List[Ingredient]
    steps: List[str]

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
    nutrients: List[Nutrient]
    ingredients: List[Ingredient]
    steps: List[str]


class RecipeUpdate(BaseModel):
    image: str
    title: str
    readyInMinutes: int
    servings: int
    vegetarian: bool
    vegan: bool
    glutenFree: bool
    dairyFree: bool
    cheep: bool
    nutrients: List[Nutrient]
    ingredients: List[Ingredient]
    steps: List[str]












class MealPlan(BaseModel):
    id: Any = Field(alias="_id")
    title: str
    description: str
    summary: str
    private: bool

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)


class MealPlansOut(BaseModel):
    meal_plans: List[MealPlan]


class DailyPlan(BaseModel):
    day: date
    recipes: Dict[time,Recipe]
    summary: str


class MealPlanOut(BaseModel):
    id: Any = Field(alias="_id")
    user: Any
    title: str
    description: str
    dailyPlans: List[DailyPlan]
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
    dailyPlans: List[DailyPlan]
    summary: str
    private: bool


class MealPlanUpdate(BaseModel):
    title: str
    description: str
    dailyPlans: List[DailyPlan]
    summary: str
    private: bool
