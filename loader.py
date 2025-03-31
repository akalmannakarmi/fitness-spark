import glob
import json
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]
recipes_collection = database["recipes"]

async def read_and_insert_json_files():
    json_files = glob.glob("recipies_*.json")
    print(json_files)

    for file in json_files:
        print(f"Working on {file}")
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for recipe in data.get("results"):
                    nutrients = []
                    ingredients = []
                    steps = []
                    for nutrient in recipe.get("nutrition",{}).get("nutrients",[]):
                        if isinstance(nutrient,dict):
                            nutrients.append({
                                "name": nutrient.get("name",""),
                                "amount": nutrient.get("amount",-1),
                                "unit": nutrient.get("unit",""),
                            })
                    
                    for ingredient in recipe.get("nutrition",{}).get("ingredients",[]):
                        if isinstance(nutrient,dict):
                            ingredients.append({
                                "name": ingredient.get("name",""),
                                "amount": ingredient.get("amount",-1),
                                "unit": ingredient.get("unit",""),
                            })
                    
                    for instructions in recipe.get("analyzedInstructions",[]):
                        if isinstance(instructions,dict):
                            for step in instructions.get("steps",[]):
                                if isinstance(step,dict):
                                    steps.append(step.get("step",""))

                    await recipes_collection.insert_one({
                        "title":recipe.get("title",""),
                        "image":recipe.get("image",""),
                        "readyInMinutes":recipe.get("readyInMinutes",-1),
                        "servings":recipe.get("servings",-1),
                        "vegetarian":recipe.get("vegetarian",False),
                        "vegan":recipe.get("vegan",False),
                        "glutenFree":recipe.get("glutenFree",False),
                        "dairyFree":recipe.get("dairyFree",False),
                        "cheep":recipe.get("cheep",False),
                        "nutrients":nutrients,
                        "ingredients":ingredients,
                        "steps":steps,
                    })
        except Exception as e:
            print(f"Error processing {file}: {e.with_traceback()}")

import asyncio
asyncio.run(read_and_insert_json_files())
