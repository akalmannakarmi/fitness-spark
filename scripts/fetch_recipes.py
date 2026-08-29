import argparse
import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

API_URL = (
    "https://api.spoonacular.com/recipes/complexSearch"
    "?apiKey={api_key}&addRecipeNutrition=True&addRecipeInstructions=True"
)


def fetch_recipes(api_key: str, cuisine: str, number: int, offset: int) -> None:
    url = API_URL.format(api_key=api_key)

    total_results: int = 1
    while offset < total_results:
        response = requests.get(
            f"{url}&cuisine={cuisine}&number={number}&offset={offset}",
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        total_results = int(data["totalResults"])
        offset += number

        filename = f"recipies_{cuisine.lower()}_{offset}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info("Saved %s recipes to %s", number, filename)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch recipes from the Spoonacular API into recipies_*.json dumps"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("SPOONACULAR_API_KEY", ""),
        help="Spoonacular API key (or set SPOONACULAR_API_KEY)",
    )
    parser.add_argument("--cuisine", default="Vietnamese", help="Cuisine to fetch")
    parser.add_argument("--number", type=int, default=100, help="Recipes per request")
    parser.add_argument("--offset", type=int, default=0, help="Starting offset")
    args = parser.parse_args()

    if not args.api_key:
        parser.error("An API key is required (--api-key or SPOONACULAR_API_KEY)")

    logging.basicConfig(level=logging.INFO)
    fetch_recipes(args.api_key, args.cuisine, args.number, args.offset)


if __name__ == "__main__":
    main()
