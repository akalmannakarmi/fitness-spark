from datetime import date, time

from bson import ObjectId


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
    nutrients: list[Nutrient]
    ingredients: list[Ingredient]
    steps: list[str]


class DailyPlan:
    day: date
    recipes: dict[time, Recipe]
    summary: str


class MealPlan:
    _id: ObjectId
    user: ObjectId
    title: str
    description: str
    dailyPlans: list[DailyPlan]
    summary: str
    private: bool
