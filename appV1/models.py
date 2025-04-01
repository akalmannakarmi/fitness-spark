from bson import ObjectId
from typing import List,Dict
from datetime import date
from datetime import time

class Nutrient:
    name: str
    amount: float
    unit: str

class Ingredient:
    name: str
    amount: float
    unit: str

class Recipe:
    _id: ObjectId
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


class DailyPlan:
    day: date
    recipes: Dict[time,Recipe]
    summary: str


class MealPlan:
    _id: ObjectId
    user: ObjectId
    title: str
    description: str
    dailyPlans: List[DailyPlan]
    summary: str
    private: bool
