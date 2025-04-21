from pydantic import BaseModel, Field, field_serializer, field_validator
from bson import ObjectId
from typing import Optional,Any,List,Dict
from datetime import datetime


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
    image: str = None
    title: str = None
    readyInMinutes: int = None
    servings: int = None
    vegetarian: bool = None
    vegan: bool = None
    glutenFree: bool = None
    dairyFree: bool = None
    cheep: bool = None
    nutrients: List[Nutrient] = None
    ingredients: List[Ingredient] = None
    steps: List[str] = None




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
    def serialize_objectidUser(self, value: ObjectId) -> str:
        return str(value)


class MealPlansOut(BaseModel):
    meal_plans: List[MealPlan]
    page: int
    limit: int
    total: int
    pages: int


class DailyPlan(BaseModel):
    day: datetime
    recipes: Dict[str,str]
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
    title: str = None
    description: str = None
    dailyPlans: List[DailyPlan] = None
    summary: str = None
    private: bool = None


class RecipeFilter(BaseModel):
    search: Optional[str] = None
    vegetarian: Optional[bool] = None
    vegan: Optional[bool] = None
    glutenFree: Optional[bool] = None
    dairyFree: Optional[bool] = None
    cheep: Optional[bool] = None
    min_readyInMinutes: Optional[int] = None
    max_readyInMinutes: Optional[int] = None
    include_ingredients: Optional[List[str]] = None
    exclude_ingredients: Optional[List[str]] = None
    nutrients: Optional[dict] = None

    page: int = 1
    limit: int = 10

    @property
    def skip(self):
        return (self.page - 1) * self.limit


class MealPlanFilter(BaseModel):
    search: Optional[str] = None
    recipe_ids: Optional[List[str]] = None
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
    recipes: List[RecipeShort]


class MealPlanShort(BaseModel):
    id: Any = Field(alias="_id")
    title: str

    @field_serializer("id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)

class MealPlanOut(BaseModel):
    mealPlans: List[MealPlanShort]