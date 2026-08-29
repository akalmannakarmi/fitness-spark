import asyncio
import glob
import json
import logging
from typing import Any

from database import recipes_collection

logger = logging.getLogger(__name__)


async def read_and_insert_json_files() -> None:
    json_files = glob.glob("recipies_*.json")
    logger.info("Found %s JSON files", len(json_files))

    for file in json_files:
        logger.info("Working on %s", file)
        try:
            with open(file, encoding="utf-8") as f:
                data = json.load(f)
                for recipe in data.get("results", []):
                    nutrients: list[dict[str, Any]] = []
                    ingredients: list[dict[str, Any]] = []
                    steps: list[str] = []

                    for nutrient in recipe.get("nutrition", {}).get("nutrients", []):
                        if isinstance(nutrient, dict):
                            nutrients.append(
                                {
                                    "name": nutrient.get("name", ""),
                                    "amount": nutrient.get("amount", -1),
                                    "unit": nutrient.get("unit", ""),
                                }
                            )

                    for ingredient in recipe.get("nutrition", {}).get(
                        "ingredients", []
                    ):
                        if isinstance(ingredient, dict):
                            ingredients.append(
                                {
                                    "name": ingredient.get("name", ""),
                                    "amount": ingredient.get("amount", -1),
                                    "unit": ingredient.get("unit", ""),
                                }
                            )

                    for instructions in recipe.get("analyzedInstructions", []):
                        if isinstance(instructions, dict):
                            for step in instructions.get("steps", []):
                                if isinstance(step, dict):
                                    steps.append(step.get("step", ""))

                    await recipes_collection.insert_one(
                        {
                            "title": recipe.get("title", ""),
                            "image": recipe.get("image", ""),
                            "readyInMinutes": recipe.get("readyInMinutes", -1),
                            "servings": recipe.get("servings", -1),
                            "vegetarian": recipe.get("vegetarian", False),
                            "vegan": recipe.get("vegan", False),
                            "glutenFree": recipe.get("glutenFree", False),
                            "dairyFree": recipe.get("dairyFree", False),
                            "cheep": recipe.get("cheep", False),
                            "nutrients": nutrients,
                            "ingredients": ingredients,
                            "steps": steps,
                        }
                    )
        except Exception as e:
            logger.error("Error processing %s: %s", file, e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(read_and_insert_json_files())
